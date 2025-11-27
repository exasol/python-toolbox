Migrating Legacy Projects
=========================

Migrating old projects to a new project setup and the :code:`python-toolbox` can be tedious and annoying. This guide will try to provide some basic steps and guidance to simplify this process.

.. _before_you_migrate:

What a Project Should Have Before You Migrate
+++++++++++++++++++++++++++++++++++++++++++++

* The project configuration should be :code:`pyproject.toml` based. **[Required]**
* The project should be :code:`poetry` based. **[Required]**
* Dependencies should point only to officially published dependencies on PyPI (no git references or similar) **[Required]**.
* The project documentation should be :code:`sphinx` based **[Required]**.
* Automated tasks within the project should be available as Python code or `Nox`_ tasks. **[Helpful]**

.. hint::

    If you are interested or want to get a good idea of what a bare standard project based on the toolbox should have, excluding the workflows, it is always good to have a look at the `cookiecutter template <https://github.com/exasol/python-toolbox/tree/main/project-template>`_ provided by the toolbox. If the template parts are confusing, you can generate an "empty" project based on it. For details, refer to the :ref:`new project` section.


Iterative Migration Guide
++++++++++++++++++++++++++

Ensure you comply with the :ref:`basic requirements <before_you_migrate>` for your project. Follow these steps for a smooth migration process.

1. Introduce Nox
----------------
As a first step, it is generally advisable to introduce `Nox`_ as a task runner if it is not already in use. Since the :code:`python-toolbox` uses `Nox`_ as its foundation, this simplifies the migration to the toolbox and enhances the user's understanding of `Nox`_.

2. Introduce the Standard Nox Tasks
-----------------------------------
This can be done incrementally for different checks of your project, such as *project*, *test*, *linting*, *documentation*, and *other* tasks.
As the tasks can be split into roughly five groups, it likely makes sense to integrate at least one group at a time.

Overloading a Task
__________________

In certain cases, it may not be trivial to use the nox task defined within the `python-toolbox`_. In those cases, overloads can be used to provide a smoother or faster transition or to cope with project-specific constraints or needs.

For example, if test execution isn't performed in the standard way (e.g., :code:`pytest test/unit`, :code:`pytest test/integration`, :code:`pytest test`).

.. warning::

   While overwriting can be handy and seem like the simplest way to integrate with the toolbox, please take care when making this decision. In the long run, we want to harmonize projects, their builds, execution, testing, and reporting, etc. If you create an overwrite, you are likely to run into troubles later on, e.g., when reporting is required, because you may lack specific artifacts a specific task was creating, etc.

   So while overwriting can be a good temporary solution, for the long term, it should be considered where to add or use a configuration point within the toolbox to make the standard task work for *all* projects.

   **Potential options here are:**

   * Add additional :ref:`plugin extension <plugin support>` points to the toolbox
   * Implement functionality for an :ref:`existing extension point <plugins>` in the `python-toolbox`_
   * Add additional configuration parameters in :code:`noxconfig.py` or :code:`pyproject.toml`
   * Add additional parameterization to tasks
   * :code:`pytest plugins` can take care of a specific test preparation need, e.g., `pytest-backend <https://github.com/exasol/pytest-plugins/tree/main/pytest-backend>`_


