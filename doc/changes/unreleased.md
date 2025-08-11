# Unreleased

With the refactoring of the `dependency:audit`, we use `poetry export`. For how it can
be added (project-specific or globally), see the
[poetry export documentation](https://github.com/python-poetry/poetry-plugin-export).

## Feature

* #469: Moved manual approval for slow tests to merge-gate.yml

## Refactoring

* #517: Refactored `dependency:audit` & split up to support upcoming work
* Updated dependencies (removed unused `prysk`)

## Bugfix

* #533: Fixed project-template tests to run with unreleased PTB to better detect issues pre-release
