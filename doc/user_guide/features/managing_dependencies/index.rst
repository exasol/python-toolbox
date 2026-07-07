.. _managing_dependencies:

Managing Dependencies and Vulnerabilities
=========================================

.. toctree::
   :maxdepth: 1

   zizmor_configuration

.. list-table::
   :widths: 25 20 55
   :header-rows: 1

   * - Nox session
     - CI Usage
     - Action
   * - ``dependency:licenses``
     - ``report.yml``
     - Uses ``pip-licenses`` to return packages with their licenses.
   * - ``dependency:audit``
     - No
     - Uses ``pip-audit`` to report active vulnerabilities in our dependencies.
   * - ``vulnerabilities:resolved``
     - No
     - Uses ``pip-audit`` to report known vulnerabilities in dependencies that
       have been resolved in comparison to the last release.
   * - ``vulnerabilities:update``
     - ``dependency-update.yml``
     - Uses ``pip-audit`` to update dependencies and commit ``poetry.lock`` when
       vulnerabilities are found. It also produces a concise JSON summary for
       the pull request description.
   * - ``workflow:audit``
     - ``checks.yml``
     - Uses ``zizmor`` to audit GitHub actions and workflows for security issues
       and accepts extra zizmor arguments. See :ref:`zizmor_configuration`.
