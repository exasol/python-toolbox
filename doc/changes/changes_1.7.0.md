# 1.7.0 - 2025-07-28

## Summary

This version of the PTB alters the nox session `release:prepare` to include direct dependency changes between the current and latest tag (based on the `poetry.lock` files).
This benefits developers by automating the cumbersome process of determining what changed between tags, and it does so
in a deterministic and consistent way. If there are dependency changes, then they will be rendered
as:

```markdown
## Dependency Updates

### `main`
* Updated dependency `package_1:0.0.1` to `0.1.0`

### `dev`
* Added dependency `package_2:0.2.0`
```

## Documentation

* #504: Removed Issue Tracking & Style Guides, moved & updated "Create a release", moved & updated "Collecting metrics"

## Feature

* #382: Added onto nox session `release:prepare` to append dependency changes between current and latest tag

## Refactoring

* #498: Centralized changelog code relevant for `release:trigger` & robustly tested

## Dependency Updates

### `main`
* Updated dependency `furo:2024.8.6` to `2025.7.19`
* Updated dependency `mypy:1.16.1` to `1.17.0`
* Updated dependency `shibuya:2025.5.30` to `2025.7.14`
