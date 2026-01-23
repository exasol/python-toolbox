Dependencies
============

Core Dependencies
-----------------

- Python >= 3.10
- `Poetry <https://python-poetry.org/docs/#installing-with-the-official-installer>`__ >= 2.3.0
  - `poetry export <https://github.com/python-poetry/poetry-plugin-export>`__

Supported Poetry Versions by PTB
--------------------------------

.. list-table:: PTB Poetry Version Compatibility
   :header-rows: 1

   * - PTB Version
     - Default in PTB
     - Range Allowed
     - Migration Information
   * - >=1.0.0, <5.0.0
     - 2.1.2
     - >=2.1.0,<3.0
     - None
   * - >=5.0.0
     - 2.3.0
     - >=2.3.0,<3.0
     - :ref:`migration_to_2.3.x`

Migration Information
---------------------

.. _migration_to_2.3.x:

From Poetry ``2.1.x`` to ``2.3.0``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is **highly** encouraged that a developer update their ``pyproject.toml`` and
system-wide Poetry installation to most use effectively use Poetry ``2.3.0``:

#. In your terminal, update your system-wide Poetry version:

    .. code-block:: bash

        poetry self update 2.3.0

#. In your project's ``pyproject.toml``, update the ``requires-poetry`` value:

    .. code-block:: toml

        requires-poetry = ">=2.3.0"

#. In your terminal, execute ``poetry check`` and resolve any listed issues
#. In your terminal, run ``poetry lock`` to update the lock
#. (optional but recommended) In your project's ``pyproject.toml``, update it to fit:
    * `PEP-621 <https://peps.python.org/pep-0621/>`__
    * `PEP-735 <https://peps.python.org/pep-0735/>`__

    .. note::
        Note that `uvx migrate-to-uv <https://github.com/mkniewallner/migrate-to-uv>`__
        seems to do a good job with automating many of the PEP-related changes.
        Though, a developer should take care to verify the changes, as some are unneeded
        as it completes the migration to ``uv`` which the PTB does NOT yet support.
