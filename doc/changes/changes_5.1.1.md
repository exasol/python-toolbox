# 5.1.1 - 2026-02-06

## Summary

In this patch release, we:

* Fixed a bug which was affecting new GitHub projects from using the nox session `release:prepare`.
* Switched from using a string verified by PyYaml to directly using ruamel-yaml for rendering the GitHub workflows.

## Bug

* #692: Fixed bug where creating first release failed due to no previous tags

## Documentation

* #585: Added instructions how to ignore sonar issues to the User Guide
* #630: Updated cookiecutter command to reduce errors experienced by users

## Refactoring

* #686: Switched GitHub templates to be fully parsed by ruamel-yaml

## Dependency Updates

### `main`
* Removed dependency `pyyaml:6.0.3`
* Added dependency `ruamel-yaml:0.18.16`
