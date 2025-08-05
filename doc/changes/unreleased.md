# Unreleased

## Summary

With the refactoring of the `dependency:audit`, we use `poetry export`. For how it can
be added (project-specific or globally), see the
[poetry export documentation](https://github.com/python-poetry/poetry-plugin-export).

## Refactoring

* #525: Added tests for installing `pipx` on different GitHub runners
* #517: Refactored `dependency:audit` & split up to support upcoming work
