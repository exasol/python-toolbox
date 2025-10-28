# 1.11.0 - 2025-10-28

With the addition of the nox session `package:check`, it's recommended to
switch a README.md to README.rst. The underlying package `twine` which is used
in that check performs more checks for rst files.

## Feature

* #494: Created check of built packages with nox session `package:check`

## Refactoring

* #578: Updated GitHub actions which now use node 24:
   * actions/checkout to [v5](https://github.com/actions/checkout/releases/tag/v5.0.0)
   * actions/download-artifact to [v6](https://github.com/actions/download-artifact/releases/tag/v6.0.0)
   * actions/upload-artifact to [v5](https://github.com/actions/upload-artifact/releases/tag/v5.0.0)

## Security

* #578: Resolved CVE-2024-12797 for cryptography and CVE-2025-8869 for pip by updating the lock file

## Dependency Updates

### `main`
* Updated dependency `black:25.1.0` to `25.9.0`
* Updated dependency `coverage:7.10.6` to `7.11.0`
* Updated dependency `furo:2025.7.19` to `2025.9.25`
* Updated dependency `import-linter:2.4` to `2.5.2`
* Updated dependency `isort:6.0.1` to `6.1.0`
* Updated dependency `mypy:1.17.1` to `1.18.2`
* Updated dependency `nox:2025.5.1` to `2025.10.16`
* Updated dependency `pip-licenses:5.0.0` to `5.5.0`
* Updated dependency `pydantic:2.11.7` to `2.12.3`
* Updated dependency `pylint:3.3.8` to `4.0.2`
* Updated dependency `pysonar:1.1.0.2035` to `1.2.0.2419`
* Updated dependency `pytest:8.4.1` to `8.4.2`
* Updated dependency `pyupgrade:3.20.0` to `3.21.0`
* Updated dependency `shibuya:2025.8.16` to `2025.10.21`
* Added dependency `twine:6.2.0`
* Updated dependency `typer:0.17.3` to `0.20.0`
