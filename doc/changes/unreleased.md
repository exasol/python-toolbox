# Unreleased

## Summary

This release renamed some of the GitHub workflows which requires to update your branch protection. It needs to be `Checks / Allow Merge` in contrast to `merge-gate / Allow Merge` in the past.

This release also changes the semantics of field `PROJECT_CONFIG.add_to_excluded_python_paths`.

Before, a `.venv` directory would have be excluded no matter what parent directory structure it had. Now, only ROOT_PATH / `.venv` would be excluded. If you have multiple paths like `.venv` before, you will need to specifically specify them relative to the ROOT_PATH.

Please see the user guide for details.

## Features

* #697: Supported multi-part paths in `add_to_excluded_python_paths`

## Refactoring

* #728: Updated to latest PTB workflows and added `.workflow-patcher.yml`
* #736: Capitalized and shorten names of GitHub workflows
* #742: Renamed Workflows
