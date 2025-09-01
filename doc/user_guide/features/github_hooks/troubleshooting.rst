Troubleshooting
===============

The checks for ``git commit`` or ``git push`` keep failing
----------------------------------------------------------

The ``pre-commit`` hooks, as defined in the ``.pre-commit-config.yaml``
use multiple nox sessions. If a step fails multiple times, despite a user adding fixes
or manually resolving the error, then please check which nox session is failing
and refer to its troubleshooting documentation for help:

* :ref:`Formatting Troubleshooting <formatting_troubleshooting>`
