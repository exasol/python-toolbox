# 0.10.0 - 2024-05-15

🚨 Breaking Changes
Static callbacks/hooks in the Config object have been removed and replaced with Plugin hooks.

For additional information, refer to [customization](../user_guide/customization.rst) in the user guide.
## 🐞 Fixed
* Updated templates for GH workflows to add content of changes file for release letter

## ✨ Added
* Implemented plugin support for `pre-` and `post-` integration-tests hooks.

## 📚 Documentation
* Added documentation on nox task plugins for users and developers.
* Added documentation on python-environment action.
* Updated theme and structure of the documentation.

## 🔩 Internal
* Relocked and updated dependencies