.. _format_check_reports_unmodified_files:

Format Check Reports Unmodified Files
=====================================

Sometimes ``checks.yml`` or ``format:check`` reports formatting issues in
files that have not been modified.

This is likely due to one of our tools (i.e. ``black``) being upgraded. Within the
``pyproject.toml`` of the PTB, dependencies are specified to allow
compatible versions or a restricted version range (i.e., ``^6.0.1``, ``>=24.1.0,<26.0.0``).
Such specifications should restrict major reformatting changes to coincide only with a
new major version of the PTB. However, sometimes a tool's versioning may not properly
adhere to semantic versioning.

If you encounter this scenario, please:

#. Ensure that your ``pyproject.toml`` has the PTB restricted to compatible versions
   (i.e., ``^1.7.0``).
#. Identify which tool is trying to reformat files that you did not modify.
#. Reset your ``poetry.lock`` to align with what's in the project's **default branch**.
#. More selectively update your ``poetry.lock`` with `poetry update <package-name>`.
#. Share with your team which tool & version led to the unexpected changes. So that
   other PTB users do not experience the same difficulties, we will update the PTB with
   a patch version to avoid this tool's version and later do a major release to better
   indicate the breaking changes. You could later create an issue in your GitHub
   repository to update to the new major version of the PTB & do the reformatting.
