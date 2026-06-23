# 10.0.0 - 2026-06-23

## Summary

In this major release, several modifications were made to the PTB's workflow templates and actions:

* the default DB-version was updated to come from `BaseConfig` instead of the
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
* the new `workflow:audit` Nox session runs `zizmor` against GitHub Actions and
  reusable workflows, so security checks are part of the normal `checks.yml`
  pipeline instead of being a separate manual step. It also keeps the audit
  configuration in the project root via `.zizmor.yml`; see the
  [zizmor configuration guide](https://exasol.github.io/python-toolbox/main/user_guide/features/managing_dependencies/zizmor_configuration.html)
  and the
  [troubleshooting guide for findings](https://exasol.github.io/python-toolbox/main/user_guide/troubleshooting/handle_zizmor_findings.html)
  for details on tuning or suppressing findings locally.

## Security Issues

This release fixes vulnerabilities by updating dependencies:

| Dependency   | Vulnerability       | Affected | Fixed in |
|--------------|---------------------|----------|----------|
| cryptography | GHSA-537c-gmf6-5ccf | 48.0.0   | 48.0.1   |
| msgpack      | GHSA-6v7p-g79w-8964 | 1.1.2    | 1.2.1    |

## Feature

* #874: Added the `security` label to dependency update PR creation
* #699: Added `all-extras` support to the Python environment GitHub action
* #875: Added `name` attribute to generated workflow jobs using `-extension.yml` workflows

## Bug

* #744: Updated nox DB-version handling to use `BaseConfig.minimum_exasol_version` instead hardcoded `7.1.9`

## Feature

* #878: Added Nox session `workflow:audit` which uses `zizmor` and added it in `checks.yml`
* #872: Added `custom_workflows` to `github_template_dict` for automatic custom workflow secret extraction

## Refactoring

* #744: Extracted shared minimum-version selection logic into `minimum_declared_version()`
* #699: Switched `extras` in the Python environment GitHub action to comma-separation

## Documentation

* #828: Removed the legacy migration page and merged the useful guidance into getting started
* #789: Consolidated the metrics and Sonar documentation to reflect the current PTB reporting flow

## Security

* #867: Fixed zizmor linting results

## Dependency Updates

### `main`

* Updated dependency `coverage:7.14.1` to `7.14.3`
* Updated dependency `import-linter:2.11` to `2.12`
* Updated dependency `pip-audit:2.10.0` to `2.10.1`
* Updated dependency `pylint:4.0.5` to `4.0.6`
* Updated dependency `pytest:9.0.3` to `9.1.1`
* Updated dependency `zizmor:1.25.2` to `1.26.1`