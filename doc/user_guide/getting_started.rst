Getting Started
===============

Preparing the Project
---------------------

1. Add the toolbox as dependency
++++++++++++++++++++++++++++++++

.. code-block:: shell

    poetry add --group dev exasol-toolbox

2. Fine tune the .gitignore file
+++++++++++++++++++++++++++++++++
Add the standard documentation output folder (*.html-documentation*) to the *.gitignore*.

.. code-block:: shell

    echo ".html-documentation" >> .gitignore && git add .gitignore && git commit -m "Add documentation build folder to .gitignore"

3. Provide a project configuration
++++++++++++++++++++++++++++++++++
Make sure you provide the required configuration. Configuration for the exasol-toolbox gets provided by creating
a *noxconfig.py* file in the workspace root. This file should contain at least
a single module constant with the name **PROJECT_CONFIG** pointing to an object,
which is required to to provide the following attributes:

* .. py:attribute:: root
    :type: Path

* .. py:attribute:: doc
    :type: Path

* .. py:attribute:: version_file
    :type: Path

Alternatively you can use the *noxconfig.py* file bellow and adjust the value of the attributes if needed:

.. note::

   Be aware that the plugin definitions are completely optional. For further details on plugins, see the customization section.

.. literalinclude:: ../../noxconfig.py
   :language: python3

4. Configure the tooling
++++++++++++++++++++++++
In order to make all standard task work properly you need add the configuration settings bellow to your *pyproject.toml*,
and adjust the following settings to your project needs:

* coverage
    - source
    - fail_under
* pylint
    - fail-under
* mypy (overrides)
    - module

.. literalinclude:: ../../pyproject.toml
    :language: toml
    :start-after: # Tooling

5. Make the toolbox task available
++++++++++++++++++++++++++++++++++
In order to use the standard toolbox task via nox, just import them in your *noxfile.py*.
If you only need the standard tasks provided by the toolbox your *noxfile.py* is straight
forward and you just can use the example *noxfile.py* bellow.

.. literalinclude:: ../../noxfile.py
   :language: python3
   :end-before: # entry point for debugging


.. attention::

    Keep in mind that the current path may not be included in the :code:`PYTHONPATH`, depending on the operating system you are using. This is explained in more detail in this resource: https://fedoraproject.org/wiki/Changes/PythonSafePath. Thus, it might be necessary to properly set the :code:`PYTHONPATH` before running nox. This is because our nox tasks expect the `noxconfig` module to be located within the python path.

    For additional information on resolving this issue, please :ref:`refer to <faq_no_module_noxconfig>`.

        

6. Setup the pre-commit hooks
+++++++++++++++++++++++++++++

#. Add the following .pre-commit-config.yaml to your project root

    .. literalinclude:: ../../.pre-commit-config.yaml
       :language: yaml

#. Enable pre commit hooks for your workspace

    .. code-block:: shell

        poetry run pre-commit install

7. Go 🥜
+++++++++++++
You are ready to use the toolbox. With *nox -l* you can list all available tasks.

.. code-block:: console

    $ nox -l
    Sessions defined in <PATH_TO_YOUR_PROJECT>/noxfile.py:

    * fix -> Runs all automated fixes on the code base
    - check -> Runs all available checks on the project
    - lint -> Runs the linter on the project
    - type-check -> Runs the type checker on the project
    - unit-tests -> Runs all unit tests
    - integration-tests -> Runs the all integration tests
    - coverage -> Runs all tests (unit + integration) and reports the code coverage
    - build-docs -> Builds the project documentation
    - open-docs -> Opens the built project documentation
    - clean-docs -> Removes the documentations build folder
    - report -> Collects and generates a metrics summary for the workspace

    sessions marked with * are selected, sessions marked with - are skipped.


Enjoy!
