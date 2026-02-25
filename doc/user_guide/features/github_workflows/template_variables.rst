.. _template_variables:

Template Variables
==================

Underlying the CLI, the PTB uses Jinja to dynamically generate project-specific
workflows. The rendering process is supported by the ``github_template_dict`` found in
your ``noxconfig.py::PROJECT_CONFIG``. This dictionary is inherited by default from
:py:attr:`exasol.toolbox.config.BaseConfig.github_template_dict`, ensuring a
standardized baseline that can be easily overridden, if necessary.

.. literalinclude:: ../../../../exasol/toolbox/config.py
  :language: python
  :start-at: github_template_dict
  :end-before: @computed_field
