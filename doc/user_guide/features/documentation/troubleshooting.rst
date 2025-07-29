Troubleshooting
===============

Duplicated label error when building documentation
--------------------------------------------------

If you have an error similar to this one:
.. :code-block::

    Warning, treated as error:
    integration-test-docker-environment/doc/changes/changes_0.10.0.md:5:duplicate
    label summary, other instance in
    integration-test-docker-environment/doc/changes/changes_0.1.0.md'

then, this might be caused by sphinx extension ``sphinx.ext.autosectionlabel``.
Try to remove this extension in ``doc/conf.py``.


.. _faq_multiversion_build_warnings:

Warning while building multiversion documentation
--------------------------------------------------
When running ``nox -s docs:multiversion``, you receive the following warnings during the build:

.. code-block::

    WARNING: unknown config value 'smv_metadata_path' in override, ignoring
    WARNING: unknown config value 'smv_current_version' in override, ignoring

It is likely that the multiversion extension is not configured in your Sphinx
configuration (``doc/conf.py``). Try adding it to your configuration and rerun the build.

.. code-block:: python

    extensions = [
        ...,
        ...,
        "exasol.toolbox.sphinx.multiversion",
    ]



Missing version selection box in multiversion documentation
------------------------------------------------------------

You have run ``nox -s docs:multiversion``, but you still do not see any version
selection box in the upper right corner before the GitHub symbol.

This is likely due to :ref:`faq_multiversion_build_warnings` or
:ref:`limited_multiversion_documentation`.


.. _limited_multiversion_documentation:

Limited previous versions in multiversion documentation
-------------------------------------------------------

If not all previous versions of the project are available via the version selection box
of the multiversion documentation, it is likely due to the fact that the unavailable
documentation for those versions was not in a compatible format. In other words, there
had not, for those missing versions, been a compatible setup of a Sphinx-based
documentation.

``links:check`` breaks CI build
-------------------------------
``links:check`` is run in the CI ``checks.yml``. If this step fails in the CI, it will
cause the build to break. Please check the output & manually resolve the issues. There
might be some cases where you need to update your ``doc/conf.py`` with specific values
for the allowed options for the
`Linkcheck Builder <https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder>`__.
