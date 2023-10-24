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

        runs-on: ubuntu-latest

        permissions:
          issues: write

        steps:
          - name: SCM Checkout
            uses: actions/checkout@v2

          - name: Report Security Issues
            uses: exasol/python-toolbox/.github/actions/security-issues@feature/security-issues-action
            with:
              format: "maven"
              command: "cat maven-output.json"
              github-token: ${{ secrets.GITHUB_TOKEN }}
