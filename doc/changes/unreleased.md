# Unreleased

## Bugfixes

* #965: Added additional parameters to ``format:fix`` tools to run with the minimum Python version
* #983: Deduplicated vulnerable dependencies in Nox session ``release:prepare``

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
