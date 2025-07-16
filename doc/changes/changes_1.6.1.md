# 1.6.1 - 2025-07-16

## Summary

This version of the PTB resolves many bugs associated with the cookiecutter template
and creating a new project that uses the PTB.

If any directories or files specified in your `noxconfig.py` via `Config.source` should
not be included in a Sonar analysis, it is recommended to add the following to
your `pyproject.toml` under the `[tool.sonar]` section:

```toml
exclusions = "<source-directory>/version.py,<source_directory>/<directory-to-ignore>/*"
```

## Bugfixes

* #489: Fixed .pre-commit-config.yaml to use existing nox tasks
* #490: Fixed artifacts:validate & sonar:check to work for newly created projects
* #484: Fixed hint command text in version.py to include -s for executing nox task

## Documentation

* #488: Updated user guide to make clearer under which conditions branch protections based on GitHub actions can be enacted

## Refactoring

* #482: Updated pull_request_template.md to reflect checks we should regularly perform
