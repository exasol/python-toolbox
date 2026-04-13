# Unreleased

## Summary

This release includes an update of `action/upload-pages-artifact` from v4 to v5. With this
change, now all actions used in the PTB run with Node.js 24. This is important as support
for Node.js 20 reaches it end-of-life in April of 2026 and support for it in GitHub will end in
September 2026; for more details, see GitHub's [deprecation notice](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/).

## Refactoring

* #764: Updated `action/upload-pages-artifact` from v4 to [v5](https://github.com/actions/upload-pages-artifact/releases/tag/v5.0.0)
