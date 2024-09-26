Github Workflows
================

The exasol-toolbox ships with various GitHub workflows. By default, we suggest installing all of them,
while the core workflows are:

**Workflows**:

* CI
    Verifies PRs and regularly checks the project.

* CD
    Publishes releases of the project.

* PR-Merge
    Validates merges and updates the documentation.


The toolbox command itself, :code:`tbx`, provides various CLI functions to help you maintain those workflows.
For further help, run the command :code:`tbx workflow --help`.

1. Configure your project
+++++++++++++++++++++++++

* Make sure your GitHub project has access to a deployment token for PyPi with the following name: **PYPI_TOKEN**. It should be available to the repository either as an Organization-, Repository-, or Environment-secret.

* If you want to enable manual approval for "slow" CI steps, add an environment named :code:`manual-approval` (:code:`Settings/Environments/manual-approval`) and configure it appropriately.

2. Add all workflows to your project
++++++++++++++++++++++++++++++++++++

.. code-block:: shell

    tbx workflow install all

.. warning::

    #. If you already have various workflows, you may want to run the :code:`update` command instead of the :code:`install` command.

    #. Some workflows depend on other workflows. Please ensure you have all the required workflows if you do not install all of them.

3. Update Branch Protection
++++++++++++++++++++++++++++

The best and most maintainable way to have solid branch protection (:code:`Settings/Branches/main`) is to require the workflow :code:`CI / Allow Merge` to pass successfully.
