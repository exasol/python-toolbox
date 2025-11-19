# Unreleased

## Documentation

* #589: Corrected configuration for Sonar documentation for host.url
* #535: Added more information about Sonar's usage of ``exclusions``
* #596: Corrected and added more information regarding ``pyupgrade``

## Features

* #595: Created class `ResolvedVulnerabilities` to track resolved vulnerabilities between versions
* #544: Modified nox sessions `project:fix` and `project:format` to use ruff to remove unused imports

## Refactoring

* #596: Added newline after header in versioned changelog
