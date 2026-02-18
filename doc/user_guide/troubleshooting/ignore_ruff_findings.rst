.. _ignore_ruff_findings:

Ignoring Ruff Findings
======================

A typical example is when importing all PTB's Nox sessions in your
``noxfile.py``, which may cause ruff to report error "F403 unused import".

You can ignore this finding by appending a comment to the code line:

.. code-block:: python

    from exasol.toolbox.nox.tasks import *  # noqa: F403

See also

* `Ruff documentation <https://docs.astral.sh/ruff/configuration>`_
* :ref:`prevent_auto_format`
