.. _formatting_code:

Formatting code
===============

.. toctree::
    :maxdepth: 2

    troubleshooting

The PTB automatically formats code and ensures via a step in the ``checks.yml`` GitHub
workflow that committed code adheres to these standards. The goals of this are to
improve the readability and maintainability of the code and to provide a uniform
experience across projects.

.. _formatting_sessions:

Nox sessions
++++++++++++

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
| ``project:fix``    | No               | Applies code formatting changes    |
+--------------------+------------------+------------------------------------+
| ``project:format`` | ``checks.yml``   | Checks that current code does not  |
|                    |                  | need to be re-formatted            |
+--------------------+------------------+------------------------------------+

.. _formatting_configuration:

Configuration
+++++++++++++

black
^^^^^

Your ``black`` configuration should look similar to this:

.. literalinclude:: ../../../../project-template/{{cookiecutter.repo_name}}/pyproject.toml
  :language: toml
  :start-at: [tool.black]
  :end-before: [tool.isort]

For further configuration options, see
`black configuration <https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#configuration-format>`__.

isort
^^^^^

Ensure ``isort`` is configured with compatibility for ``black``:

.. literalinclude:: ../../../../project-template/{{cookiecutter.repo_name}}/pyproject.toml
  :language: toml
  :start-at: [tool.isort]
  :end-before: [tool.pylint.master]

For further configuration options, see
`isort options <https://pycqa.github.io/isort/docs/configuration/options.html>`__.


pyupgrade
^^^^^^^^^

No initial configuration of ``pyupgrade`` is required. By default, this is
configured to be derived from the minimum Python version that your project supports
and is defined in the :meth:`exasol.toolbox.config.BaseConfig.pyupgrade_argument`.

For further configuration options, see the
`pyupgrade documentation <https://pypi.org/project/pyupgrade/>`__.

ruff
^^^^

Ensure ``ruff`` is configured like so:

.. literalinclude:: ../../../../project-template/{{cookiecutter.repo_name}}/pyproject.toml
  :language: toml
  :start-at: [tool.ruff.lint]
  :end-before: [tool.mypy.overrides]

For further configuration options, see
`ruff options <https://docs.astral.sh/ruff/configuration>`__.
