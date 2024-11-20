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


Iterative Migration Guide
++++++++++++++++++++++++++

Ensure you comply with the basic requirements for your project. Follow these steps for a smooth migration process.

1. Introduce Nox
----------------
As a first step, it is generally advisable to introduce `Nox`_ as a task runner if it is not already in use. Since the :code:`python-toolbox` uses `Nox`_ as its foundation, this simplifies the migration to the toolbox and enhances the user's understanding of `Nox`_.

2. Introduce Python-Toolbox Nox Tasks
-------------------------------------
This can be done incrementally for different checks of your project, such as linting, typing, documentation, and other tasks.

.. note::
   If test execution isn't performed in the standard way (e.g., :code:`pytest test/unit`, :code:`pytest test/integration`, :code:`pytest test`), you will need to overwrite the test-specific Nox tasks and will not be able to use the default ones.

3. Establish a Baseline
-----------------------
Configure code quality and settings in the :code:`pyproject.toml` and establish a baseline for your project. If necessary, create tickets for further improvements, especially if major parts of your code need suppression, e.g., in the mypy configuration.

4. Introduce GitHub Workflows
-----------------------------
Install the GitHub workflow provided by the :code:`python-toolbox` for futher details refer to the section :ref:`GitHub Workflows`.

.. attention::
   This is just guidance. If you have a good understanding of the standard project setup, technologies, and tools used, feel free to diverge at any point or exercise your own judgment.

.. _Nox: https://github.com/exasol/python-toolbox/pull/289
