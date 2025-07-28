Creating a release
==================

Preparing a release
+++++++++++++++++++

The ``release:prepare`` nox session affects the ``pyproject.toml``, ``version.py``, and files in the ``doc/changes`` directory:

* Creates & switches to a release branch (can be skipped with ``--no-branch``)
* Updates the version in the ``pyproject.toml`` and ``version.py``
* Moves the content of unreleased changes file ``unreleased.md`` to a versioned changes file ``changes_<version>.md``
* Adds a description of dependency changes to the versioned changes file:

  * Only direct dependencies are described, no transitive dependencies
  * Changes are detected by comparing the current content of file ``poetry.lock`` to the latest Git tag.
* Updates the ``changelog.md`` list with the newly created versioned changes file
* Commits the changes (can be skipped with ``--no-add``)
* Pushes the changes and creates a PR (can be skipped with ``--no-pr``)

After a PR is created, approved, & merged into the default branch. A developer can use
the nox session ``release:trigger`` nox session to:

* Switch to & pull the changes from the default branch
* Verify that the version to be released does not already have a git tag or GitHub release
* Create a new tag & push it to the default branch, which will trigger the GitHub workflow ``cd.yml``

Simplified instructions
-------------------

#. Prepare the project for a new release:

    .. code-block:: shell

         nox -s release:prepare -- --type {major,minor,patch}

#. Merge your **Pull Request** to the **default branch**

#. Trigger the release:

    .. code-block:: shell

        nox -s release:trigger


What to do if the release failed?
+++++++++++++++++++++++++++++++++

The release failed during pre-release checks
--------------------------------------------

#. Delete the local tag

    .. code-block:: shell

        git tag -d "<major>.<minor>.<patch>""

#. Delete the remote tag

    .. code-block:: shell

        git push --delete origin "<major>.<minor>.<patch>"

#. Fix the issue(s) which led to the failing checks
#. Start the release process from the beginning


One of the release steps failed (Partial Release)
-------------------------------------------------
#. Check the GitHub action/workflow to see which steps failed
#. Finish or redo the failed release steps manually

.. note:: Example

    **Scenario**: Publishing of the release on GitHub was successfully but during the PyPi release, the upload step was interrupted.

    **Solution**: Manually push the package to PyPi
