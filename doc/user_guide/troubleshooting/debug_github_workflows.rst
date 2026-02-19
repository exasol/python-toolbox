.. _debug_workflows_troubleshooting:

Debugging Generated GitHub Workflows
====================================

This troubleshooting guide is helpful if you run into issues installing or updating
the GitHub workflows provided by the PTB.

Enabling Debug Logging
----------------------

To get more detailed output, set the ``LOG_LEVEL`` environment variable to ``DEBUG`` before executing a CLI command.
By default, the ``LOG_LEVEL`` is set to ``INFO``.

.. code-block:: bash

   export LOG_LEVEL=DEBUG

Checking Custom Exceptions
----------------------------

Certain pain points are associated with custom exceptions. These give a brief statement
on what could be wrong and in which file. For further information, check the traceback.

For the list of the custom exceptions for installing or updating the GitHub workflows,
see the :ref:`workflow_exceptions`.
