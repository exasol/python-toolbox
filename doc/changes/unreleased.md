# Unreleased

## Summary

Updated the nox DB-version default to come from `BaseConfig` instead of the hardcoded `7.1.9`,
so ITDE-related test flows use the configured Exasol baseline and unit-test help no longer advertises `--db-version`.

## Feature

* #874: Added the `security` label and `Integration Kanban` project to dependency update PR creation

## Bug

* #744: Updated nox DB-version handling to use `BaseConfig.minimum_exasol_version` instead hardcoded `7.1.9`

## Refactoring

* #744: Extracted shared minimum-version selection logic into `minimum_declared_version()`
## Security

* #867: Fixed zizmor linting results
