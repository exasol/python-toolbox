How to Release?
===============

Creating a Release
++++++++++++++++++

#. Prepare the project for a new release:

    .. code-block:: shell

        nox -s release:prepare -- [-h] [-v | --version VERSION] [-t | --type {major,minor,patch}]

#. Merge your **Pull Request** to the **default branch**

#. Trigger the release:

    .. code-block:: shell

        nox -s release:trigger -- [-h] [-v | --version VERSION] [-t | --type {major,minor,patch}]

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