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

Secrets
-------

For accessing specific services in the Internet, your project often needs a
related *token* or other credentials. These credentials can be acquired by
registering on the service's website.

In many cases your company or organization may manage the credentials
centrally and enable the use in multiple projects. The credentials can be
managed as Secrets in GitHub and can be made accessible to GitHub projects and
used by their workflows.

In summary, your GitHub project may have individual secrets and/or secrets
inherited from the enclosing GitHub *Organization*. As soon as a secret is
accessible to your project, your GitHub workflows can use it and probably will
map it to *environment variables* that are used by your CI/CD automation.

* **PYPI_TOKEN**: This secret is required to publish your project on the
  `Python Package Index <pypi_>`_ (PyPi). Most projects will use the
  org-secret.
* **SONAR_TOKEN**: See :ref:`Sonar Configuration <sonar_configuration>`.

.. _pypi: https://pypi.org/
