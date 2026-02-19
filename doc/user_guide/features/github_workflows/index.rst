.. _GitHub Workflows:

GitHub Workflow Templates
=========================

.. toctree::
    :maxdepth: 1
    :hidden:

    github_project_configuration
    create_and_update
    template_variables

The PTB ships with configurable GitHub workflow templates covering the most common
CI/CD setup variants for Python projects. The templates are defined in:
`exasol/toolbox/templates/github/workflows <https://github.com/exasol/python-toolbox/tree/main/exasol/toolbox/templates/github/workflows>`__.

The PTB provides a command line interface (CLI) for generating and updating actual
workflows from the templates.

.. code-block:: bash

    poetry run -- tbx workflow --help

.. attention::

   In most cases, we recommend using _all_ workflows without change to ensure
   consistent interdependencies. For more details, see :ref:`ci_actions`.


Workflows
---------

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
       cross-references (AKA. "links") to be valid,runs various linters
       (security, type checks, etc.), and unit tests.
   * - ``ci.yml``
     - Pull request and monthly
     - Executes the continuous integration suite by calling ``merge-gate.yml`` and
       ``report.yml``. See :ref:`ci_yml` for a graph of workflow calls.
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
   * - ``pr-merge.yml``
     - Push to main
     - Runs ``checks.yml``, ``gh-pages.yml``, and ``report.yml``. See
       :ref:`pr_merge_yml` for a graph of called workflows.
   * - ``report.yml``
     - Workflow call
     - Downloads results from code coverage analysis and linting,
       creates a summary displayed by GitHub as result of running
       the action, and uploads the results to Sonar.
   * - ``slow-checks.yml``
     - Workflow call
     - Runs long-running checks, which typically involve an Exasol database instance.

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

If one of the jobs in the chain fails (or if ``run-slow-tests`` is not approved),
then the subsequent jobs will not be started.

.. mermaid::

    graph TD
        %% Workflow Triggers (Solid Lines)
        ci[ci.yml] --> merge-gate[merge-gate.yml]
        ci --> metrics[report.yml]

        merge-gate --> fast-checks[checks.yml]
        merge-gate --> run-slow-tests[run-slow-tests]
        run-slow-tests -.->|needs| slow-checks[slow-checks.yml]

        %% Dependencies / Waiting (Dotted Lines)
        fast-checks -.->|needs| approve-merge[approve-merge]
        slow-checks -.->|needs| approve-merge

        %% Final Dependency
        approve-merge -.->|needs| metrics

        %% Visual Styling to distinguish jobs
        style approve-merge fill:#fff,stroke:#333,stroke-dasharray: 5 5
        style run-slow-tests fill:#fff,stroke:#333,stroke-dasharray: 5 5


.. _pr_merge_yml:

Merge
^^^^^

When a pull request is merged to main, then the ``pr-merge.yml`` workflow is activated.

.. mermaid::
   :name: merge-diagram

    graph TD
        %% Workflow Triggers (Solid Lines)
        pr-merge[pr-merge.yml] --> checks[checks.yml]
        pr-merge --> publish-docs[publish-docs.yml]

        %% Dependencies / Waiting (Dotted Lines)
        checks -.->|needs| report[report.yml]

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
