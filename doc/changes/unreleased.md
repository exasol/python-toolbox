# Unreleased

## Summary

In this major release, we:

* Dropped the Nox sessions `test:coverage` and `project:check`
* Modified the Nox sessions `test:unit` and `test:integration` to accept one or more
  files or directories via `--paths`
* Raised the minimum supported Python version from 3.11 to 3.11.5, as later versions of
  `soupsieve` no longer support earlier patch releases and the vulnerability in
  `soupsieve` for Python 3.11 could not otherwise be resolved.

## Refactoring

* #998: Raised `requires-python` to `>=3.11.5,<4.0`
* #939:
   * Removed Nox session `test:coverage`
   * Removed Nox session `project:check`
   * Modified Nox sessions `test:unit` and `test:integration` to accept one or more files or directories via `--paths`, overriding the default test directory
