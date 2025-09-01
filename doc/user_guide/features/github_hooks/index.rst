.. _github_hooks:

Enabling GitHub Hooks
=====================

.. toctree::
    :maxdepth: 2

    troubleshooting

GitHub hooks are automated scripts that run at specific points during Git's execution,
allowing developers to enforce quality standards, automate tasks, and customize Git's
behavior. The PTB uses the `pre-commit <https://pre-commit.com/>`__ framework to
define common GitHub hooks for Git commits and pushes. The configuration for
``pre-commit``  is provided in a ``.pre-commit-config.yaml`` file and described in
:ref:`pre-commit_configuration`.

.. _pre-commit_configuration:

Configuration
+++++++++++++

#. Add a ``.pre-commit-config.yaml`` file to your project's root directory. Feel free to
   take inspiration from the example ``.pre-commit-config.yaml``:

    .. collapse:: .pre-commit-config.yaml

        .. literalinclude:: ../../../../project-template/{{cookiecutter.repo_name}}/.pre-commit-config.yaml
           :language: yaml


#. Enable pre-commit hooks for your workspace:

    .. code-block:: shell

        poetry run -- pre-commit install --hook-type pre-commit --hook-type pre-push


Working with ``pre-commit``
+++++++++++++++++++++++++++

.. _committing:

Committing
----------

Once ``pre-commit`` has been configured, the process for performing a ``git commit`` is:

#. Make your code changes
#. ``git add`` changed files and ``git commit -m "<message>"``
#. ``pre-commit`` performs checks on the changed files and produces an output like

    .. code-block:: bash

        code-format..........................................(no files to check)Skipped
        check yaml...........................................(no files to check)Skipped
        fix end of files.........................................................Passed
        trim trailing whitespace.................................................Passed

   * If all steps pass, then no action is needed.
   * If a step fails, then check the output further. If it was an automatic fix, then
     just add the altered file to your commit and execute your ``git commit`` line again.
     Otherwise, manual intervention is needed.

Pushing
-------

Once ``pre-commit`` has been configured, the process for performing a ``git push`` is:

#. Perform one or more iterations of :ref:`committing`.
#. ``git push``
#. ``pre-commit`` performs checks on the changed files and produces an output like

    .. code-block:: bash

        type-check...............................................................Passed
        lint.....................................................................Passed

   * If all steps pass, then no action is needed.
   * If a step fails, then check the output further. The suggested ``pre-push`` actions
     given in the :ref:`pre-commit_configuration` require manual intervention. Create
     a new commit to resolve the issue & try ``git push`` again.
