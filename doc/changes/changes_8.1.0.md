# 8.1.0 - 2026-05-27

## Summary

In this minor release, the nox session `workflow:check` was added and is now used in the `checks.yml`.
If this job is active in your CI, please double-check if additional files should be added into your project's `.gitattributes`.

## Security Issues

This release fixes vulnerabilities by updating dependencies:

| Dependency | Vulnerability  | Affected | Fixed in |
|------------|----------------|----------|----------|
| idna       | CVE-2026-45409 | 3.14     | 3.15     |

## Bugfix

* #840: Added `export` plugin installation within `dependency-update.yml`
* #847: Used hashed `poetry export` output with `pip-audit --disable-pip` to avoid the
  copied-interpreter failure in Poetry-managed Python builds

## Feature

* #722: Added check in `workflow:generate` to compare the generated and existing content before writing out and nox session `workflow:check`
* #642: Added nox session `workflow:check` into the `checks.yml`
* #698: Added a comment in the top of all workflows maintained by the PTB

## Refactoring

* #722: Modified `workflow:generate` backend function to class `WorkflowOrchestrator`

## Dependency Updates

### `main`

* Updated dependency `black:26.3.1` to `26.5.1`
* Updated dependency `shibuya:2026.1.9` to `2026.5.19`

### `dev`

* Updated dependency `types-pyyaml:6.0.12.20260510` to `6.0.12.20260518`
