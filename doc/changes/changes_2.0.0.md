# 2.0.0 - 2025-11-04

With this release, all projects using the PTB must use has their project `Config` inherit
from `BaseConfig` (introduced in [1.10.0](https://exasol.github.io/python-toolbox/main/changes/changes_1.10.0.html)). Otherwise, the workflows using these
attributes will raise an exception indicating that this action is needed.

As Python 3.9 reached its EOL on 2025-10-31, the PTB no longer supports Python 3.9,
and it has added support for 3.14. For project's that were still using Python 3.9,
it is anticipated that there will be larger formatting change due to the arguments
to `pyupgrade` changing.

## Refactoring

* #590:
   * Dropped support for Python 3.9 and added support for Python 3.14
   * Enforced that the `PROJECT_CONFIG` defined in `noxconfig.py` must be derived from `BaseConfig`.
     * Replaced `MINIMUM_PYTHON_VERSION` which acted as a back-up value for the nox session `artifacts:copy`
     with `BaseConfig.minimum_python_version_`
     * Replaced `_PYTHON_VERSIONS` which acted as a back-up value for the nox sessions `matrix:python` and `matrix:all`
     with  `BaseConfig.python_versions_`
     * Replaced `__EXASOL_VERSIONS` which acted as a back-up value for the nox sessions `matrix:exasol` and `matrix:all`
     with `BaseConfig.python_versions_`
     * Moved `pyupgrade_args` from being defined per PROJECT_CONFIG to a calculated property
     `BaseConfig.pyupgrade_argument_`

## Dependency Updates

### `main`
* Updated dependency `pysonar:1.2.0.2419` to `1.2.1.3951`
* Updated dependency `shibuya:2025.10.21` to `2025.11.4`
