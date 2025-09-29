.. _Getting Started:

Getting Started
===============

Your usage of the `exasol-toolbox` will likely fall into one of two scenarios:

#. :ref:`existing`
#. :ref:`new project`

.. _new project:

Creating a New Project with Exasol-Toolbox Support
--------------------------------------------------

.. important::

    To establish a new project with toolbox support, you need to have `Cookiecutter <https://www.cookiecutter.io>`_ installed:

    :code:`pip install cookiecutter`


**1. Create a new project**

Cookiecutter will create the project within the current directory. So if you
usually checkout all your GitHub repos in ``~/git`` you could use ``cd ~/git``
before calling cookiecutter.

Use the following command to create a new project:

.. code-block:: shell

   cookiecutter https://github.com/exasol/python-toolbox.git \
    --checkout <latest-tag> --directory project-template

.. note::

    Without option :code:`--checkout` cookiecutter will use the main branch of the PTB. In order
    to get reliable and reproducible results, we recommend using the tag of PTB's latest released
    version instead.

**2. Follow the interactive project setup prompt**

**3. Bootstrap the development environment**

Navigate to the directory of the newly created project:

.. code-block:: shell

    cd <your-project-name>

Generate a poetry environment for the project:

.. code-block:: shell

    # An example python_version value is python3.10
    poetry env use <python_version>

Install all necessary project and development dependencies for the project:

.. code-block:: shell

    poetry install

**4. Start using your project**

List all available nox sessions:

.. code-block:: shell

    nox -l


.. _existing:

Integrating Exasol-Toolbox into your Project
--------------------------------------------

1. Add the toolbox as a dependency
++++++++++++++++++++++++++++++++++

.. code-block:: shell

    poetry add --group dev exasol-toolbox

2. Provide a project configuration
++++++++++++++++++++++++++++++++++
Make sure you provide the required configuration. Configuration for the exasol-toolbox gets provided by creating
a ``noxconfig.py`` file in the workspace root. This file should be similar to the
example shown below.

.. note::

   For further details on plugins, see the customization section.

.. collapse:: noxconfig.py

    .. literalinclude:: ../../project-template/{{cookiecutter.repo_name}}/noxconfig.py
       :language: python3

3. Configure the tooling
++++++++++++++++++++++++
Configuration values for the tooling should be defined in the ``pyproject.toml``.
Copy the example below & adapt it for your project's specific needs.

.. collapse:: pyproject.toml (tool specific configuration)

    .. literalinclude:: ../../project-template/{{cookiecutter.repo_name}}/pyproject.toml
      :language: toml
      :start-after: # Tooling

For further reference, see the :ref:`formatting code configuration <formatting_configuration>` section.


4. Make the toolbox sessions available
++++++++++++++++++++++++++++++++++++++
To use the standard toolbox session via nox, just import them in your ``noxfile.py``.
If you only need the standard sessions provided by the toolbox, your ``noxfile.py`` is
straightforward, and you just can use the example ``noxfile.py`` below.

.. collapse:: noxfile.py

    .. literalinclude:: ../../project-template/{{cookiecutter.repo_name}}/noxfile.py
       :language: python3


5. Set up the GitHub ``pre-commit`` hooks [optional]
++++++++++++++++++++++++++++++++++++++++++++++++++++

See the :ref:`pre-commit configuration <pre-commit_configuration>` section for the required steps.


6. Set up deploying documentation (optional)
++++++++++++++++++++++++++++++++++++++++++++

See the :ref:`documentation configuration <documentation_configuration>` section for the required steps.

7. Set up Sonar
+++++++++++++++

Look at the configuration of Sonar for a:

* :ref:`configure_sonar_public_project`
* :ref:`configure_sonar_private_project`

8. Go 🥜
+++++++++++++
You are ready to use the toolbox. With ``nox -l`` you can list all available sessions.
