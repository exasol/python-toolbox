.. _GitHub Workflows:

GitHub Workflow Templates
=========================

.. toctree::
    :maxdepth: 1
    :hidden:

    github_project_configuration
    create_and_update
    template_variables
    workflow_patcher

The PTB ships with configurable GitHub workflow templates covering the most common
CI/CD setup variants for Python projects. The templates are defined in:
`exasol/toolbox/templates/github/workflows <https://github.com/exasol/python-toolbox/tree/main/exasol/toolbox/templates/github/workflows>`__.

The PTB provides a command line interface (CLI) for generating and updating actual
workflows from the templates.

.. code-block:: bash

    poetry run -- nox -s workflow:generate --help

.. attention::

   In most cases, we recommend using _all_ workflows without change to ensure
   consistent interdependencies. For more details, see :ref:`ci_actions`.


Workflows
---------

The PTB has two categories of workflows:
  #. those maintained by the PTB, which can be modified using the :ref:`workflow_patcher`.
  #. those which extend the PTB-provided workflows and are maintained by the project (not the PTB).

Maintained by the PTB
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Filename
     - Run on
     - Description
   * - ``build-and-publish.yml``
     - Workflow call
     - Packages the distribution and publishes it to PyPi and GitHub.
   * - ``cd.yml``
     - Push with new tag
     - Manages continuous delivery by calling ``check-release-tag.yml``,
       ``build-and-publish.yml``, and ``gh-pages.yml``. See :ref:`cd_yml`
       for a graph of workflow calls.
   * - ``check-release-tag.yml``
     - Workflow call
     - Verifies that the release tag matches the project's internal versioning.
   * - ``checks.yml``
     - Workflow call
     - Executes many small & fast checks: builds documentation and validates
       cross-references (AKA. "links") to be valid, and runs various linters
       (security, type checks, etc.).
   * - ``ci.yml``
     - Pull request
     - Executes the continuous integration suite by calling ``merge-gate.yml`` and
       ``report.yml``. See :ref:`ci_yml` for a graph of workflow calls.
   * - ``fast-tests.yml``
     - Workflow call
     - Executes unit tests.
   * - ``gh-pages.yml``
     - Workflow call
     - Builds the documentation and deploys it to GitHub Pages.
   * - ``matrix-all.yml``
     - Workflow call
     - Calls Nox session ``matrix:all``, which typically evaluates ``exasol_versions``
       and ``python_versions`` from the ``PROJECT_CONFIG``.
   * - ``matrix-exasol.yml``
     - Workflow call
     - Calls Nox session ``matrix:exasol`` to get the ``exasol_versions`` from the
       ``PROJECT_CONFIG``.
   * - ``matrix-python.yml``
     - Workflow call
     - Calls Nox session ``matrix:python`` to get the ``python_versions`` from the
       ``PROJECT_CONFIG``.
   * - ``merge-gate.yml``
     - Workflow call
     - Acts as a final status check (gatekeeper) to ensure all required CI steps have
       passed before allowing to merge the branch of your pull request to the
       default branch of the repository. e.g. ``main``.
   * - ``periodic-validation.yml``
     - weekly
     - Acts as a periodic validator that critical checks and tests are working as
       expected. See :ref:`periodic_validation_yml` for a graph of workflow calls.
   * - ``pr-merge.yml``
     - Push to main
     - Runs ``gh-pages.yml``. See :ref:`pr_merge_yml` for a graph of called workflows.
   * - ``report.yml``
     - Workflow call
     - Downloads results from code coverage analysis and linting,
       creates a summary displayed by GitHub as result of running
       the action, and uploads the results to Sonar.
   * - ``slow-checks.yml``
     - Workflow call
     - Runs long-running checks, which typically involve an Exasol database instance.

Workflow Extensions
^^^^^^^^^^^^^^^^^^^

To use a workflow extension, a user must simply add the file to their project's
``.github/workflows`` directory. The PTB checks that this file exists, and if it does,
then it automatically activates calling that workflow in the relevant parent workflow.

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Filename
     - Run on
     - Description
   * - ``fast-tests-extension.yml``
     - Workflow call
     - This extends the ``fast-tests.yml`` and should include additional fast tests.
   * - ``merge-gate-extension.yml``
     - Workflow call
     - This extends the ``merge-gate.yml`` and the ``needs`` criteria of the job
       ``allow-merge``. This extension is used to define additional requirements
       to the ``merge-gate``, and it is most likely to include costly slows checks or
       tests. It's encouraged to add to this workflow extension additional approval
       requests, similar to ``approve-run-slow-tests``.

