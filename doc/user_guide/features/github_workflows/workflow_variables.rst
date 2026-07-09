.. _workflow_variables:

Workflow Variables
==================

.. _workflow_templates:

Workflow Templates
------------------

Underlying the CLI, the PTB uses Jinja to dynamically generate project-specific
workflows. The rendering process is supported by the ``github_template_dict`` found in
your ``noxconfig.py::PROJECT_CONFIG``. This dictionary is inherited by default from
:py:attr:`exasol.toolbox.config.BaseConfig.github_template_dict`, ensuring a
standardized baseline that can be overridden in individual projects.

.. literalinclude:: ../../../../exasol/toolbox/config.py
  :language: python
  :start-at: github_template_dict
  :end-before: @computed_field

.. _custom_workflow_metadata:

Custom Workflow Metadata
^^^^^^^^^^^^^^^^^^^^^^^^

The PTB extracts metadata from reusable custom workflow files and exposes it
through :py:attr:`exasol.toolbox.config.BaseConfig.github_template_dict` under the
``custom_workflows`` entry. PTB-controlled workflow templates use that metadata
when they call reusable workflows.

.. _custom_workflow_secrets:

Secrets
-------

The PTB extracts secret names from reusable custom workflow files and exposes them
through :py:attr:`exasol.toolbox.config.BaseConfig.github_template_dict` under the
``custom_workflows`` entry. PTB-controlled workflow templates use those extracted
names when they call reusable workflows and forward secrets via ``secrets:``.

To make a custom workflow compatible with this extraction, declare its secrets at the
top of the reusable workflow file under ``on.workflow_call`` and before ``jobs``.
The extractor reads that section and collects the secret names automatically.

For example, ``slow-checks.yml`` can define its reusable workflow header like this:

.. code-block:: yaml

   name: Slow-Checks

   on:
     workflow_call:
       secrets:
         PYPI_TOKEN:
           required: true
         SONAR_TOKEN:
           required: true

Those extracted secret names are then made available to the PTB templates that
reference the custom workflow.

.. _custom_workflow_permissions:

Permissions
-----------

The PTB extracts the effective GitHub permissions required by reusable custom
workflow files. It scans every job in the workflow, reads each job's
``permissions`` block, and combines the results into a single ordered mapping.

When multiple jobs request the same permission, the most permissive level wins
while the first-seen key order is preserved. For example, if one job requests
``contents: read`` and another later job requests ``contents: write``, the final
mapping keeps ``contents`` once, with ``write`` as the level.

Please only configure the minimum required permissions and granting the least required
access. In practice, ``contents: read`` is the most common baseline for workflows, and
other permissions should only be added when a particular step truly requires them.

For example, a custom workflow can declare permissions like this:

.. code-block:: yaml

   name: Slow-Checks

   on:
     workflow_call:

   jobs:
     run-integration-tests:
       permissions:
         contents: read

.. _workflow_matrix:

Matrix Combinations
-------------------

The ``matrix.yml`` is used to generate different combinations of workflow inputs, such
as Python versions, Exasol versions, and any project-specific values exposed by the
config. This lets the PTB render workflows from a single matrix definition instead of
maintaining separate variants.

Extending the Matrix
^^^^^^^^^^^^^^^^^^^^

If you need to expose additional values via the ``matrix.yml``, you can extend
:class:`exasol.toolbox.config.BaseConfig`.

The example adds two additional matrix dimensions: A declared one
`extra_matrix_value` and a computed one `computed_matrix_value`. Each of them
returning only a simple string value.

PTB's Nox task `generate:matrix` will then be able to use each of the these
dimensions when generating a build matrix.

.. code-block:: python

    from pydantic import computed_field

    from exasol.toolbox.config import BaseConfig


    class Config(BaseConfig):
        extra_matrix_value: str = "extra"

        @computed_field  # type: ignore[misc]
        @property
        def computed_matrix_value(self) -> str:
            # This can be requested when generating the matrix. If it is a simple
            # string value, like is shown here, the generator wraps it in an array.
            return f"{self.project_name}-computed"

You can consume the additional value in a workflow by passing the relevant
``matrix_keys_json`` entries when calling ``matrix.yml``:

.. code-block:: yaml

    jobs:
      build-matrix:
        uses: ./.github/workflows/matrix.yml
        with:
          matrix_keys_json: '["extra_matrix_value","computed_matrix_value"]'
