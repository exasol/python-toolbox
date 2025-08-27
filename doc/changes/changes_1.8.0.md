# 1.8.0 - 2025-08-14
With the refactoring of the `dependency:audit`, we use `poetry export`. For how it can
be added (project-specific or globally), see the
[poetry export documentation](https://github.com/python-poetry/poetry-plugin-export).

Within the `report.yml`, the `actions/download-artifact@v4.2.1` was upgraded to
`v5.0.0`. This upgrade should not affect the existing functionality of the standard
GitHub workflows from the PTB. However, there are breaking changes that affect cases
where artifacts are downloaded by ID. For further details, please see the
[release notes for 5.0.0](https://github.com/actions/download-artifact/releases/tag/v5.0.0).

## Feature

* #469: Moved manual approval for slow tests to merge-gate.yml

## Refactoring

* #517: Refactored `dependency:audit` & split up to support upcoming work
* #541: Refactored test code using `prysk` and removed `prysk` as a dependency

## Bugfix

* #533: Fixed project-template tests to run with unreleased PTB to better detect issues pre-release

## Dependency Updates

### `main`
* Updated dependency `coverage:7.10.1` to `7.10.3`
* Updated dependency `mypy:1.17.0` to `1.17.1`
* Updated dependency `pre-commit:4.2.0` to `4.3.0`
* Removed dependency `prysk:0.20.0`
* Updated dependency `pylint:3.3.7` to `3.3.8`
* Updated dependency `pytest:7.4.4` to `8.4.1`
