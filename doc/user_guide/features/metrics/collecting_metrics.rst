Collecting Metrics
==================

The PTB allows you to collect various metrics on the quality of your project
regarding Coverage, Security, and Static Code Analysis.

.. toctree::
   :maxdepth: 2
   :hidden:

   sonar
   ignore_findings

.. _generated_metrics:

Generating Metrics
++++++++++++++++++

For each metric, there is a dedicated nox session, generating one or multiple
files and based on a selected external Python tool.

+------------------------------------+-----------------------------+--------------+
| Nox session                        | Generated files             | Based on     |
+====================================+=============================+==============+
| ``lint:code``                      | ``lint.txt``, ``lint.json`` | ``pylint``   |
+------------------------------------+-----------------------------+--------------+
| ``lint:security``                  | ``.security.json``          | ``bandit``   |
+------------------------------------+-----------------------------+--------------+
| ``test:unit -- --coverage``        | ``.coverage``               | ``coverage`` |
+------------------------------------+-----------------------------+--------------+
| ``test:integration -- --coverage`` | ``.coverage``               | ``coverage`` |
+------------------------------------+-----------------------------+--------------+

These metrics are computed for each element in your build matrix, e.g. for each
Python version defined in the `PROJECT_CONFIG` of the ``noxconfig.py`` file.

The GitHub workflows of your project can:

* Use a build matrix, e.g. using different Python versions as shown above
* Define multiple test sessions, e.g. for distinguishing fast vs. slow or expensive tests.


Reporting Metrics
+++++++++++++++++

The PTB uses only the metrics associated with the Python version specified by
:meth:`exasol.toolbox.config.BaseConfig.minimum_python_version`.

Nox session ``sonar:check`` uploads the :ref:`findings <generated_metrics>` to
:ref:`SonarQube <sonarqube_analysis>` for aggregation and additional static
code analysis, presenting the results in Sonar's `feature-rich UI
<https://docs.sonarsource.com/sonarqube-server>`__.

The CI workflow ``report.yml`` runs ``sonar:check`` after two additional Nox
sessions collect the artifacts from various jobs:

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
