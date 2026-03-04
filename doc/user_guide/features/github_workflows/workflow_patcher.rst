.. _workflow_patcher:

Workflow Patcher
================

Underlying the CLI, the PTB uses, if defined, a ``.workflow_patcher.yml`` file to
customize generated project-specific workflows. The rendering process is supported by
the ``github_workflow_patcher_yaml`` found in your ``noxconfig.py::PROJECT_CONFIG``.
This filepath is inherited by default from
:py:attr:`exasol.toolbox.config.BaseConfig.github_workflow_patcher_yaml`
ensuring a standardized baseline that can be easily overridden, if necessary.

.. literalinclude:: ../../../../exasol/toolbox/config.py
  :language: python
  :start-at: github_workflow_patcher_yaml

Model
-------

.. code-block:: yaml

   workflows:
     - name: pr-merge
       remove_jobs:
         - publish-docs
       step_customizations:
         - action: REPLACE | INSERT_AFTER
           job: run-unit-tests
           step_id: check-out-repository
           content:
             - name: Check out Repository
               id: check-out-repository
               uses: actions/checkout@v6
               with:
                 fetch-depth: 0


* ``name``: Name of the GitHub workflow to customize. The PTB supports these workflows:
  `exasol/toolbox/templates/github/workflows <https://github.com/exasol/python-toolbox/tree/main/exasol/toolbox/templates/github/workflows>`__.
* ``remove_jobs``: List of job names to remove from the workflow.
  This is useful when a job like ``publish-docs`` is not applicable for a project.
* ``step_customizations``: List of customizations:

  * ``action``: Type of customization

    * ``REPLACE``: Replace an existing step with the new content
    * ``INSERT_AFTER``: Insert the content **after** the specified step

  * ``job``: Name of the job inside the workflow that should be modified, e.g. ``run-unit-tests``.
  * ``step_id``: ID of the step to replace or after which to insert the new step
  * ``content``: Content of the new step. The PTB does not validate that this will work on
    GitHub, but it does validate that it is valid YAML content.

.. note::

    For more information, see the API documentation for
    :class:`exasol.toolbox.util.workflows.patch_workflow.WorkflowPatcherConfig`.
