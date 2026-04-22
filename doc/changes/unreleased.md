# Unreleased

## Summary

## Features

* #777: Improved VulnerabilityMatcher to handle packages with multiple vulnerabilities
* #517: Modified nox session `release:prepare` to report resolved security issues

## Refactoring

* #731: Reduced costly `test-python-environment.yml` to run when triggered on `main` or when the files related to the action are altered
* #785: Removed nox session `project:report` and metrics-schema, as superseded by Sonar usage
* #763: Parsed and manipulated Changes Files
* #788: Removed tbx workflow CLI commands, as superseded by nox session `workflow:generate`
* #800: Removed tbx security pretty-print, tbx lint pretty-print, and creation of .lint.txt, as superseded by Sonar and .lint.json usage

## Bugfix

* #798: Added test to ensure `tbx security cve` works
