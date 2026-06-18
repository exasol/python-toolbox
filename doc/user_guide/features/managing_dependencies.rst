Managing Dependencies and Vulnerabilities
=========================================

+------------------------------+----------------+-------------------------------------+
| Nox session                  | CI Usage       | Action                              |
+==============================+================+=====================================+
| ``dependency:licenses``      | ``report.yml`` | Uses ``pip-licenses`` to return     |
|                              |                | packages with their licenses        |
+------------------------------+----------------+-------------------------------------+
| ``dependency:audit``         | No             | Uses ``pip-audit`` to report active |
|                              |                | vulnerabilities in our dependencies |
+------------------------------+----------------+-------------------------------------+
| ``vulnerabilities:resolved`` | No             | Uses ``pip-audit`` to report known  |
|                              |                | vulnerabilities in dependencies     |
|                              |                | that have been resolved in          |
|                              |                | comparison to the last release.     |
+------------------------------+----------------+-------------------------------------+
| ``workflow:audit``           | ``checks.yml`` | Uses ``zizmor`` to audit GitHub     |
|                              |                | actions and workflows for security  |
|                              |                | issues and accepts extra zizmor     |
|                              |                | arguments. See                      |
|                              |                | :ref:`zizmor_configuration` for     |
|                              |                | configuration details.              |
+------------------------------+----------------+-------------------------------------+

.. _zizmor_configuration:

Configuring Zizmor
------------------

``workflow:audit`` uses `zizmor <https://docs.zizmor.sh/>`__ to audit GitHub
Actions and workflows. Zizmor reads its project configuration from a file named
``.zizmor.yml`` in the repository root.

As a starting point, copy the template shipped with the PTB:

.. literalinclude:: ../../../exasol/toolbox/templates/github/zizmor.yml
  :language: yaml

For details on the available audit and configuration options, see the
`zizmor documentation <https://docs.zizmor.sh/>`__.

For how to ignore accepted findings, see :ref:`ignore_zizmor_findings`.
