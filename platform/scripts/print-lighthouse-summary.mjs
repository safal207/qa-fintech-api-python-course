import fs from 'node:fs';
import path from 'node:path';

const resultsDir = path.resolve('lighthouse-results');
const summaryFile = process.env.GITHUB_STEP_SUMMARY;

function walk(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const fullPath = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(fullPath) : [fullPath];
  });
}

function readLighthouseReports() {
  return walk(resultsDir)
    .filter((file) => file.endsWith('.json'))
    .flatMap((file) => {
      try {
        const raw = fs.readFileSync(file, 'utf8');
        const json = JSON.parse(raw);
        if (!json.categories || !json.finalDisplayedUrl) return [];

        const profile = file.includes(`${path.sep}mobile${path.sep}`)
          ? 'Mobile'
          : file.includes(`${path.sep}desktop${path.sep}`)
            ? 'Desktop'
            : 'Unknown';

        return [{ file, profile, report: json }];
      } catch {
        return [];
      }
    });
}

function score(category) {
  if (!category || typeof category.score !== 'number') return 'n/a';
  return Math.round(category.score * 100);
}

function status(value, warningThreshold = 90) {
  if (value === 'n/a') return '⚪';
  if (value >= warningThreshold) return '🟢';
  if (value >= 80) return '🟡';
  return '🔴';
}

function buildMarkdown(reports) {
  const lines = [
    '# Lighthouse audit summary',
    '',
    '| Profile | URL | Performance | Accessibility | Best Practices | SEO |',
    '|---|---|---:|---:|---:|---:|',
  ];

  for (const { profile, report } of reports) {
    const categories = report.categories;
    const performance = score(categories.performance);
    const accessibility = score(categories.accessibility);
    const bestPractices = score(categories['best-practices']);
    const seo = score(categories.seo);

    lines.push(
      `| ${profile} | ${report.finalDisplayedUrl} | ${status(performance, 90)} ${performance} | ${status(accessibility, 90)} ${accessibility} | ${status(bestPractices, 90)} ${bestPractices} | ${status(seo, 90)} ${seo} |`,
    );
  }

  lines.push('', '## Reading the result', '');
  lines.push('- 🟢 90-100: healthy');
  lines.push('- 🟡 80-89: acceptable, but worth improving');
  lines.push('- 🔴 below 80: should be fixed');

  return `${lines.join('\n')}\n`;
}

const reports = readLighthouseReports();

if (reports.length === 0) {
  const message = 'No Lighthouse JSON reports found. Check lighthouse-results artifact.';
  console.log(message);
  if (summaryFile) fs.appendFileSync(summaryFile, `# Lighthouse audit summary\n\n${message}\n`);
  process.exit(0);
}

const markdown = buildMarkdown(reports);
console.log(markdown);

if (summaryFile) {
  fs.appendFileSync(summaryFile, markdown);
}
