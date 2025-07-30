.. _project_report:

``project:report``
==================
After collecting the metrics described in by :ref:`generated_metrics`, you can use the
nox session ``project:report`` to create a report using one of the following formats:

* JSON
    This format is usually used in the CI. The created JSON file is uploaded as an
    artifact, which can be downloaded and aggregated for multiple projects
    (see :ref:`metrics_schema`).
* markdown
    This is displayed in the GitHub Action's summary for a given CI run. Displaying
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

The Integration team runs regular aggregation of the metrics from all projects into a centralized data sink
as decribed in the company Wiki.

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
