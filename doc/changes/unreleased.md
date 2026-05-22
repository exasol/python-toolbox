# Unreleased

## Summary

In this minor release, the nox session `workflow:check` was added and is now used in the `checks.yml`.

## Bugfix

* #840: Added `export` plugin installation within `dependency-update.yml`

## Feature

* #722: Added check in `workflow:generate` to compare the generated and existing content before writing out, nox session `workflow:check`, and `workflow:check` into the `checks.yml`

## Refactoring

* #722: Modified `workflow:generate` backend function to class `WorkflowOrchestrator`
