Common PTB Nox Sessions
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 24 48 28
   :header-rows: 1

   * - Session
     - Purpose
     - More information
   * - ``format:fix``
     - Apply automated formatting and cleanup fixes.
     - :ref:`formatting_code`
   * - ``format:check``
     - Verify formatting without changing files.
     - :ref:`formatting_code`
   * - ``project:check``
     - Run the main local quality gate across formatting, linting, typing, and coverage.
     - :ref:`features`
   * - ``lint:code``
     - Run ``pylint`` and write ``.lint.json``.
     - :doc:`/user_guide/features/metrics/collecting_metrics`
   * - ``lint:typing``
     - Run ``mypy`` over the project.
     - :ref:`features`
   * - ``lint:security``
     - Run ``bandit`` and write ``.security.json``.
     - :doc:`/user_guide/features/metrics/collecting_metrics`
   * - ``lint:dependencies``
     - Reject git, path, and URL-based Poetry dependencies.
     - :ref:`managing_dependencies`
   * - ``lint:import``
     - Run Import Linter against ``.import_linter_config``.
     - `Import Linter docs <https://import-linter.readthedocs.io/en/stable/>`_
   * - ``test:unit``
     - Run unit tests.
     - :ref:`features`
   * - ``test:integration``
     - Run integration tests, including plugin hooks when configured.
     - :ref:`plugins`
   * - ``test:coverage``
     - Run unit and integration tests and print a combined coverage report.
     - :doc:`/user_guide/features/metrics/collecting_metrics`
   * - ``docs:build``
     - Build the documentation with Sphinx.
     - :ref:`deploying_documentation`
   * - ``docs:multiversion``
     - Build multiversion documentation output.
     - :ref:`deploying_documentation`
   * - ``docs:open``
     - Open the built documentation locally.
     - :ref:`deploying_documentation`
   * - ``docs:clean``
     - Remove built documentation output.
     - :ref:`deploying_documentation`
   * - ``links:list``
     - List documentation links discovered by Sphinx linkcheck.
     - :ref:`deploying_documentation`
   * - ``links:check``
     - Validate documentation links.
     - :ref:`deploying_documentation`
   * - ``changelog:updated``
     - Fail if ``doc/changes`` was not updated.
     - :ref:`deploying_documentation`
   * - ``workflow:generate``
     - Render PTB workflow templates into ``.github/workflows``.
     - :ref:`GitHub Workflows`
   * - ``workflow:check``
     - Compare checked-in workflows to generated PTB output.
     - :ref:`GitHub Workflows`
   * - ``workflow:audit``
     - Run ``zizmor`` against workflows and actions.
     - :ref:`managing_dependencies`
   * - ``matrix:generate``
     - Emit selected ``BaseConfig`` values as JSON for workflow matrices.
     - :ref:`GitHub Workflows`
   * - ``matrix:python``
     - Deprecated Python-only matrix output.
     - :ref:`GitHub Workflows`
   * - ``matrix:exasol``
     - Deprecated Exasol-only matrix output.
     - :ref:`GitHub Workflows`
   * - ``matrix:all``
     - Deprecated combined matrix output.
     - :ref:`GitHub Workflows`
   * - ``artifacts:copy``
     - Combine coverage artifacts and copy report inputs into the project root.
     - :doc:`/user_guide/features/metrics/collecting_metrics`
   * - ``artifacts:validate``
     - Validate ``.lint.json``, ``.security.json``, and ``.coverage`` before Sonar upload.
     - :doc:`/user_guide/features/metrics/collecting_metrics`
   * - ``sonar:check``
     - Generate ``ci-coverage.xml`` and upload code-quality data to Sonar.
     - :doc:`/user_guide/features/metrics/collecting_metrics`
   * - ``dependency:licenses``
     - Print dependency license information.
     - :ref:`managing_dependencies`
   * - ``dependency:audit``
     - Report known dependency vulnerabilities with ``pip-audit``.
     - :ref:`managing_dependencies`
   * - ``vulnerabilities:resolved``
     - Report vulnerabilities resolved since the last release.
     - :ref:`managing_dependencies`
   * - ``package:check``
     - Build the package and verify the long description with ``twine check``.
     - :ref:`features`
   * - ``release:prepare``
     - Bump the version, prepare changelog files, create a release branch, and optionally open a pull request.
     - :doc:`/user_guide/features/creating_a_release`
   * - ``release:update``
     - Refresh the prepared release changelog.
     - :doc:`/user_guide/features/creating_a_release`
   * - ``release:trigger``
     - Create and push the release tag.
     - :doc:`/user_guide/features/creating_a_release`

Notes
+++++

* The old task name ``test:typing`` is obsolete. The current session name is ``lint:typing``.
* The ``matrix:python``, ``matrix:exasol``, and ``matrix:all`` sessions are deprecated. Prefer ``matrix:generate``.
