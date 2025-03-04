How to Release?
===============

Creating a Release
++++++++++++++++++

1. Set a variable named **TAG** with the appropriate version numbers:

    .. code-block:: shell

        TAG="<major>.<minor>.<patch>"

#. Prepare the project for a new release:

    .. code-block:: shell

        nox -s release:prepare -- "${TAG}"

#. Merge your **Pull Request** to the **default branch**
#. Switch to the **default branch**:

    .. code-block:: shell

        git checkout $(git remote show origin | sed -n '/HEAD branch/s/.*: //p')

#. Update branch:

    .. code-block:: shell

        git pull

#. Create a new tag in your local repo:

    .. code-block:: shell

        git tag "${TAG}"

#. Push the repo to remote:

    .. code-block:: shell

        git push origin "${TAG}"

    .. hint::

         GitHub workflow **.github/workflows/cd.yml** reacts on this tag and starts the release process

What to do if the release failed?
+++++++++++++++++++++++++++++++++

The release failed during pre-release checks
--------------------------------------------

#. Delete the local tag

    .. code-block:: shell

        git tag -d "${TAG}"

#. Delete the remote tag

    .. code-block:: shell

        git push --delete origin "${TAG}"

#. Fix the issue(s) which lead to the failing checks
#. Start the release process from the beginning


One of the release steps failed (Partial Release)
-------------------------------------------------
#. Check the Github action/workflow to see which steps failed
#. Finish or redo the failed release steps manually

.. note:: Example

    **Scenario**: Publishing of the release on Github was successfully but during the PyPi release, the upload step got interrupted.

    **Solution**: Manually push the package to PyPi