.. _ci_actions:

CI Actions
----------

.. _ci_yml:

Pull Request
^^^^^^^^^^^^

When any pull request is opened, synchronized, or reopened, then the ``ci.yml`` will be
triggered.

When configured as described on :ref:`github_project_configuration`, the
``run-slow-tests`` job requires a developer to manually approve executing the slower
workflows, like ``slow-checks.yml``. This allows developers to update their pull
request more often and to only periodically run the more time-expensive tests.

The ``report.yml`` is called twice:

#. after the steps in ``checks.yml`` successfully finish - this allows developers
   to get faster feedback for linting, security, and unit test coverage.
#. after the steps in ``slow-checks.yml`` successfully finish - this gives developers an
   overview of the total coverage, as well as the information provided from running
   the ``checks.yml``

In both scenarios, the results are posted in the PR and made available on Sonar's UI.
Note that Sonar does not keep historical information, so it will only show the latest
information provided to it.

If one of the jobs in the chain fails (or if ``run-slow-tests`` is not approved),
then the subsequent jobs will not be started.

.. mermaid::

    graph TD
        %% Define Nodes
        checks[checks.yml]
        ci_job[ci.yml]
        fast-report[1st call to report.yml]
        fast-tests[fast-tests.yml]
        gate[merge-gate.yml]
        slow_run[run-slow-tests]
        slow_checks[slow-checks.yml]
        report[2nd call to report.yml]

        approver[approve-merge]

        %% Workflow Triggers
        ci_job --> gate
        gate --> checks
        gate --> fast-tests
        gate --> slow_run
        slow_run -.->|needs| slow_checks

        %% Dependencies
        checks -.->|needs| approver
        checks -.->|needs| fast-report
        fast-tests -.->|needs| fast-report
        fast-tests -.->|needs| approver
        slow_checks -.->|needs| approver
        approver -.->|needs| report

        %% Styling
        style approver fill:#fff,stroke:#333,stroke-dasharray: 5 5
        style slow_run fill:#fff,stroke:#333,stroke-dasharray: 5 5

.. _pr_merge_yml:

Merge
^^^^^

When a pull request is merged to main, then the ``pr-merge.yml`` workflow is activated.

.. mermaid::
   :name: merge-diagram

    graph TD
        %% Workflow Triggers (Solid Lines)
        pr-merge[pr-merge.yml] --> publish-docs[publish-docs.yml]

.. _cd_yml:

Release
^^^^^^^

When the nox session ``release:trigger`` is used, a new tag is created & pushed
to main. This starts the release process by activating the ``cd.yml`` workflow.

.. mermaid::
    :name: release-diagram

    graph TD
        %% Workflow Triggers (Solid Lines)
        cd[cd.yml] --> check-release-tag[check-release-tag.yml]

        %% Dependencies / Waiting (Dotted Lines)
        check-release-tag -.->|needs| build-and-publish[build-and-publish.yml]
        build-and-publish -.->|needs| gh-pages[gh-pages.yml]

.. _periodic_validation_yml:

Periodic Validation
^^^^^^^^^^^^^^^^^^^

Once a week, this workflow is triggered on the default branch.

.. literalinclude:: ../../../../exasol/toolbox/templates/github/workflows/periodic-validation.yml
   :language: yaml
   :start-at:   schedule:
   :end-at:     - cron: "0 0 * * 6"

.. mermaid::

    graph TD
        %% Define Nodes
        checks[checks.yml]
        periodic_validation[periodic-validation.yml]
        fast-tests[fast-tests.yml]
        slow_checks[slow-checks.yml]
        report[report.yml]

        %% Workflow Triggers
        periodic_validation --> checks
        periodic_validation --> fast-tests
        periodic_validation --> slow_checks

        %% Dependencies
        checks -.->|needs| report
        fast-tests -.->|needs| report
        slow_checks -.->|needs| report
