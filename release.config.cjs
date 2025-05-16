/**
 * @type {import('semantic-release').GlobalConfig}
 */

module.exports = {
    branches: ["master",
      {
        channel: 'alpha',
        name: "*alpha*",
        prerelease: true
      }, 
      {
        channel: 'beta',
        name: "*beta*",
        prerelease: true
      }
    ],
    plugins: [
      [
        "@semantic-release/commit-analyzer",
        {
          preset: "angular",
          releaseRules: [
            {
              breaking: true,
              release: "major",
            },
            {
              type: "feat",
              release: "minor",
            },
            {
              type: "fix",
              release: "patch",
            },
            {
              type: "docs",
              scope: "README",
              release: "patch",
            },
            {
              type: "chore",
              release: "patch",
            },
            {
              type: "perf",
              release: "patch",
            },
            {
              type: "style",
              release: "patch",
            },
            {
              type: "refactor",
              release: "patch",
            },
            {
              type: "test",
              release: "patch",
            },
            {
              type: "build",
              release: "patch",
            },
            {
              type: "ci",
              release: "patch",
            }
          ],
          parserOpts: {
            noteKeywords: ["BREAKING CHANGE", "BREAKING CHANGES", "BREAKING"],
            headerPattern: /^(:\w*:)?\s*(\w*)(?:\((.*)\))?\: (.*)$/,
            headerCorrespondence: ["emoji", "type", "scope", "subject"],
          },
        },
      ],
      [
        "@semantic-release/release-notes-generator",
        {
          preset: "conventionalcommits",
          presetConfig: {
            types: [
              { type: "feat", section: "✨ Features", hidden: false },
              { type: "fix", section: "🐛 Bug Fixes", hidden: false },
              { type: "docs", section: "📚 Documentation", hidden: false },
              { type: "chore", section: "⚙️ Miscellaneous Chores", hidden: false },
              { type: "perf", section: "⚡ Improvements", hidden: false },
              { type: "style", section: "🎨 Styles", hidden: true },
              { type: "refactor", section: "♻️ Code Refactoring", hidden: true },
              { type: "test", section: "✅ Tests", hidden: true },
              { type: "build", section: "📦 Build System", hidden: true },
              { type: "ci", section: "👷 Continuous Integration", hidden: true },
            ],
          },
          parserOpts: {
            noteKeywords: ["BREAKING CHANGE", "BREAKING CHANGES", "BREAKING"],
            headerPattern: /^(:\w*:)?\s*(\w*)(?:\((.*)\))?\: (.*)$/,
            headerCorrespondence: ["emoji", "type", "scope", "subject"],
          },
        },
      ],
      [
        "@semantic-release/changelog",
        {
          changelogFile: "CHANGELOG.md",
          skipUnstable: true
        },
      ],
      [
        "@semantic-release/github",
        {
          "assets": [
            {
              "path": "dist/DBtective.exe",
              "label": "DBtective-${nextRelease.version}-windows-no-installer.exe"
            },
            // {
            //   "path": "dist/DBtective-linux", 
            //   "label": "DBtective-${nextRelease.version}-linux-no-installer"
            // },
            // {
            //   "path": "dist/DBtective-macos", 
            //   "label": "DBtective-${nextRelease.version}-macos-no-installer"
            // },
          ]
        }
      ],
      [
        "@semantic-release/git",
        {
          assets: ["package.json", "CHANGELOG.md"],
          message: ":gear: chore: Release ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
        },
      ],
    ],
  };