.. _zizmor_configuration:

Configuring Zizmor
==================

``workflow:audit`` uses `zizmor <https://docs.zizmor.sh/>`__ to audit GitHub
Actions and workflows. Zizmor reads its project configuration from a file named
``.zizmor.yml`` in the repository root.

As a starting point, copy the template shipped with the PTB:

.. literalinclude:: ../../../../exasol/toolbox/templates/github/zizmor.yml
  :language: yaml

For troubleshooting help, see :ref:`handle_zizmor_findings`.
