# Unreleased

## ✨ Added

* added tbx task for markdown formating of .lint.json

## 🐞 Fixed
* Fixed an issue in the CI workflow that caused it to be executed twice on the initial push of a PR if the PR branch was on the repo itself.

    🚨 Attention: Due to these changes, the workflows will no longer be executed if the PR comes from a branch not located in this repository.
                  As third-party contributions from outside forks are rare to nearly non-existent, this downside was considered a reasonable trade-off at this time.

## 📚 Documentation
* Updated design doc (Added known Issues)
* Updated migration progress table

## 🔩 Internal
* Relocked dependencies
* Update referenced github actions
