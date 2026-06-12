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
:class:`exasol.toolbox.config.BaseConfig` as shown below.

Declared fields are regular config attributes. Computed fields are derived values
that Pydantic exposes separately via ``@computed_field``. Both can be used as
matrix keys because the matrix generator accepts either kind of config value.

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

Simple string values such as ``computed_matrix_value`` do not need to be wrapped in an
array in ``PROJECT_CONFIG``. The ``matrix.yml`` generation automatically converts them
into arrays for the workflow matrix.
