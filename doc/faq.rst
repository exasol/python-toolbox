.. _faq_toolbox:

:octicon:`question` FAQ
=======================


.. _faq_no_module_noxconfig:

No Module Named 'noxconfig'
---------------------------

The error, :code:`ModuleNotFoundError: No module named 'noxconfig'`, often appears on systems such as Fedora, where the current path may not be included in the :code:`PYTHONPATH`. This issue is elaborated upon at https://fedoraproject.org/wiki/Changes/PythonSafePath. Accordingly, it may be necessary to correctly set the :code:`PYTHONPATH` before initiating nox, as our nox tasks anticipate the `noxconfig` module to be located within the python path.

There are several methods to configure your shell:

    1. For a one-time setup: :code:`PYTHONPATH=\`pwd\` nox -s task`
    2. For a general setup: :code:`export PYTHONPATH=`pwd``
    3. Alternatively, tools like `direnv <https://direnv.net>`_ can be used.

.. _faq_failing_format_check:

Format Still Fails After Running ``project:fix``
------------------------------------------------

If running the following sequence of commands results in ``project:format`` failing with an error during the execution of ``isort``:

#. Run ``project:fix``
#. Run ``project:format``

It is very likely that you did not configure ``isort`` and/or ``black`` appropriately in your ``pyproject.toml`` file.

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
