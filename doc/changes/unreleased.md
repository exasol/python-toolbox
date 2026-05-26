# Unreleased

## Summary

## Bugfix

* #840: Added `export` plugin installation within `dependency-update.yml`
* Use hashed `poetry export` output with `pip-audit --disable-pip` to avoid the
  copied-interpreter failure in Poetry-managed Python builds

## Feature

* #722: Added check in `workflow:generate` to compare the generated and existing content before writing out

## Refactoring

* #722: Modified `workflow:generate` backend function to class `WorkflowOrchestrator`
