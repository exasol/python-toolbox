# Unreleased

## 🚨 Breaking Changes
* **CI-CD Workflow (Breaking Change)**

    **Overview:**

    The CI-CD workflow now assumes the changelog to be in markdown and the location `/doc/changes/change_x.y.z.md`

## 🐞 Fixed
* Fixed `_deny_filter` function in `exasol.toolbox._shared` module
* Fixed GitHub workflow references in `ci.yml`, ci-cd.yml` and `pr-merge.yml` workflows
* Fixed indent error/issue in `checks.yml` workflow

## ✨ Added
* **Added Nox Task `prepare-release`**

    **Overview:**

    A new Nox task, `prepare-release`, has been introduced to streamline the release preparation process. This task automates several crucial steps:

    - Create a dedicated branch for the release changes.
    - Transfer changes from the "Unreleased" section to the appropriate versioned changelog section.
    - Update the version number to the next release.
    - Initiate a Pull Request (PR) for review and integration into the main branch.

    **Usage:**

    To prepare a release, simply execute a command in your terminal like in the example below:

    ```shell
    nox -s prepare-release -- 1.10.1
    ```

    Add the changes for releasing on top of the current branch:

    ```shell
    nox -s prepare-release -- 1.10.1 --no-pr --no-branch
    ```

    For additional options and help regarding the task `prepare-release`, execute:

    ```shell
    nox -s prepare-release -- -h 
    ```

## 📚 Documentation
* Fixed typos and updated documentation

## 🔩 Internal
* Restructured `exasol.toolbox.nox` module
