# Unreleased

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
