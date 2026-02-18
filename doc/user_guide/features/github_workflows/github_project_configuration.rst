.. _github_project_configuration:

GitHub Project Configuration
============================

Branch Protection
-----------------

The best and most maintainable way to have solid branch protection
(:code:`Settings/Branches/main`) is to require the workflow :code:`CI / Allow
Merge` to pass successfully.

.. note::
   Setting the required status checks to pass before merging is only possible
   after running a CI build at **least once** on the affected branch.

Manual Approval
---------------

If your CI workflow involves slow or expensive steps you can guard these to be
executed only after manual approval. The CI workflow will automatically create
a GitHub environment named :code:`manual-approval`. You only need to add
reviewers in (:code:`Settings/Environments/manual-approval`) and move the
steps to be guarded into the related section in job :code:`slow-checks` in
file :code:`.github/workflows/merge-gate.yml`.

PYPI Token
----------

Make sure your GitHub project has access to a deployment token for PyPi with
the following name: **PYPI_TOKEN**. It should be available to the repository
either as an Organization-, Repository-, or Environment-secret.
