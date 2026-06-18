.. _managing_dependencies:

Managing Dependencies and Vulnerabilities
=========================================

.. toctree::
   :maxdepth: 1

   zizmor_configuration

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
|                              |                | :ref:`zizmor_configuration`.        |
+------------------------------+----------------+-------------------------------------+

