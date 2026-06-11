# 8.2.0 - 2026-06-10

## Summary

This minor release adds manual triggering for `periodic-validation.yml` and makes the
Sonar secret name used by `report.yml` configurable via `BaseConfig`.

## Security Issues

This release fixes vulnerabilities by updating dependencies:

| Dependency | Vulnerability  | Affected | Fixed in |
|------------|----------------|----------|----------|
| pip        | PYSEC-2026-196 | 26.1.1   | 26.1.2   |

## Feature

* #854: Added `workflow_dispatch` for `periodic-validation.yml`
* #827: Modified `report.yml` to allow overriding the Sonar secret name via `BaseConfig`

## Refactoring

* #852: Modified `merge-gate` to ensure `run-fast-tests` succeeds
* #811: Modified workflow templates to not persist-credentials, not provide attacker-controllable inlines, and not pass more secrets to `report.yml`

## Dependency Updates

### `main`

* Updated dependency `coverage:7.14.0` to `7.14.1`
* Updated dependency `pysonar:1.5.0.4793` to `1.6.0.4905`
* Updated dependency `sphinx-toolbox:4.1.2` to `4.2.0`
* Updated dependency `typer:0.25.1` to `0.26.7`
