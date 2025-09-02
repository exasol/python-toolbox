.. _features:

Features
========

.. toctree::
    :maxdepth: 2

    metrics/collecting_metrics
    creating_a_release
    documentation/index
    git_hooks/index
    formatting_code/index
    managing_dependencies

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
