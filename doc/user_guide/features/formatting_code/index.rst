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

.. _pre_commit:

pre-commit
++++++++++++

`Pre-commit <https://pre-commit.com/>` is a framework that automatically runs
configurable checks and fixes on code before Git commits and pushes.
Included in the cookiecutter project template is a ``.pre-commit-config.yaml``, which
uses the formatting :ref:`formatting_sessions`. For information on configuring and
setting it up see :ref:`pre-commit_configuration`.

Once it's ready to use, the process is:

#. Make your code changes
#. ``git add -u`` and ``git commit -m "<message>"``
#. pre-commit performs checks on the changed files and produces an output like

    .. code-block:: bash

        code-format..........................................(no files to check)Skipped
        check yaml...........................................(no files to check)Skipped
        fix end of files.........................................................Passed
        trim trailing whitespace.................................................Passed

   * If all steps pass, then no action is needed.
   * If a step fails, then check the output further. If it was an automatic fix, then
     just add the altered file to your commit and execute your ``git commit`` line again.
     Otherwise, you will need to take on manual intervention.

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

.. _pre-commit_configuration:

pre-commit
^^^^^^^^^^
#. Add a :code:`.pre-commit-config.yaml` file to your project root

    Feel free to get some inspiration from the Python toolbox itself:

    .. literalinclude:: ../../../../project-template/{{cookiecutter.repo_name}}/.pre-commit-config.yaml
       :language: yaml

#. Enable pre-commit hooks for your workspace

    .. code-block:: shell

        poetry run -- pre-commit install --hook-type pre-commit --hook-type pre-push


pyupgrade
^^^^^^^^^
No initial configuration of ``pyupgrade`` is required.

For individual configuration, see the
`pyupgrade CLI options <https://pypi.org/project/pyupgrade/>`__. These can
be passed to the :ref:`formatting_sessions` via the ``pyupgrade_args``
attribute of the :class:`noxconfig.Config`.
