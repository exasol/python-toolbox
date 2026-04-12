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
