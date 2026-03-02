# Unreleased

## Summary

This release changes the semantics of field `PROJECT_CONFIG.add_to_excluded_python_paths`. Before, this was a string making PTB ignore each file with this string in its path.

With this release, an arbitrary path in `PROJECT_CONFIG.add_to_excluded_python_paths` will make PTB ignore only files below this path interpreted relative to the project root.

Please see the user guide for details.

## Features

* #697: Supported multi-part paths in `add_to_excluded_python_paths`

## Refactoring

* #728: Updated to latest PTB workflows and added `.workflow-patcher.yml`
