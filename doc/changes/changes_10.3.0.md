# 10.3.0 - 2026-07-15

## Summary

This minor release extends automatic custom workflow permission extraction for
`github_template_dict.custom_workflows` and removes the deprecated
`lint:dependencies` usage from `report.yml` while adding a deprecation notice.
The `lint:dependencies` will be removed in October 2026.

## Features

* #922: Extended `custom_workflows` of `github_template_dict` for automatic custom workflow permissions extraction

## Refactoring

* #924: Removed `lint:dependencies` usage from `report.yml` and added deprecation notice
