# 10.4.0 - 2026-07-27

## Summary

This minor release adds SPDX software bill of materials generation to
`build-and-publish.yml` through the new `dependency:sbom` Nox session and
updates the active `actions/checkout` references from v6 to v7. The new
version blocks checking out fork pull requests in privileged
`pull_request_target` and `workflow_run` workflows as a security improvement;
see the [v7 release notes](https://github.com/actions/checkout/releases/tag/v7).

## Features

* #905: Added SPDX SBOM generation to the `build-and-publish.yml` with the new Nox session `dependency:sbom`

## Refactoring

* #932: Updated active `actions/checkout` references from v6 to v7 in workflows, templates, documentation, and tests

## Dependency Updates

### `main`

* Added dependency `cyclonedx-bom:7.3.0`
* Added dependency `sbomconvert:0.1.0`
