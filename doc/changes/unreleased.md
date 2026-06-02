# Unreleased

## Summary

## Feature

* #854: Added `workflow_dispatch` for `periodic-validation.yml`

## Refactoring

* #852: Modified `merge-gate` to ensure `run-fast-tests` succeeds
* #811: Modified workflow templates to not persist-credentials, not provide attacker-controllable inlines, and not pass more secrets to `report.yml`
