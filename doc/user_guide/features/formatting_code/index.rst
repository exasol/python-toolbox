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

isort
^^^^^
Ensure ``isort`` is configured with compatibility for ``black``:

.. literalinclude:: ../../../../project-template/{{cookiecutter.repo_name}}/pyproject.toml
  :language: toml
  :start-at: [tool.isort]
  :end-before: [tool.pylint.master]

pyupgrade
^^^^^^^^^
No initial configuration of ``pyupgrade`` is required.
