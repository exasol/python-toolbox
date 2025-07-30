.. _project_report:

``project:report``
==================
The nox session ``project:report`` provides an overall coverage percentage,
maintainability grade, and security grade based on the :ref:`generated_metrics` collected.
The definitions used for evaluating the quality of the Python code is defined in the
`metrics.py`_ file, and the required fields are specified by the code-agnostic
:ref:`metrics_schema` for Exasol. This nox session can return its analysis in two forms:

* JSON
    This directly meets the requirements for the :ref:`metrics_schema`. In our CI runs,
    a JSON is created & uploaded as an artifact, which can be downloaded later by the
    crawler project.
* markdown
    This is displayed in the GitHub Action's Summary for a given CI run. Displaying
    this content per CI run gives the developer immediate feedback as to how the code
    quality has changed between code modifications.


.. _metrics_schema:

Metrics schema
++++++++++++++
The PTB supports the uniform json schema for metrics used by all projects
of the Exasol Product Integration Team:

* `Exasol Schemas`_
* `Metrics Schema`_
* `Metrics Schema Project`_

For our open-source projects, there is a scheduled job that regularly collects metrics
from projects. This data is then aggregated and added to a central data store. For more
details, please refer to the crawler project documentation.

Development
-----------

If the metrics schema needs to be updated, the `Metrics Schema Project`_ provides a
convenient way (via a Pydantic model) to update and generate an updated schema for the
metrics.

.. note::

   The updated version needs to be first integrated into the `Exasol Schemas Project`_.


.. _Exasol Schemas: https://schemas.exasol.com
.. _Exasol Schemas Project: https://github.com/exasol/schemas
.. _Metrics Schema: https://schemas.exasol.com/project-metrics-0.2.0.html
.. _metrics.py: https://github.com/exasol/python-toolbox/blob/main/exasol/toolbox/metrics.py
.. _Metrics Schema Project: https://github.com/exasol/python-toolbox/tree/main/metrics-schema
