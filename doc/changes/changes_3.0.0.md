# 3.0.0 - 2025-11-20

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

## Dependency Updates

### `main`
* Updated dependency `bandit:1.8.6` to `1.9.1`
* Updated dependency `black:25.9.0` to `25.11.0`
* Updated dependency `coverage:7.11.0` to `7.12.0`
* Updated dependency `import-linter:2.5.2` to `2.7`
* Updated dependency `isort:6.1.0` to `7.0.0`
* Updated dependency `nox:2025.10.16` to `2025.11.12`
* Updated dependency `pre-commit:4.3.0` to `4.4.0`
* Updated dependency `pydantic:2.12.3` to `2.12.4`
* Updated dependency `pylint:4.0.2` to `4.0.3`
* Updated dependency `pytest:8.4.2` to `9.0.1`
* Updated dependency `pyupgrade:3.21.0` to `3.21.2`
* Added dependency `ruff:0.14.5`
* Updated dependency `shibuya:2025.11.4` to `2025.11.10`
