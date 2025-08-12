# Unreleased

With the refactoring of the `dependency:audit`, we use `poetry export`. For how it can
be added (project-specific or globally), see the
[poetry export documentation](https://github.com/python-poetry/poetry-plugin-export).

## Feature

* #469: Moved manual approval for slow tests to merge-gate.yml
* #544: Added ruff to `project:fix` and `project:format` for handling unused imports

## Refactoring

* #517: Refactored `dependency:audit` & split up to support upcoming work

## Documentation

* #544: Added documentation on code formatting nox sessions (i.e. `project:fix`, `project:format`)

## Bugfix

* #533: Fixed project-template tests to run with unreleased PTB to better detect issues pre-release
