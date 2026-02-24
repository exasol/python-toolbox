.. _update_github_workflows:

Creating and Updating the GitHub Workflows in Your Project
==========================================================

The PTB can initially generate the GitHub workflows in your project and also
update existing workflows.

The workflows are based on Jinja templates with variables populated by the
PTB. The PTB reads the values from various attributes and properties of your
project's config, see :ref:`template_variables`.

Please note that the PTB only updates the values in the GitHub workflows when
*updating* the workflows. So, after updating the :ref:`list of Python versions
<python_versions>` in file ``noxconfig.py``, you need to :ref:`re-generate
<update_workflows>` the GitHub workflows.

Poetry Version
--------------

PTB has a default value for the Poetry version but you can override it in file
``noxconfig.py``, e.g.

.. code-block:: shell

    PROJECT_CONFIG = Config(
        dependency_manager=DependencyManager(name="poetry", version="2.3.0"),
    )

.. _python_versions:

Versions of Python and Exasol Docker DB
---------------------------------------

Many workflows are using a Build-matrix to iterate over multiple versions of
Python and/or the Exasol Docker DB. This is to make sure your code is valid,
free of bugs and working correctly for each combination of these items.

The PTB has a default for these versions, but you can override it in the
``noxconfig.py`` file, e.g.

.. code-block:: shell

    PROJECT_CONFIG = Config(
        python_versions=("3.10", "3.12),
        exasol_versions=("7.1.30", "8.29.13", "2025.1.8"),
    )

Some workflows are expected to not depend on a specific Python version and
will use only the lowest Python version in the list specified above.

.. _customize_workflows:

Customize Workflows for Your Project
------------------------------------

The PTB allows you to customise workflows by targeting specific jobs or steps:

* Remove a job by its job_name.
* Replace a step (referenced by step_id) with one or more new steps.
* Insert steps after a specific step_id.

.. note::

   These operations do not currently cascade. For example, removing a job
   without accounting for its downstream dependencies may result in errors.
   You must manually adjust any subsequent steps that rely on the removed
   job's or step's output.

.. _update_workflows:

Add all Workflows to Your Project
---------------------------------

.. code-block:: shell

    poetry run -- nox -s workflow:generate -- all

.. warning::
    Some workflows depend on other workflows. Please ensure you have all
    the required workflows if you do not install all of them.

.. note::

   The commands:

   * ``tbx workflow install all`` - used to install workflows
   * ``tbx workflow update all`` - used to update workflows

   are considered historic variants of this command.

   **Deprecation Notice:**
   These ``tbx`` endpoints are marked as **deprecated** and are scheduled for removal
   by **April 22nd, 2025**.

   Please note that these legacy commands do not allow users to use their specified
   ``.workflow-patcher.yml`` file to further customise or patch workflows. Users
   should transition to the ``nox``-based command to leverage full customisation
   features.
