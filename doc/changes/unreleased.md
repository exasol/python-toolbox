# Unreleased

## Summary

In this minor release, the nox session `workflow:check` was added and is now used in the `checks.yml`.
If this job is active in your CI, please double-check if additional files should be added into your project's `.gitattributes`.

## Bugfix

* #840: Added `export` plugin installation within `dependency-update.yml`

## Feature

* #722: Added check in `workflow:generate` to compare the generated and existing content before writing out and nox session `workflow:check`
* #642: Added nox session `workflow:check` into the `checks.yml`

## Refactoring

* #722: Modified `workflow:generate` backend function to class `WorkflowOrchestrator`
