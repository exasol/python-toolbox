# 12.0.0 - 2026-10-26

## Summary

This major release removes support for Python 3.10 and adds Nox sessions for
validating and installing packaged agent skills. It also extends those sessions to
support multiple skills and updates the GitHub Actions environment to Ubuntu 26.04.

## Bugfixes

* #965: Added additional parameters to ``format:fix`` tools to run with the minimum Python version
* #983: Deduplicated vulnerable dependencies in Nox session ``release:prepare``

## Security Issues

This release fixes vulnerabilities by updating dependencies:

| Dependency | Vulnerability   | Affected  | Fixed in   |
|------------|-----------------|-----------|------------|
| black      | CVE-2026-114134 | 26.5.1    | 26.10.1    |
| certifi    | PYSEC-2026-4320 | 2026.7.22 | 2026.10.19 |
| filelock   | CVE-2026-112907 | 3.32.6    | 4.2.1      |
| filelock   | CVE-2026-112913 | 3.32.6    | 4.2.1      |
| filelock   | CVE-2026-112940 | 3.32.6    | 4.2.1      |
| urllib3    | PYSEC-2026-4175 | 2.7.0     | 2.8.0      |
| urllib3    | PYSEC-2026-4176 | 2.7.0     | 2.8.0      |
| urllib3    | PYSEC-2026-4177 | 2.7.0     | 2.8.0      |
| virtualenv | CVE-2026-113714 | 21.7.9    | 21.14.9    |
| virtualenv | CVE-2026-113715 | 21.7.9    | 21.14.9    |
| virtualenv | CVE-2026-113717 | 21.7.9    | 21.14.9    |
| virtualenv | CVE-2026-113718 | 21.7.9    | 21.14.9    |
| virtualenv | CVE-2026-113720 | 21.7.9    | 21.14.9    |
| virtualenv | CVE-2026-113722 | 21.7.9    | 21.14.9    |
| virtualenv | CVE-2026-113723 | 21.7.9    | 21.14.9    |
| virtualenv | CVE-2026-113725 | 21.7.9    | 21.14.7    |
| virtualenv | CVE-2026-113726 | 21.7.9    | 21.14.4    |
| virtualenv | CVE-2026-113732 | 21.7.9    | 21.14.2    |
| virtualenv | CVE-2026-113776 | 21.7.9    | 21.14.2    |
| virtualenv | PYSEC-2026-4011 | 21.7.9    | 21.7.12    |
| virtualenv | PYSEC-2026-4012 | 21.7.9    | 21.7.11    |
| virtualenv | PYSEC-2026-4013 | 21.7.9    | 21.7.13    |
| virtualenv | PYSEC-2026-4014 | 21.7.9    | 21.7.12    |

## Features

* #940: Added shared validation for packaged agent skills and the `skills:check` Nox session.
* #938: Added the `skills:install` Nox session for installing the packaged PTB agent skill.
* #942: Added api-contract-audit skill for identifying mismatches between type annotations, docstrings, and runtime behavior
* #963: Extended packaged skill checks and installation to support multiple skills.
* #978: Updated template `doc/conf.py`

## Refactoring

* #924: Removed the deprecated `lint:dependencies` Nox session and its unused implementation and tests.
* #972: Switched from ravsamhq/notify-slack-action to maintained slackapi/slack-github-action & removed workflow versioned header
* #967: Refactored skill installation into reusable filesystem helpers.
* #965: Removed support for Python 3.10 (reach end-of-life October 2026), updated to Ubuntu-26.04 for GitHub actions, and updated default databases

## Dependency Updates

### `main`

* Updated dependency `black:26.5.1` to `26.10.1`
* Updated dependency `coverage:7.16.1` to `7.17.0`
* Updated dependency `cyclonedx-bom:7.3.1` to `7.5.0`
* Updated dependency `mypy:2.3.1` to `2.4.0`
* Updated dependency `nox:2026.8.17` to `2026.10.20`
* Updated dependency `pluggy:1.6.0` to `1.7.0`
* Updated dependency `pre-commit:4.6.2` to `4.7.0`
* Updated dependency `pydantic:2.13.5` to `2.14.1`
* Updated dependency `pylint:4.0.8` to `4.1.3`
* Updated dependency `pysonar:1.8.0.5390` to `1.10.0.5888`
* Updated dependency `pyupgrade:3.21.2` to `3.22.0`
* Updated dependency `typer:0.27.2` to `0.27.3`
* Updated dependency `zizmor:1.30.1` to `1.31.1`
