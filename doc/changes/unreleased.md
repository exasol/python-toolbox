# Unreleased

## Summary

In this major release, support for the `version.py`file has been removed. Users should:
- delete the `version.py` file
- add in their project's `__init__.py` module

    ```python
    from importlib.metadata import version
    __version__ = version("<package_name>")
    ```
This is required for the nox session `docs:multiversion` to successfully complete,
and it is a Python standard for users to check in the terminal which version they are
using.

## Refactoring

* #800: Removed tbx security pretty-print, tbx lint pretty-print, and creation of .lint.txt, as superseded by Sonar and .lint.json usage
* #791: Resolved Sonar concerns: accepted specific `subprocess` import usage & improved minor maintainability items
* #629: Replace `version.py` with version from the `__init__.py`
