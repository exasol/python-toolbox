# Unreleased

## Summary

This release documents how to discover and use PTB's Nox sessions in the user
guide and removes the unused Modules section from the developer guide.

## Documentation

* #456: Documented how to discover PTB nox sessions in the user guide and removed the unused developer-guide Modules section
## Bug

* #909: Updated `cd.yml` workflow so that `cd-extension.yml` workflow depends on `build-and-publish`. This ensures that the custom release workflow only runs when the PyPi release was successful.
* #910: Add `gh-pages.yml` to be ignored when `has_documentation=False` in the `PROJECT_CONFIG`
