# Unreleased

## ✨ Added
* **Added Nox Task `prepare-release`**

    **Overview:**

    A new Nox task, `prepare-release`, has been introduced to streamline the release preparation process. This task automates several crucial steps:

    - Updates the version number to the next release.
    - Transfers changes from the "Unreleased" section to the appropriate versioned changelog section.
    - Creates a dedicated branch for the release changes.
    - Initiates a Pull Request (PR) for review and integration into the main branch.

    **Usage:**

    To prepare a release, simply execute the following command in your terminal:

    ```shell
    nox -s prepare-release -- 1.10.1
    ```

    Add the changes for releasing ontop of the current branch:

    ```shell
    nox -s prepare-release -- 1.10.1 --no-pr --no-branch
    ```

    For additional options and help regarding the prepare-release task, execute:

    ```shell
    nox -s prepare-release -- -h 
    ```
