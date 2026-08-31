# 10.5.0 - 2026-08-31

## Summary

This release documents how to discover and use PTB's Nox sessions in the user
guide, adds an agent skill for PTB work, and removes the unused Modules section
from the developer guide.

## Security Issues

This release fixes vulnerabilities by updating dependencies:

| Dependency | Vulnerability | Affected | Fixed in |
|------------|---------------|----------|----------|
| cryptography | PYSEC-2026-3552 | 49.0.0 | 50.0.0 |
| pip | PYSEC-2026-3721 | 26.1.2 | 26.2 |

## Documentation

* #456: Documented how to discover PTB nox sessions in the user guide
* #933: Added an agent skill for PTB work

## Feature

* #946: Added project name and version context to SBOM file name

## Refactoring

* #934: Removed unused, experimental Nox session `lint:import`
* #952: Updated zizmor and GitHub Actions workflows to use GitHub's self-repository syntax

## Dependency Updates

### `main`

* Updated dependency `coverage:7.15.2` to `7.16.0`
* Removed dependency `import-linter:2.13`
* Updated dependency `mypy:2.3.0` to `2.3.1`
* Updated dependency `nox:2026.7.11` to `2026.8.17`
* Updated dependency `pre-commit:4.6.1` to `4.6.2`
* Updated dependency `pydantic:2.13.4` to `2.13.5`
* Updated dependency `pylint:4.0.6` to `4.0.8`
* Updated dependency `pysonar:1.7.0.5143` to `1.8.0.5390`
* Updated dependency `sphinx-toolbox:4.2.0` to `4.3.0`
* Updated dependency `typer:0.27.0` to `0.27.2`
* Updated dependency `zizmor:1.28.0` to `1.30.0`

### `dev`

* Updated dependency `types-pyyaml:6.0.12.20260724` to `6.0.12.20260815`
