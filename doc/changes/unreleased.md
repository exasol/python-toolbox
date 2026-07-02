# Unreleased

## Summary

## Bug

* #909: Updated `cd.yml` workflow so that `cd-extension.yml` workflow depends on `build-and-publish`. This ensures that the custom release workflow only runs when the PyPi release was successful.
* #910: Add `gh-pages.yml` to be ignored when `has_documentation=False` in the `PROJECT_CONFIG`
