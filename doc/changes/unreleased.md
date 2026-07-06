# Unreleased

## Summary

This minor release adds automated vulnerability updates through Nox session
`vulnerabilities:update` and improves the `dependency-update.yml`. It also includes a
few workflow-related bug fixes and documentation updates.

## Bug

* #909: Updated `cd.yml` workflow so that `cd-extension.yml` workflow depends on `build-and-publish`. This ensures that the custom release workflow only runs when the PyPi release was successful.
* #910: Added `gh-pages.yml` to be ignored when `has_documentation=False` in the `PROJECT_CONFIG`

## Feature

* #898: Created Nox session `vulnerabilities:update` to automatically resolve
  vulnerable dependencies and report the result for the dependency update workflow
