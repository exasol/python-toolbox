# Unreleased

## Features

* #940: Added shared validation for packaged agent skills and the `skills:check` Nox session.
* #938: Added the `skills:install` Nox session for installing the packaged PTB agent skill.
* #942: Added api-contract-audit skill for identifying mismatches between type annotations, docstrings, and runtime
  behavior
* #963: Extended packaged skill checks and installation to support multiple skills.

## Refactoring

* #924: Removed the deprecated `lint:dependencies` Nox session and its unused implementation and tests.
* #972: Switched from ravsamhq/notify-slack-action to maintained slackapi/slack-github-action & removed workflow versioned header
* #967: Refactored skill installation into reusable filesystem helpers.
