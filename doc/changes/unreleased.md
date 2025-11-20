# Unreleased

## Summary

In this release, the nox sessions `project:fix` and `project:format` have been modified
to include removing unused imports via ruff. To avoid unexpected changes, please add
the ruff configuration to your `pyproject.toml` as specified on
[Formatting Code Configuration](https://exasol.github.io/python-toolbox/main/user_guide/features/formatting_code/index.html#configuration)
page.

Additionally, `isort` has been updated from `^6.0.0` to `^7.0.0`. In 7.x, `isort` has
provided fixes for Python 3.14.

## Documentation

* #589: Corrected configuration for Sonar documentation for host.url
* #535: Added more information about Sonar's usage of ``exclusions``
* #596: Corrected and added more information regarding ``pyupgrade``

## Features

* #595: Created class `ResolvedVulnerabilities` to track resolved vulnerabilities between versions
* #544: Modified nox sessions `project:fix` and `project:format` to use ruff to remove unused imports

## Refactoring

* #596: Added newline after header in versioned changelog
