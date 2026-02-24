.. _workflow_patcher:

Workflow Patcher
================

Underlying the CLI, the PTB uses, if defined, a ``.workflow_patcher.yml`` file to
customize generated project-specific workflows. The rendering process is supported by
the ``github_workflow_patcher_yaml`` found in your ``noxconfig.py::PROJECT_CONFIG``.
This Path is inherited by default from
:py:attr:`exasol.toolbox.config.BaseConfig.github_workflow_patcher_yaml`
ensuring a standardized baseline that can be easily overridden, if necessary.

.. literalinclude:: ../../../../exasol/toolbox/config.py
  :language: python
  :start-at: github_workflow_patcher_yaml
