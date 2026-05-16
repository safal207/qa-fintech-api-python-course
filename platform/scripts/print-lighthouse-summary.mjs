import fs from 'node:fs';
import path from 'node:path';

const resultsDir = path.resolve('lighthouse-results');
const summaryFile = process.env.GITHUB_STEP_SUMMARY;
const recommendationReportPath = path.join(resultsDir, 'lighthouse-recommendations.md');

const auditFileMap = [
  {
    match: /title|meta-description|canonical|crawlable|robots|hreflang|structured-data|link-text|is-crawlable/i,
    files: [
      'platform/src/components/CourseShell.astro',
      'platform/src/pages/index.astro',
      'platform/src/pages/lessons/[slug].astro',
      'platform/astro.config.mjs',
      'platform/public/robots.txt',
    ],
    recommendation: 'Improve page metadata, canonical URL, crawlability, robots/sitemap, and meaningful link text.',
  },
  {
    match: /unused-javascript|legacy-javascript|bootup-time|mainthread-work|total-byte-weight|render-blocking|critical-request|third-party|uses-rel-preload|uses-rel-preconnect/i,
    files: [
      'platform/package.json',
      'platform/astro.config.mjs',
      'platform/src/components/CourseShell.astro',
      'platform/src/pages/index.astro',
      'platform/src/pages/lessons/[slug].astro',
    ],
    recommendation: 'Reduce client JavaScript, remove unused framework integrations, and keep the platform mostly static until interactive islands are needed.',
  },
  {
    match: /color-contrast|aria|button-name|link-name|heading-order|html-has-lang|label|list|tabindex|focus/i,
    files: [
      'platform/src/styles/global.css',
      'platform/src/components/CourseShell.astro',
      'platform/src/pages/index.astro',
      'platform/src/pages/lessons/[slug].astro',
    ],
    recommendation: 'Improve accessibility semantics, labels, focus states, contrast, and keyboard/touch navigation.',
  },
  {
    match: /viewport|tap-targets|font-size|content-width|interactive|mobile/i,
    files: [
      'platform/src/styles/global.css',
      'platform/src/pages/index.astro',
      'platform/src/pages/lessons/[slug].astro',
    ],
    recommendation: 'Tune mobile typography, spacing, tap targets, overflow behavior, and responsive navigation.',
  },
  {
    match: /csp|xss|https|vulnerable|inspector|console-errors|errors-in-console|deprecations|doctype/i,
    files: [
      'platform/src/components/CourseShell.astro',
      'platform/package.json',
      '.github/workflows/lighthouse.yml',
      '.github/workflows/pages.yml',
    ],
    recommendation: 'Check security headers, dependency hygiene, console/runtime errors, and deployment settings.',
  },
];

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

function auditScore(audit) {
  if (!audit || typeof audit.score !== 'number') return 'n/a';
  return Math.round(audit.score * 100);
}

function status(value, warningThreshold = 90) {
  if (value === 'n/a') return '⚪';
  if (value >= warningThreshold) return '🟢';
  if (value >= 80) return '🟡';
  return '🔴';
}

function severity(value) {
  if (value === 'n/a') return 'info';
  if (value < 50) return 'high';
  if (value < 80) return 'medium';
  if (value < 100) return 'low';
  return 'pass';
}

function stripMarkdownLinks(text = '') {
  return text
    .replace(/\[([^\]]+)\]\([^\)]+\)/g, '$1')
    .replace(/`/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function likelyFilesForAudit(auditId, auditTitle) {
  const haystack = `${auditId} ${auditTitle}`;
  const matched = auditFileMap.find((entry) => entry.match.test(haystack));

  if (!matched) {
    return {
      files: [
        'platform/src/pages/index.astro',
        'platform/src/pages/lessons/[slug].astro',
        'platform/src/styles/global.css',
      ],
      recommendation: 'Inspect the Lighthouse HTML report for exact node/URL evidence, then update the nearest Astro page or shared style/config file.',
    };
  }

  return matched;
}

function collectFindings(report, profile) {
  return Object.entries(report.audits || {})
    .flatMap(([id, audit]) => {
      const value = auditScore(audit);
      if (value === 'n/a') return [];
      if (value >= 100) return [];

      const mapping = likelyFilesForAudit(id, audit.title);
      return [
        {
          profile,
          id,
          title: audit.title,
          score: value,
          severity: severity(value),
          displayValue: audit.displayValue || '',
          description: stripMarkdownLinks(audit.description || ''),
          files: mapping.files,
          recommendation: mapping.recommendation,
        },
      ];
    })
    .sort((a, b) => {
      const order = { high: 0, medium: 1, low: 2, info: 3, pass: 4 };
      return order[a.severity] - order[b.severity] || a.score - b.score;
    });
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
  lines.push('');

  const allFindings = reports.flatMap(({ profile, report }) => collectFindings(report, profile));
  const visibleFindings = allFindings.filter((finding) => finding.severity !== 'pass');

  lines.push('## Detailed recommendations by likely files', '');

  if (visibleFindings.length === 0) {
    lines.push('No non-perfect Lighthouse audits were found in JSON reports. Keep monitoring as pages become more interactive.');
  } else {
    lines.push('| Severity | Profile | Audit | Score | Likely files | Recommendation |');
    lines.push('|---|---|---|---:|---|---|');

    for (const finding of visibleFindings.slice(0, 20)) {
      const files = finding.files.map((file) => `\`${file}\``).join('<br>');
      const title = `${finding.title}${finding.displayValue ? ` (${finding.displayValue})` : ''}`;
      lines.push(
        `| ${finding.severity} | ${finding.profile} | ${title} | ${finding.score} | ${files} | ${finding.recommendation} |`,
      );
    }

    lines.push('', '## Top audit explanations', '');
    for (const finding of visibleFindings.slice(0, 10)) {
      lines.push(`### ${finding.profile}: ${finding.title}`);
      lines.push('');
      lines.push(`- Score: ${finding.score}`);
      if (finding.displayValue) lines.push(`- Display value: ${finding.displayValue}`);
      lines.push(`- Lighthouse audit id: \`${finding.id}\``);
      if (finding.description) lines.push(`- Why it matters: ${finding.description}`);
      lines.push(`- Recommended files: ${finding.files.map((file) => `\`${file}\``).join(', ')}`);
      lines.push(`- Suggested action: ${finding.recommendation}`);
      lines.push('');
    }
  }

  lines.push('## Next engineering actions', '');
  lines.push('1. If SEO is below 100, add per-page title/description, canonical URL, Open Graph, sitemap, and robots.txt.');
  lines.push('2. If Best Practices is below 100, inspect the HTML report for exact audit IDs and fix deployment/security/runtime details.');
  lines.push('3. If Performance drops, remove unused client JavaScript and keep Astro pages static until React islands are needed.');
  lines.push('4. If Accessibility drops, improve focus states, aria-labels, contrast, and mobile navigation semantics.');

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

fs.mkdirSync(resultsDir, { recursive: true });
fs.writeFileSync(recommendationReportPath, markdown);

if (summaryFile) {
  fs.appendFileSync(summaryFile, markdown);
}
