Creating a release
==================

Preparing a release
+++++++++++++++++++

The ``release:prepare`` nox session affects files in the ``doc/changes`` directory:

* Creates & switches to a release branch (can be skipped with ``--no-branch``)
* Updates the version in the ``pyproject.toml``
* Moves the content of unreleased changes file ``unreleased.md`` to a versioned changes file ``changes_<version>.md``
* Appends to the versioned changes file any direct dependency changes between the current ``poetry.lock`` and the one from the latest tag
* Updates the ``changelog.md`` list with the newly create versioned changes file
* Commits the changes (can be skipped with ``--no-add``)
* Pushes the changes and creates a PR (can be deactivated with ``--no-pr``)

After a PR is created, approved, & merged into the default branch. A developer can use
the ``release:trigger`` nox session which:

* Switches & pulls the changes from the default branch
* Verifies that the version to be released does not already have a git tag or GitHub release
* Creates a new tag & pushes it to the default branch, which will trigger the GitHub workflow ``cd.yml``

Simple instructions
-------------------

The ``release:trigger`` nox session


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
