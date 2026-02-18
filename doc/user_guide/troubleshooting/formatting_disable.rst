.. _prevent_auto_format:

Prevent Auto Format
===================

Sometimes you need to disable auto format in specific places.

Usually, automatic formatting is helpful, but there are rare cases where a
developer might want to ignore automatically applied formatting.

.. note::
 To ensure that automatic formatting remains useful, developers should always
 seek to use the minimum fix reasonable for the affected code. In most cases,
 this would mean adding a comment for a single line.

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
| (example with F401)   |                                |                       |
|                       |   <line-to-ignore> # noqa: F401|    # ruff: noqa F401  |
+-----------------------+--------------------------------+-----------------------+

See also :ref:`ignore_ruff_findings`.
