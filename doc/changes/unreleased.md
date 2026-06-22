# Unreleased

## Summary

In this major release, several modifications were made to the PTB's workflow templates and actions:

* the nox DB-version default was updated to come from `BaseConfig` instead of the
  hardcoded `7.1.9`, so ITDE-related test flows use the configured Exasol baseline
  and unit-test help no longer advertises `--db-version`.
* the `github_template_dict.custom_workflows` entry now auto-detects secret names
  from custom workflow files and passes them into PTB-controlled workflow templates.
  For example:

  ```yaml
  on:
    workflow_call:
      secrets:
        PYPI_TOKEN:
          required: true
        SONAR_TOKEN:
          required: true
  ```
* the Python environment GitHub action now accepts `extras` as a comma-separated
  list, which makes it easier to pass multiple optional dependency groups in one
  value. Additionally, it supports `all-extras`, so that all extras are installed
  without further specification needed.

## Feature

* #874: Added the `security` label to dependency update PR creation
* #699: Added `all-extras` support to the Python environment GitHub action

## Bug

* #744: Updated nox DB-version handling to use `BaseConfig.minimum_exasol_version` instead hardcoded `7.1.9`

## Feature

* #878: Added Nox session `workflow:audit` which uses `zizmor` and added it in `checks.yml`
* #872: Added `custom_workflows` to `github_template_dict` for automatic custom workflow secret extraction

## Refactoring

* #744: Extracted shared minimum-version selection logic into `minimum_declared_version()`
* #699: Switched `extras` in the Python environment GitHub action to comma-separation

## Security

* #867: Fixed zizmor linting results
