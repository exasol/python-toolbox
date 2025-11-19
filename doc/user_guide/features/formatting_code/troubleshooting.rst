.. _formatting_troubleshooting:

Troubleshooting
===============

Formatting still fails after running ``project:fix``
----------------------------------------------------

If when you execute:

#. Run ``project:fix``
#. Run ``project:format``

you receive an error from ``project:format`` (i.e. ``isort`` or ``black``), it it
likely that you need to update your configuration to align with
:ref:`formatting_configuration`.

The automatic formatting is doing x, but we shouldn't do that because of y
---------------------------------------------------------------------------
Usually, automatic formatting is helpful, but there are rare cases where a developer
might want to ignore automatically applied formatting.

.. note::
 To ensure that automatic formatting remains useful, developers should always seek
 to use the minimum fix reasonable for the affected code. In most cases, this would
 mean adding a comment for a single line.

+-----------------------+--------------------------------+-----------------------+
| Undesired Action      | Single line                    | Within a file         |
+=======================+================================+=======================+
| formatting from black | .. code-block:: python                                 |
|                       |                                                        |
|                       |   # fmt: off                                           |
|                       |   <code being ignored by black>                        |
|                       |   # fmt: on                                            |
+-----------------------+--------------------------------+-----------------------+
| formatting from isort | .. code-block:: python         | .. code-block:: python|
|                       |                                |                       |
|                       |   <line-to-ignore> # isort:skip|    # isort:skip_file  |
+-----------------------+--------------------------------+-----------------------+
| formatting from ruff  | .. code-block:: python         | .. code-block:: python|
|                       |                                |                       |
|                       |   <line-to-ignore> # noqa: F401|    # ruff: noqa F401  |
+-----------------------+--------------------------------+-----------------------+


In the ``checks.yml``, ``project:format`` wants me to reformat code I did not modify
------------------------------------------------------------------------------------

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
