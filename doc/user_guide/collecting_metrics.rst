Collecting Metrics
==================

PTB allows you to collect various metrics on the quality of your project
regarding Coverage, Security, and Static Code Analysis.

For each metric, there is a dedicated nox task, generating one or multiple
files and based on a selected external python tool.

+-----------------------------+-----------------------------+--------------+
| Nox Task                    | Generated Files             | Based on     |
+=============================+=============================+==============+
| ``lint:code``               | ``lint.txt``, ``lint.json`` | ``pylint``   |
+-----------------------------+-----------------------------+--------------+
| ``lint:security``           | ``.security.json``          | ``bandit``   |
+-----------------------------+-----------------------------+--------------+
| ``test:unit -- --coverage`` | ``.coverage``               | ``coverage`` |
+-----------------------------+-----------------------------+--------------+

The metrics are computed for each point in your build matrix, e.g. for each
Python version defined in file ``noxconfig.py``:

.. code-block:: python

    @dataclass(frozen=True)
    class Config:
        python_versions = ["3.9", "3.10", "3.11", "3.12", "3.13"]

The GitHub workflows of your project can:

* Use a build matrix, e.g. using different python versions as shown above
* Define multiple test sessions, e.g. for distinguishing fast vs. slow or expensive tests.

PTB combines the coverage data of all test sessions but using only the python
version named first in attribute ``python_versions`` of class ``Config``.
