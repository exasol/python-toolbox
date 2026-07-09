# 10.2.0 - 2026-07-07

## Summary

This minor release adds automated vulnerability updates through Nox session
`vulnerabilities:update` and improves the `dependency-update.yml`. It also includes a
few workflow-related bug fixes and documentation updates.

## Bug Fix

* #909: Updated `cd.yml` workflow so that `cd-extension.yml` workflow depends on `build-and-publish`. This ensures that the custom release workflow only runs when the PyPi release was successful.
* #910: Added `gh-pages.yml` to be ignored when `has_documentation=False` in the `PROJECT_CONFIG`

## Feature

* #898: Created Nox session `vulnerabilities:update` to automatically resolve
  vulnerable dependencies and report the result for the dependency update workflow

## Dependency Updates

### `main`

* Updated dependency `coverage:7.14.3` to `7.15.0`
* Updated dependency `typer:0.26.7` to `0.26.8`
