# Unreleased

## Summary

In exasol-toolbox version `5.0.0` and higher the default behavior for
`.github/actions/python-environment/action.yml` has changed. In previous versions,
the default value for `poetry-version` was `2.1.2`, and it is now `2.3.0`.

* Depending on its poetry version, a repository relying on the default behavior of said
action may run into breaking changes. This can easily be resolved with explicitly setting the
`poetry-version` when calling the GitHub action. It is, however, recommended whenever
possible to update the poetry version of the affected repository. In this major release,
you can, if needed, alter the `poetry-version` via the `noxconfig.py::PROJECT_CONFIG`
by changing `dependency_manager_version`. If you do this, please create an issue to
update to `2.3.0` at your earliest convenience.

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
* #667: Switched GitHub workflow templates to be controlled by PROJECT_CONFIG:
   * The in `BaseConfig.github_template_dict` are used to render the following values in
     the templates
      * `dependency_manager_version` - used for `poetry-version` in the workflows.
         The default it `2.3.0`.
      * `minimum_python_version` - used for `python-version` in the workflows whenever
         `python-version` for actions that are run once. The default is the minimum value
         in your project's defined `python_versions`
      * `os_version` - used for the GitHub runner in the workflows. The default is
         `ubuntu-24.04`

## Refactoring

* 624: Updated GitHub python-environment action and all code to use Poetry >= 2.3.0
