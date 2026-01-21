# Unreleased

## Summary

In exasol-toolbox version `5.0.0` and higher the default behavior for
`.github/actions/python-environment/action.yml` has changed. In previous versions,
the default value for `poetry-version` was `2.1.2`, and it is now `2.3.0`.

* Depending on its poetry version, a repository relying on the default behavior of said
action may run into breaking changes. This can easily be resolved with explicitly setting the
`poetry-version` when calling the GitHub action. It is, however, recommended whenever
possible to update the poetry version of the affected repository. Unfortunately,
there is not a quick and easy way to update all the places where `poetry-version`
could be specified in the GitHub workflows.

* Projects migrating to this version should:

* Update their `pyproject.toml` to have:
    ```toml
    requires-poetry = ">=2.3.0"
    ```
* Run `poetry check` and resolve any issues
* (optional) Run `poetry lock` to update the  lock
* (optional) Update their `pyproject.toml` to fit:
   * [PEP-621](https://peps.python.org/pep-0621/)
   * [PEP-735](https://peps.python.org/pep-0735/)

Note that [uvx migrate-to-uv](https://github.com/mkniewallner/migrate-to-uv) seems to
do a good job with automating many of the PEP-related changes; though developers should
take care and will need to make manual changes to ensure it still works with
`poetry`, as the PTB does not yet support `uv`.

## Documentation

* #648: Moved sonar setup instructions in the User guide

## Features

* #649: Restricted noxconfig usage throughout exasol.toolbox to only exasol.toolbox.nox.*
* #647: Added summary to changelog template
* #657: Updated `release:prepare` to modify cookiecutter template exasol-toolbox version range

## Refactoring

* #624: Updated GitHub python-environment action and all code to use Poetry >= 2.3.0
* #662: Update GitHub actions checkout from v5 to [v6](https://github.com/actions/checkout/releases/tag/v6.0.0)
