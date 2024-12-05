# 0.19.0 - 2024-12-05

## 🔧 Changed

* Add `__version__` member to generated `version.py` for compatibility with other versions schemes
* Excluded pyupgrade from project check due to its destructive nature
* Updated cookiecutter template
    - removed obsolete template file `version.html`
* Added nox task for format checking
* Updated GitHub workflow and workflow template of `checks.yml` to include format check

## 🐞 Fixed

* Fixed syntax error in the `check.yml` template which resulted in an invalid workflow file
* Fixed context forwarding to plugins hooking into `pre` and `post` integration test hooks
    - `pre_integration_tests_hook(self, session, config, context)`
    - `post_integration_tests_hook(self, session, config, context)`

## 📚 Documentation

* Fixed various documentation typos
* Added a toolbox migration guide
* Fixed version information in GitHub Actions reference
* Updated the `pre-commit` related documentation
