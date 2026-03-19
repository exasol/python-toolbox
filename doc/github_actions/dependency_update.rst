dependency-update
=================

This workflow updates the project dependencies using Poetry.

It first runs a dependency audit via ``nox -s dependency:audit`` and then updates the dependencies using ``poetry update``.
If the ``poetry.lock`` file changes, a pull request is created automatically.

Example Usage
-------------

.. code-block:: bash

    tbx workflow install dependency-update