Creating a Release
==================

Preparing a Release
+++++++++++++++++++

#. Prepare the project for a new release

    .. code-block:: shell

         nox -s release:prepare -- --type {major,minor,patch}

    The ``release:prepare`` nox session affects the ``pyproject.toml`` and files in the
    ``doc/changes`` directory:

    * Creates & switches to a release branch (can be skipped with ``--no-branch``)
    * Updates the version in the ``pyproject.toml``
    * Moves the content of unreleased changes file ``unreleased.md`` to a
      versioned changes file ``changes_<version>.md``
    * Describes additional changes in the versioned changes file by comparing
      file ``poetry.lock`` to the latest Git tag:

      * Resolved vulnerabilities based on `Pip Audit`_.
      * Updated direct dependencies, excluding transitive dependencies
    * Updates file ``changelog.md`` to list the newly created versioned changes file
    * Commits the changes (can be skipped with ``--no-add``)
    * Pushes the changes and creates a PR (can be skipped with ``--no-pr``)

.. _Pip Audit: https://pypi.org/project/pip-audit/

#. Merge your **Pull Request** to the **default branch**

#. Trigger the release

    .. code-block:: shell

        nox -s release:trigger

    Use the nox session ``release:trigger`` to:

    * Switch to & pull the changes from the default branch
    * Verify that the version to be released does not already have a git tag
      or GitHub release
    * Create a new tag & push it to the default branch, which will trigger the
      GitHub workflow ``cd.yml``

    Additionally, if enabled in your project config, the task will create an
    additional tag with pattern ``v<MAJOR_VERSION>``.  This is especially
    useful if other projects use Github actions of your project, for example:

    .. code-block:: yaml

        uses: exasol/your_project/.github/actions/your_action@v1

    Your ``PROJECT_CONFIG`` needs to have the flag
    ``create_major_version_tags=True``.

Updating The Versioned Changes File
+++++++++++++++++++++++++++++++++++

If you need to update some dependencies after running the nox session
``release:prepare`` you can update the versioned changes file by running the
nox session ``release:update``.


What to do if the Release Failed?
+++++++++++++++++++++++++++++++++

The Release Failed During Pre-Release Checks
--------------------------------------------

#. Delete the local tag

    .. code-block:: shell

        git tag -d "<major>.<minor>.<patch>""

#. Delete the remote tag

    .. code-block:: shell

        git push --delete origin "<major>.<minor>.<patch>"

#. Fix the issue(s) which led to the failing checks
#. Start the release process from the beginning


One of the Release Steps Failed (Partial Release)
-------------------------------------------------
#. Check the GitHub action/workflow to see which steps failed
#. Finish or redo the failed release steps manually

.. note:: Example

    **Scenario**: Publishing of the release on GitHub was successful but
    during the PyPi release, the upload step was interrupted.

    **Solution**: Manually push the package to PyPi
