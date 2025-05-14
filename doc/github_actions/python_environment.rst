python-environment
==================
This action prepares everything related to Python for the project to run or to be tested. It involves installing the Python interpreter and Poetry. It also includes creating and activating a Poetry environment, as well as installing the project dependencies, and the project itself, into the Poetry environment.

Parameters
----------
.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Required
     - Default
   * - python-version
     - Python version to use
     - True
     - 3.10
   * - poetry-version
     - Poetry version to use
     - True
     - 2.1.2
   * - working-directory
     - 'Working directory to use'
     - True
     - .
   * - extras
     - Comma-separated list of extras
     - False
     -
   * - use-cache
     - Use cache for poetry environment
     - False
     - true

Example Usage
-------------

.. code-block:: yaml

    name: Checks

    ...

    jobs:

      test-job:
        name: Tests
        runs-on: ubuntu-24.04

        steps:
          - name: SCM Checkout
            uses: actions/checkout@v4

          - name: Setup Python & Poetry Environment
            uses: exasol/python-toolbox/.github/actions/python-environment@0.21.0
            with:
              python-version: 3.12
              poetry-version: 2.1.2
              working-directory: .

            ...
