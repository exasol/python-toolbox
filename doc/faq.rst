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
