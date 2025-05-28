# Unreleased

## Summary

With #441, please ensure that the location of the `version.py` is given for `Config.version_file`,
which is specified in the `noxconfig.py`

With #449, it's possible to customize what arguments are being using with `pyupgrade`
via the `noxconfig.Config`:
```python
pyupgrade_args = ("--py310-plus",)
```

## 📚 Documentation
* Updated getting_started.rst for allowing tag-based releases

## ✨ Features

* [#441](https://github.com/exasol/python-toolbox/issues/441): Switched nox task for `version:check` to use the config value of `version_file` to specify the location of the `version.py`
* [#451](https://github.com/exasol/python-toolbox/issues/451): Added Sonar to project for quality checks

## ⚒️ Refactorings

* [#449](https://github.com/exasol/python-toolbox/issues/449): Refactored `dependency:licenses`:
    * to use pydantic models & `poetry show` for dependencies
    * to updated reading the `pyproject.toml` to be compatible with poetry 2.x+