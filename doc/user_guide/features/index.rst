.. _features:

Features
========

.. toctree::
   :maxdepth: 2

   formatting_code/index
   github_workflows/index
   documentation/index
   creating_a_release
   managing_dependencies/index
   git_hooks/index
   metrics/collecting_metrics

Uniform Project Layout
----------------------

The PTB expects a default project layout following "convention over configuration" wherever possible and reasonable.
See the cookiecutter project template, which can be found in directory `project-template`, for more details.
For more details on this, please check out section :ref:`Getting Started` section.

Nox
---

The most central tool when interacting with the toolbox is :code:`nox`, which is the task runner used across all of Exasol's Python-based projects.
The toolbox itself provides various standard tasks and a plugin mechanism to extend these tasks as needed. For more information regarding nox, please visit the `nox homepage <https://nox.thea.codes/en/stable/>`_.

Central files in regards to nox and the toolbox are:

- ``noxfile.py``: Standard nox configuration/setup file
- ``noxconfig.py``: Exasol-specific file containing additional information needed by the standard tasks of the toolbox

Important Nox Commands
^^^^^^^^^^^^^^^^^^^^^^

* :code:`nox -l` shows a list of all available nox sessions
* :code:`nox -s <session>` run the specified session(s)

Use :code:`nox -l` to show the current list of sessions for your project.

Common examples are:

* :code:`nox -s format:fix` applies formatting changes.
* :code:`nox -s project:check` runs the main local quality gate.
* :code:`nox -s test:unit` runs unit tests.
* :code:`nox -s workflow:generate -- all` updates PTB workflow files.

For more details, see the feature pages in this guide. They include formatting,
GitHub workflows, dependency management, release preparation, and code-quality
reporting.
