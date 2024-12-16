# Unreleased

## 🚨 Breaking Changes
* **Matrices in CI/CD workflows will be generated automatically now**

    Make sure you have installed all the latest workflow files, especially the newly added ones:

    - `matrix-all.yml`
    - `matrix-python.yml`
    - `matrix-exasol.yml`


## ✨ Added
* Added support for dynamically generated workflow matrices.

    This feature allows you to easily change the test matrices in one place: `noxconfig.py`.

    Note: As usual, there are different ways a user can adjust or change the behavior. In the case of the build matrices, there are three obvious ways:

    - Set the appropriate fields in the `noxconfig.py` project configuration (`PROJECT_CONFIG`):
        * `python_versions = [ ... ]`
        * `exasol_versions = [ ... ]`
    - Overwrite the nox tasks:
        * `matrix:all`
        * `matrix:python`
        * `matrix:exasol`
    - Overwrite/replace the matrix generation workflows:
        * `matrix-all.yml`
        * `matrix-python.yml`
        * `matrix-exasol.yml`

    Among all of the above, the safest way is to set the matrix-related fields in your project config object in `noxconfig.py`.

* Added a nox task to validate the build/test artifacts and use it in the github workflow report


## 📚 Documentation

* Added new entries to the frequently asked questions regarding `multiversion documentation`


## 🐞 Fixed

* Fixed `index.rst` documentation template to provide the correct underlining length of the main heading
* Added multi-version extension to Sphinx configuration of the project template
* fixed bug in tbx worflow install error if directory exists [#298](https://github.com/exasol/python-toolbox/issues/298) also [#297](https://github.com/exasol/python-toolbox/issues/297)

## 🔩 Internal
* Relocked dependencies
