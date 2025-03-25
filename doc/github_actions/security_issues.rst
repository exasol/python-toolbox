security-issues
===============

Example Usage
-------------

.. code-block:: yaml

    name: Report Security Issues for Repository

    on:
      schedule:
        # “Every day at 00:00.” (https://crontab.guru)
        - cron: "0 0 * * *"

    jobs:

      report_security_issues:

        name: Report Security Issues

        runs-on: ubuntu-24.04

        permissions:
          issues: write

        steps:
          - name: SCM Checkout
            uses: actions/checkout@v4

          - name: Report Security Issues
            uses: exasol/python-toolbox/.github/actions/security-issues@0.6.1
            with:
              format: "maven"
              command: "cat maven-cve-report.json"
              github-token: ${{ secrets.GITHUB_TOKEN }}

Configuration
-------------
This action exposes 3 configuration parameters `command`_, `format`_ and `github-token`_, for details see
the specific sections below.

command
+++++++

Workspace command which shall be executed in order to check the project's dependencies for CVEs.

.. note::

    The calling workflow needs to make sure the specified command can be executed in the context of the workflow.


format
++++++

Specifies converter which needs to be applied on the output of the provided command.
Currently there are only two converters available

#. maven

    Converts the output of mavens oss plugin into required input format.


#. pass-through

    In case the command itself already outputs the expected input format, the format can be specified as code:`pass-through`.


Input Format
____________

The expect intput format is jsonl (line based json), of the following form:

.. code-block:: python

    { "cve": "<cve-id>", "cwe": "<cwe-id>", "description": "<multiline string>", "coordinates": "<string>", "references": ["<url>", "<url>", ...] }


.. attention::

    The input format may change in the future. Therefore make sure to rather use or contribute a converter for
    a specific format rather than outputting this format by your own tooling.


github-token
++++++++++++
The temporary GitHub token of the workflow needs to be passed into the action (:code:`${{ secrets.GITHUB_TOKEN }}`),
in order to enable the action to query and created GitHub issues.


project
+++++++
Title of the GitHub-Project the created issue(s) shall be associated with (default = None).
To determine the title of an project you can use the GitHub-CLI, see example below.

.. code-block:: shell

    gh project list --owner exasol

    NUMBER  TITLE                             STATE  ID
    ...


Ideas
-----

.. todo::

    Add additional details to the :code:`security.Issue` type


.. todo::

    Consider adapting common CVE report format as input, for additional details
    `see here <https://github.com/CVEProject/cve-schema/blob/master/schema/v5.0/CVE_JSON_5.0_schema.json>`_.
