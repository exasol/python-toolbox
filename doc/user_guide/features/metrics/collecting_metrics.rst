Measuring Code Quality
======================

The PTB uses various Nox sessions incl. linting and tests to collect code-quality data
and upload the results to Sonar for aggregation and review.

.. toctree::
   :maxdepth: 2
   :hidden:

   sonar
   ignore_findings

.. _generated_metrics:

Overview
++++++++

The PTB code-quality flow has three stages:

1. Run linting and test sessions that generate artifact files.
2. Collect and validate those artifacts in ``report.yml``.
3. Upload the consolidated results with ``sonar:check``.

The individual tools still produce the raw data, but Sonar is the main place
where PTB projects review the combined results in CI.


Generate Code Quality Results
+++++++++++++++++++++++++++++

For each result type, there is a dedicated nox session, generating one or multiple
files and based on a selected external Python tool.

+------------------------------------+-----------------------------+--------------+
| Nox session                        | Generated files             | Based on     |
+====================================+=============================+==============+
| ``lint:code``                      | ``.lint.json``              | ``pylint``   |
+------------------------------------+-----------------------------+--------------+
| ``lint:security``                  | ``.security.json``          | ``bandit``   |
+------------------------------------+-----------------------------+--------------+
| ``test:unit -- --coverage``        | ``.coverage``               | ``coverage`` |
+------------------------------------+-----------------------------+--------------+
| ``test:integration -- --coverage`` | ``.coverage``               | ``coverage`` |
+------------------------------------+-----------------------------+--------------+

These results are computed for each element in your build matrix, e.g. for each
Python version defined in the `PROJECT_CONFIG` of the ``noxconfig.py`` file.

The GitHub workflows of your project can use a build matrix and multiple test
workflows, for example to distinguish fast and slow tests.


Report Code Quality Results
+++++++++++++++++++++++++++

The PTB uses only the results associated with the Python version specified by
:meth:`exasol.toolbox.config.BaseConfig.minimum_python_version`.

In CI, workflow ``report.yml`` downloads the previously generated artifacts and
then runs the following Nox sessions:

+--------------------------+----------------------------------------------------------+
| Nox session              | Actions                                                  |
+==========================+==========================================================+
| ``artifacts:copy``       | * Combines coverage artifacts from various test sources  |
|                          |   (unit, integration ...)                                |
|                          | * Copies downloaded artifacts to their parent directory  |
+--------------------------+----------------------------------------------------------+
| ``artifacts:validate``   | * Verifies that the ``.lint.json``, ``.security.json``,  |
|                          |   and ``.coverage`` are present                          |
|                          | * Checks that each file contains the expected attributes |
|                          |   for that file type                                     |
+--------------------------+----------------------------------------------------------+
| ``sonar:check``          | * Creates ``ci-coverage.xml`` from ``.coverage``         |
|                          | * Uploads lint, security, and coverage data to Sonar     |
+--------------------------+----------------------------------------------------------+

After that, Sonar becomes the main review surface for combined PTB code-quality results.


Configure Sonar
+++++++++++++++

See :ref:`sonarqube_analysis` for the repository, secret, and
``pyproject.toml`` configuration needed for Sonar.


Handle Findings
+++++++++++++++

See :ref:`ignore_findings` if a Sonar finding cannot be fixed immediately and
must be explicitly accepted or ignored.