.. code-block:: python

    import nox

    # imports all nox task provided by the toolbox
    from exasol.toolbox.nox.tasks import *  # pylint: disable=wildcard-import disable=unused-wildcard-import

    # default actions to be run if nothing is explicitly specified with the -s option
    nox.options.sessions = ["project:fix"]

    @nox.session(name="project:fix", python=False)
    def my_project_fix_overwrite(session) -> None:
        """Runs all automated fixes on the code base"""

        # ATTENTION:
        # In cases where it is reasonable to use "internal" functions, please do those imports
        # within the function to keep them isolated and simplify future removal or replacement.
        from exasol.toolbox.nox._shared import get_filtered_python_files

        py_files = get_filtered_python_files(PROJECT_CONFIG.root)
        print("The original 'project:fix' task has been taken hostage by this overwrite")
        print("Files:\n{files}".format(files="\n".join(py_files))


3. Establish a Baseline
-----------------------
Configure code quality settings in the :code:`pyproject.toml` file to establish a baseline for your project. If necessary, create tickets for further improvements, especially if major parts of your code require suppression, e.g., in the mypy configuration.

**:code:`pyproject.toml` sections to include/consider:**

* [tool.coverage.run]
* [tool.coverage.report]
* [tool.black]
* [tool.isort]
* [tool.pylint.format]
* [[tool.mypy.overrides]]

Example
_______

.. code-block:: toml

    # Adjust this section if you want fine-grained control
    # over what is considered for code coverage
    [tool.coverage.run]
    relative_files = true
    source = [
        "exasol",
    ]

    # Adjust this section to define the minimum required
    # code coverage for your project
    [tool.coverage.report]
    fail_under = 15


    # Adjust control maximum line length in your project
    #
    # NOTE:
    # As a rule of thumb, you should not exceed 120 characters,
    # because overly long lines usually accompany higher cyclomatic complexity,
    # as complex functions tend to shift right.
    [tool.black]
    line-length = 88
    include = "\\.pyi?$"


    # Adjust to modify the behavior of import sorting
    [tool.isort]
    profile = "black"
    force_grid_wrap = 2


    # Adjust to define the minimum linting score considered acceptable for your project
    [tool.pylint.master]
    fail-under = 7.5

    # Maximum line length should match what is configured for black.
    # Additionally, a maximum module size can be defined here.
    [tool.pylint.format]
    max-line-length = 88
    max-module-lines = 800


    # Configure exceptions for the type checker
    [[tool.mypy.overrides]]
    module = [
        "test.unit.*",
        "test.integration.*",
    ]
    ignore_errors = true


4. Introduce GitHub Workflows
-----------------------------
Install the GitHub workflows provided by the :code:`python-toolbox` for further details refer to the section :ref:`GitHub Workflows`.

.. attention::
   This is just guidance. If you have a good understanding of the standard project setup, technologies, and tools used, feel free to diverge at any point or exercise your own judgment.


Migration Progress
++++++++++++++++++

Could be tracked in a format and based on the information listed in the real life example bellow.

.. hint::

    This table does not provide any information about the specific `python-toolbox`_ used in the respective projects.

.. list-table:: Migration Progress
    :widths: 20 15 15 15 15 15 15 15
    :header-rows: 1

    * - Project
      - pyproject.toml
      - poetry
      - PyPI
      - Sphinx Docs
      - nox
      - toolbox-tasks
      - toolbox-workflows
    * - `python-toolbox`_
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
    * - `error-reporting-python <https://github.com/exasol/error-reporting-python>`_
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
    * - `pyexasol <https://github.com/exasol/pyexasol>`_
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
    * - `sqlalchemy-exasol <https://github.com/exasol/sqlalchemy-exasol>`_
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
      - ✗
      - ✗
    * - `bucketfs-python <https://github.com/exasol/bucketfs-python/tree/main>`_
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓/✗ partially
    * - `ITDE <https://github.com/exasol/integration-test-docker-environment>`_
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓/✗ partially
      - ✓/✗ partially
    * - `schemas <https://github.com/exasol/schemas>`_
      - ✓
      - ✓
      - ✗
      - ✗
      - ✗
      - ✗
      - ✗
    * - `pytest-plugins <https://github.com/exasol/pytest-plugins>`_
      - ✓
      - ✓
      - ✓
      - ✓/✗ partially
      - ✓
      - ✓/✗ partially
      - ✗
    * - `harlequin-exasol <https://github.com/Nicoretti/harlequin-exasol>`_
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
      - ✓
      - ✗


.. list-table:: Legend
    :widths: 20 80
    :header-rows: 1

    * - Column
      - Description
    * - Project
      - Name of the project
    * - pyproject.toml
      - Project configuration and setup is `pyproject.toml`_ based
    * - poetry
      - Project configuration and build is `Poetry`_ based
    * - PYPI
      - Project can be build and published to `PyPi`_
    * - Sphinx Docs
      - The project documentation is `Sphinx`_ based
    * - nox
      - The projects automated tasks are executed using the `Nox`_ task runner
    * - toolbox-tasks
      - All nox tasks provided by the `python-toolbox`_ are available and fully functional
    * - toolbox-workflows
      - All :ref:`GitHub Workflows` provided by the `python-toolbox`_ are available and fully functional

.. _pyproject.toml: https://peps.python.org/pep-0621/
.. _Nox: https://nox.thea.codes/en/stable/
.. _Poetry: https://python-poetry.org/
.. _PyPi: https://pypi.org/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _python-toolbox: https://github.com/exasol/python-toolbox
