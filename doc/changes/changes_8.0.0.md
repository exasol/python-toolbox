# 8.0.0 - 2026-05-13

## Summary

In this major release, several modifications were made to the PTB's workflow templates:

* For automatically resolving vulnerabilities, the `dependency-update.yml` workflow was
added. For more details, see the [Update Dependencies](https://exasol.github.io/python-toolbox/main/user_guide/features/github_workflows/index.html#update-dependencies) section.
* The periodic run which was previously executed in the `ci.yml` has been moved to its
own `periodic-validation.yml` and will run weekly. This also has been modified to
run the `slow-checks.yml` so that more complete linting and coverage information is
sent to Sonar.
* With the addition of `periodic-validation.yml`, the `pr-merge.yml` was reduced so that
it only executes `gh-pages.yml`.
* The unit tests job has been moved from `checks.yml` to its own `fast-tests.yml` file.
* Workflow extensions were added to `fast-tests` and `merge-gate`. This allows users to
add custom `fast-tests-extension.yml` and `merge-gate-extension.yml` files. For more
details, check out the [Workflow Extensions](https://exasol.github.io/python-toolbox/main/user_guide/features/github_workflows/index.html#workflow-extensions) section.
* `slow-checks.yml` is only maintained by the project (not the PTB). See the [Not Maintained by the PTB](https://exasol.github.io/python-toolbox/main/user_guide/features/github_workflows/index.html#not-maintained-by-the-ptb) section.

## Features

* #829: Extended removing a job from a workflow to also remove it from the `needs` of another job
* #825: Created two workflows by splitting up previous ones:
   * Moved the periodic jobs in `ci.yml` to its own `periodic-validation.yml`
   * Moved the unit tests job in `checks.yml` to its own `fast-tests.yml`
* #730: Added workflow extensions to `fast-tests` and `merge-gate`
* #756: Added `dependency-update.yml` to automate resolving vulnerabilities with a generated pull request
* #792: Improved `dependency-update.yml` documentation
* #831: Switched `slow-checks.yml` to be provided by the project and not maintained by the PTB and improved output of pydantic validation of `.workflow-patcher.yml`

## Bugfix

* #563: Fixed merge-gate to prevent auto-merges from happening when integration tests failed

## Security Issues

This release fixes vulnerabilities by updating dependencies:

| Dependency | Vulnerability | Affected | Fixed in |
|------------|---------------|----------|----------|
| urllib3 | CVE-2026-44431 | 2.6.3 | 2.7.0 |
| urllib3 | CVE-2026-44432 | 2.6.3 | 2.7.0 |

* #836: Relocked `poetry.lock`

## Dependency Updates

### `main`

* Updated dependency `coverage:7.13.4` to `7.14.0`
* Updated dependency `importlib-resources:6.5.2` to `7.1.0`
* Updated dependency `mypy:1.19.1` to `2.1.0`
* Updated dependency `nox:2026.2.9` to `2026.4.10`
* Updated dependency `pip-licenses:5.5.1` to `5.5.5`
* Updated dependency `pre-commit:4.5.1` to `4.6.0`
* Updated dependency `pydantic:2.12.5` to `2.13.4`
* Updated dependency `pysonar:1.0.2.1722` to `1.5.0.4793`
* Updated dependency `sphinxcontrib-mermaid:2.0.1` to `2.0.2`
* Updated dependency `typer:0.24.1` to `0.25.1`

### `dev`

* Updated dependency `types-pyyaml:6.0.12.20250915` to `6.0.12.20260510`
