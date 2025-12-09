# Unreleased

This major release removes `project:fix` and `project:format`
and replaces them with `format:fix` and `format:check`.

## Refactoring

* #606: Renamed nox session `project:fix` more aptly to `format:fix` and `project:format` to `format:check`

## Feature

* #614: Replaced `path_filters` with `BaseConfig.add_to_excluded_python_paths` and `BaseConfig.excluded_python_paths`
* #626: Replaced `plugins` with `BaseConfig.plugins_for_nox_sessions`
