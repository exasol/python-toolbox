How to Release?
===============

Creating a Release
++++++++++++++++++

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