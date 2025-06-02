# 1.3.0 - 2025-06-02

## Summary

This version of the PTB updates nox task `version:check`, see #441. 
This requires file `noxconfig.py` of each project to specify the path to `version.py` in `Config.version_file`.

With this version of the PTB you can customize the arguments for `pyupgrade` in file `noxconfig.py`, see ticket #449 for details:
```python
pyupgrade_args = ("--py310-plus",)
```

## 📚 Documentation
* Updated getting_started.rst for allowing tag-based releases

## ✨ Features

* [#441](https://github.com/exasol/python-toolbox/issues/441): Switched nox task for `version:check` to use the config value of `version_file` to specify the location of the `version.py`

## 🐞 Bug Fixes
* Updated `python-environment` action to use space-separated values for extras


## ⚒️ Refactorings

* [#449](https://github.com/exasol/python-toolbox/issues/449): Refactored `dependency:licenses`:
    * to use pydantic models & `poetry show` for dependencies
    * to updated reading the `pyproject.toml` to be compatible with poetry 2.x+

## 🔩 Internal

* Relocked dependencies
