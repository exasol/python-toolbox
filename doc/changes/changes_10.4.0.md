# 10.4.0 - 2026-07-27

## Summary

This minor release adds SPDX software bill of materials generation to
`build-and-publish.yml` through the new `dependency:sbom` Nox session.

## Features

* #905: Added SPDX SBOM generation to the `build-and-publish.yml` with the new Nox session `dependency:sbom`

## Dependency Updates

### `main`

* Added dependency `cyclonedx-bom:7.3.0`
* Added dependency `sbomconvert:0.1.0`
