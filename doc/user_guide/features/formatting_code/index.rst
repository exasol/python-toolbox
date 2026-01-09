.. _formatting_code:

Formatting code
===============

.. toctree::
    :maxdepth: 2

    configuration
    troubleshooting

The PTB automatically formats code and ensures via a step in the ``checks.yml`` GitHub
workflow that committed code adheres to these standards. The goals of this are to
improve the readability and maintainability of the code and to provide a uniform
experience across projects.

.. _formatting_sessions:

Nox sessions
++++++++++++

.. note::
    To prevent Python files from being formatted, you can do one of the following:
        * For a single file, use a comment in the files as described in :ref:`this table <prevent_auto_format>`.
        * If it is a directory (i.e. ``.workspace``), then you can exclude it by
          adding it to the ``add_to_excluded_python_paths`` in the project's ``Config``
          defined in the ``noxconfig.py``.

For autoformatting, the following tools are used:

* `black <https://black.readthedocs.io/en/stable/the_black_code_style/index.html>`__ -
  formats Python code to maintain consistent styling standards.
* `isort <https://pycqa.github.io/isort/index.html>`__ - organizes and formats Python
  import statements alphabetically and by type (from __future__, standard library
  packages, third party packages, and local application imports).
* `pyupgrade <https://pypi.org/project/pyupgrade/>`__ - upgrades syntax for newer
  versions of the Python language.
* `ruff <https://docs.astral.sh/ruff/>`__ - includes a plethora of tools to check and
  automatically format code. In the PTB, only the following checks are active:

   * `unused-import (F401) <https://docs.astral.sh/ruff/rules/unused-import/>`__ - removes unused imports

In the PTB, these tools are bundled into nox sessions to ensure that they are run in a
deterministic manner.

+--------------------+------------------+------------------------------------+
| Nox session        | CI Usage         | Action                             |
+====================+==================+====================================+
| ``format:fix``     | No               | Applies code formatting changes    |
+--------------------+------------------+------------------------------------+
| ``format:check``   | ``checks.yml``   | Checks that current code does not  |
|                    |                  | need to be re-formatted            |
+--------------------+------------------+------------------------------------+

