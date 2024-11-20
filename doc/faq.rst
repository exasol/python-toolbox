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

.. _faq_duplicated_label_error:

Duplicated label error when building documentation
--------------------------------------------------

Similar error to :code:`Warning, treated as error: integration-test-docker-environment/doc/changes/changes_0.10.0.md:5:duplicate label summary, other instance in integration-test-docker-environment/doc/changes/changes_0.1.0.md'`, might be caused by sphinx extension `sphinx.ext.autosectionlabel`. Try to remove this extension in `doc/conf.py`.
