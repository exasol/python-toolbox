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


.. _faq_multiversion_build_warnings:

Warning while building multiversion documentation
--------------------------------------------------
When running ``nox -s docs:multiversion``, I receive the following warnings during the build:

.. code-block::

    WARNING: unknown config value 'smv_metadata_path' in override, ignoring
    WARNING: unknown config value 'smv_current_version' in override, ignoring

If you receive the warnings above, it is very likely that the multiversion extension is not configured in your Sphinx configuration (``conf.py``). Try adding it to your configuration and rerun the build.

.. code-block:: python

    extensions = [
        ...,
        ...,
        "exasol.toolbox.sphinx.multiversion",
    ]


.. _faq_multiversion_selection_missing:

Missing Version Selection Box in Multiversion Documentation
------------------------------------------------------------

I have run ``nox -s docs:multiversion``, but I still do not see any version selection box in the upper right corner before the GitHub symbol.

This likely is likely due to :ref:`faq_multiversion_build_warnings`


.. _faq_multiversion_limited_versions:

Limited Previous Versions in Multiversion Documentation
-------------------------------------------------------

If not all previous versions of the project are available via the version selection box of the multiversion documentation, it is likely due to the fact that the unavailable documentation for those versions was not in a compatible format (there hasn't been a compatible setup of a Sphinx-based documentation).
