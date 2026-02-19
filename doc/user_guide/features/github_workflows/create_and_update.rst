.. _update_github_workflows:

Creating and Updating the GitHub Workflows in Your Project
==========================================================

PTB can initially generate the GitHub workflows in your project and also
update existing workflows.

The workflows are based on Jinja templates with variables populated by the
PTB. The PTB reads the values from various places within your project, see
:ref:`template_variables`.

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

PTB has a default for these versions, but you can override it in file
``noxconfig.py``, e.g.

.. code-block:: shell

    PROJECT_CONFIG = Config(
        python_versions=("3.10", "3.12),
        exasol_versions=("7.1.30", "8.29.13", "2025.1.8"),
    )

Some workflows are expected to not depend on a specific python version and
will use only the lowest Python version in the list specified above.

If you want to use a different version, though, you can override the default
in your ``PROJECT_CONFIG``:

.. code-block:: shell

    PROJECT_CONFIG = Config(
        python_versions=("3.10", "3.12),
        minimum_python_version="3.12",
    )

.. _update_workflows:

Add all Workflows to Your Project
---------------------------------

.. code-block:: shell

    tbx workflow install all

.. warning::
    #. If you already have various workflows, you may want to run the
       :code:`update` command instead of the :code:`install` command.

    #. Some workflows depend on other workflows. Please ensure you have all
       the required workflows if you do not install all of them.
