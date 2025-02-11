# Unreleased

## ✨ Added

* added tbx task for markdown formating of .lint.json
* Added a Nox task for dependencies packages and their licenses with Markdown output

## 🐞 Fixed
* Fixed an issue in the CI workflow that caused it to be executed twice on the initial push of a PR if the PR branch was on the repo itself.

    🚨 Attention: Due to these changes, the workflows will no longer be executed if the PR comes from a branch not located in this repository.
                  As third-party contributions from outside forks are rare to nearly non-existent, this downside was considered a reasonable trade-off at this time.

## 📚 Documentation
* Updated design doc (Added known Issues)
* Updated migration progress table
* Updated the FAQ with an entry about the ``isort`` compatibility issue
* [#351](https://github.com/exasol/python-toolbox/issues/351), [#352](https://github.com/exasol/python-toolbox/issues/352): updated user guide

## 🔧 Changed
* Updated `actions/upload-artifacts` version to `4.6.0`

## 🔩 Internal
* Relocked dependencies
* Update referenced github actions
