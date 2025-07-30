Collecting metrics
==================

.. toctree::
    :maxdepth: 2

    project_report
    sonar

.. _direct_metrics:

Direct metrics
++++++++++++++

The PTB allows you to collect various metrics on the quality of your project
regarding Coverage, Security, and Static Code Analysis.

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

These metrics are computed for each point in your build matrix, e.g. for each
Python version defined in the file ``noxconfig.py``:

.. code-block:: python

    @dataclass(frozen=True)
    class Config:
        python_versions = ["3.9", "3.10", "3.11", "3.12", "3.13"]

The GitHub workflows of your project can:

* Use a build matrix, e.g. using different Python versions as shown above
* Define multiple test sessions, e.g. for distinguishing fast vs. slow or expensive tests.


Reporting metrics
+++++++++++++++++

Currently, the PTB offers two methods to aggregate the :ref:`direct_metrics`
into a report:

#. the nox session ``project:report``
    This is an Exasol-specific summarization tool. For more information, see :ref:`project_report`.

#. SonarQube analysis
    This summarization tool feeds into a feature-rich UI provided by
    `Sonar <https://docs.sonarsource.com/sonarqube-server/latest/>`__. For further
    details, see :ref:`sonarqube_analysis`

Both of these reporting options require that the generated files from the :ref:`direct_metrics`
are existing and in the expected formats. As we have metrics for different Python
versions, we pass on the metrics associated with the Python version named first in
attribute ``python_versions`` of class ``Config`` to the reporting metrics tools.

To perform this validation, we have defined two nox sessions. Due to the direct
dependence on the nox session ``project:report`` and SonarQube Analysis on the
aforementioned nox sessions, all of these are executed in succession in the CI's ``report.yml``.

+--------------------------+----------------------------------------------------------+
| Nox session              | Actions                                                  |
+==========================+==========================================================+
| ``artifacts:copy``       | * Combines coverage artifacts from various test sources  |
|                          |   (unit, integration ...)                                |
|                          | * Copies downloaded artifacts to their parent directory  |
+--------------------------+----------------------------------------------------------+
| ``artifacts:validate``   | * Verifies that the ``.lint.json``, ``.lint.txt``,       |
|                          |   ``.security.json``, and ``.coverage`` are present      |
|                          | * Checks that each file contains the expected attributes |
|                          |   for that file type                                     |
+--------------------------+----------------------------------------------------------+
