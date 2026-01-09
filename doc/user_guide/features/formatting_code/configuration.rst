.. _formatting_configuration:

Configuring Formatting
++++++++++++++++++++++

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
