# Unreleased

## Summary

In this major release, the nox DB-version default was updated to come from `BaseConfig` instead of the hardcoded `7.1.9`,
so ITDE-related test flows use the configured Exasol baseline and unit-test help no longer advertises `--db-version`.

## Feature

* #874: Added the `security` label to dependency update PR creation
* #699: Added `all-extras` support to the Python environment GitHub action

## Bug

* #744: Updated nox DB-version handling to use `BaseConfig.minimum_exasol_version` instead hardcoded `7.1.9`

## Feature

* #878: Added Nox session `workflow:audit` which uses `zizmor` and added it in `checks.yml`
* #872: Added `custom_workflow_secrets` to `BaseConfig` so that tuples of secrets can be defined for custom workflows, like `slow-checks.yml`

## Refactoring

* #744: Extracted shared minimum-version selection logic into `minimum_declared_version()`

## Security

* #867: Fixed zizmor linting results
