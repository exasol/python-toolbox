Workflows (CI/CD)
=================

Generate CI & CI/CD workflows
-----------------------------

The exasol-toolbox simplifies and supports 3 easily maintainable workflows.
in order to make them work follow the description bellow.

**Workflows**:

* CI
    Verifies PR's and regularly checks the project.

* CI/CD
    Verifies and publishes releases of the project.

* PR-Merge
    Validates merges  and updates the documentation.

0. Determine the toolbox version
++++++++++++++++++++++++++++++++
One of the snippets bellow, should do the trick:

#.

    .. code-block:: shell

        poetry show exasol-toolbox

#.

    .. code-block:: python

        python -c "from exasol.toolbox.version import VERSION;print(VERSION)"

1. Configure your project
++++++++++++++++++++++++++
Make sure your github project has access to a deployment token for PyPi with the following name:  **PYPI_TOKEN**.
It should be available to the repository either as Organization-, Repository- or Environment- secret.

2. Add the standard workflows to your project
+++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: shell

    tbx workflow install all

.. warning::

    If you already have various workflows you may want to run the
    :code:`update` instead of the :code:`install` command.

CI Workflow
___________

.. figure:: ../_static/ci-workflow.png
    :alt: ci-workflow

To enable this workflow, add a file with the name *ci.yml* in your *.github/workflows* folder
and add the following content:

.. literalinclude:: ../../exasol/toolbox/templates/github/workflows/ci.yml
    :language: yaml

CI/CD Workflow
______________

.. attention::

    Requires PYPI token to be available

.. figure:: ../_static/ci-cd-workflow.png
    :alt: ci-cd-workflow

To enable this workflow, add a file with the name *ci-cd.yml* in your *.github/workflows* folder
and add the following content:

.. literalinclude:: ../../exasol/toolbox/templates/github/workflows/ci-cd.yml
    :language: yaml

PR-Merge Workflow
_________________

.. figure:: ../_static/pr-merge-workflow.png
    :alt: pr-merge-workflow

To enable this workflow, add a file with the name *pr-merge.yml* in your *.github/workflows* folder
and add the following content:

.. literalinclude:: ../../exasol/toolbox/templates/github/workflows/pr-merge.yml
    :language: yaml

In order to make merging to the main branch faster you can skip running the
tests again in this workflow.

Before removing the ``ci-job`` from the workflow by please make sure the
following prerequisites are met, as in some circumstances these tests might be
the last or even only chance to detect problems.

* GitHub branch protection for main branch is properly configured.
* All dependencies are pointing to proper pypi packages in specific versions, i.e. no
  dependencies to the main branch of other git repositories.
* Development branches are short-lived and merged to main branch soon after
  finishing tests in the context of a pull request.
