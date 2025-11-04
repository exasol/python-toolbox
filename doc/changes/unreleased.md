# Unreleased

With this release, all projects using the PTB must use the `BaseConfig` introduced
in [1.10.0](https://exasol.github.io/python-toolbox/main/changes/changes_1.10.0.html).

As Python 3.9 reached its EOL on 2025-10-31, the PTB no longer supports Python 3.9,
and it has added support for 3.14.

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
