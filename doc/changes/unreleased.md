# Unreleased

## Summary

In this major release, several modifications were made to the PTB's workflow templates:

* The periodic run which was previously executed in the `ci.yml` has been moved to its
own `periodic-validation.yml` and will run weekly. This also has been modified to
run the `slow-checks.yml` so that more complete linting and coverage information is
sent to Sonar.
* With the addition of `periodic-validation.yml`, the `pr-merge.yml` was reduced so that
it only executes `gh-pages.yml`.
* The unit tests job has been moved from `checks.yml` to its own `fast-tests.yml` file.
* Workflow extensions were added to `fast-tests` and `merge-gate`. This allows users to
add custom `fast-tests-extension.yml` and `merge-gate-extension.yml` files. For more
details, check out LINK TO BE ADDED (DOES NOT EXIST YET).

## Bugfix

* #563: Fixed merge-gate to prevent auto-merges from happening when integration tests failed

## Feature

* #829: Extended removing a job from a workflow to also remove it from the `needs` of another job
* #825: Created two workflows by splitting up previous ones:
   * Moved the periodic jobs in `ci.yml` to its own `periodic-validation.yml`
   * Moved the unit tests job in `checks.yml` to its own `fast-tests.yml`
* #730: Added workflow extensions to `fast-tests` and `merge-gate`
