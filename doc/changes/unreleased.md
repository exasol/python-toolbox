# Unreleased

## Summary

With #441, please ensure that the location of the `version.py` is given for `Config.version_file`,
which is specified in the `noxconfig.py`

## 📚 Documentation
* Updated getting_started.rst for allowing tag-based releases

## ✨ Features

* [#441](https://github.com/exasol/python-toolbox/issues/441): Switched nox task for `version:check` to use the config value of `version_file` to specify the location of the `version.py`
* [#382](https://github.com/exasol/python-toolbox/issues/382): Removed `tool.poetry.dev.dependencies` from nox task `dependency:licenses` as not poetry 2.x+ compatible