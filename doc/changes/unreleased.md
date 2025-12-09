# Unreleased

This major release removes `project:fix` and `project:format`
and replaces them with `format:fix` and `format:check`.

## Refactoring

* #606: Renamed nox session `project:fix` more aptly to `format:fix` and `project:format` to `format:check`
* #604: Updated `BaseConfig.exasol_versions` to `("7.1.30", "8.29.13", "2025.1.8")`

## Feature

* #614: Replaced `path_filters` with `BaseConfig.add_to_excluded_python_paths` and `BaseConfig.excluded_python_paths`
