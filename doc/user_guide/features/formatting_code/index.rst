.. _formatting_code:


Formatting code
===============

.. toctree::
    :maxdepth: 2

    troubleshooting

The PTB allows you to automatically format your code and to ensure via a step in the
``checks.yml`` GitHub workflow that your committed code adheres to these standards. The
goals of this are to improve the readability and maintainability of your code and to
provide a uniform experience across projects.

Nox sessions
++++++++++++

For autoformatting, we use the following tools:

* `black` - automatically formats Python code to maintain consistent styling standards.
* `isort`
* `pyupgrade`
* `ruff` - includes a plethora of tools to automatically format code. In
  the PTB, only the following checks are active:

   * `unused-import (F401) <https://docs.astral.sh/ruff/rules/unused-import/>`__ - remove unused imports

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

`pre-commit`
++++++++++++


Configuration
+++++++++++++


Ensure ``isort`` is configured with compatibility for ``black``:

.. code-block:: toml

    [tool.isort]
    profile = "black"
    force_grid_wrap = 2

Additionally, your black configuration should look similar to this:

.. code-block:: toml

    [tool.black]
    line-length = 88
    verbose = false
    include = "\\.pyi?$"
