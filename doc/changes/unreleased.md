# Unreleased

## Summary

## Features

* #777: Improved VulnerabilityMatcher to handle packages with multiple vulnerabilities

## Refactoring

* #731: Reduced costly `test-python-environment.yml` to run when triggered on `main` or when the files related to the action are altered
* #785: Remove nox session `project:report` and metrics-schema, as superseded by Sonar usage
* #763: Parse and Manipulate Changes Files
