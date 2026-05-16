module.exports = {
  ci: {
    collect: {
      staticDistDir: './dist',
      url: ['/'],
      numberOfRuns: 1,
      settings: {
        throttlingMethod: 'simulate',
        maxWaitForLoad: 30000,
        chromeFlags: '--no-sandbox --disable-dev-shm-usage',
      },
    },
    assert: {
      assertions: {
        'categories:performance': ['warn', { minScore: 0.8 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['warn', { minScore: 0.9 }],
        'categories:seo': ['warn', { minScore: 0.9 }],
        'uses-responsive-images': 'off',
        'unused-javascript': 'off',
      },
    },
    upload: {
      target: 'filesystem',
      outputDir: './lighthouse-results/mobile',
    },
  },
};
