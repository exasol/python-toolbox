Managing dependencies
=====================

+--------------------------+------------------+----------------------------------------+
| Nox session              | CI Usage         | Action                                 |
+==========================+==================+========================================+
| ``dependency:licenses``  | ``report.yml``   | Uses ``pip-licenses`` to return        |
|                          |                  | packages with their licenses           |
+--------------------------+------------------+----------------------------------------+
| ``dependency:audit``     | No               | Uses ``pip-audit`` to return active    |
|                          |                  | vulnerabilities in our dependencies    |
+--------------------------+------------------+----------------------------------------+
