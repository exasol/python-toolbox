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

Custom Workflow Secrets
^^^^^^^^^^^^^^^^^^^^^^^

If your project needs to pass secrets into project-controlled workflows, configure
the ``custom_workflow_secrets`` field on :class:`exasol.toolbox.config.BaseConfig`.
That field uses :class:`exasol.toolbox.config.CustomWorkflowSecrets` and lets you
define separate secret tuples for specific workflows. See the API reference for
:class:`exasol.toolbox.config.CustomWorkflowSecrets` for the exact structure.

Those custom secrets must be declared at the top of the reusable workflow file, under
``on.workflow_call`` and before ``jobs``. The generated workflows rely on that shape
when they call the reusable workflow with ``secrets:``.

For example, ``slow-checks.yml`` keeps its reusable workflow header at the top of the
file:

.. code-block:: yaml

   name: Slow-Checks

   on:
     workflow_call:
       secrets:
         EXAMPLE_SECRET:
           required: true



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
