.. _Getting Started:

Getting Started
===============

Your usage of the `exasol-toolbox` will likely fall into one of two scenarios:

#. Integration into an existing project.

    If this is your situation, proceed to the section titled :ref:`Integrating Exasol-Toolbox into your Project <existing>`.

#. Creation of a new project.

    If you are starting a new project, please read the section :ref:`Create a New Project with Exasol-Toolbox Support <new project>`.

.. _new project:

Create a New Project with Exasol-Toolbox Support
-------------------------------------------------

.. important::

    To establish a new project with toolbox support, you need to have `Cookiecutter <https://www.cookiecutter.io>`_ installed.

    **TL;DR:**
        :code:`pipx install cookiecutter`


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

    poetry shell

Install all necessary project and development dependencies for the project:

.. code-block:: shell

    poetry install

**4. Start using your project**

List all available nox tasks:

.. code-block:: shell

    nox -l


.. _existing:

Integrating Exasol-Toolbox into your Project
--------------------------------------------

1. Add the toolbox as dependency
++++++++++++++++++++++++++++++++

.. code-block:: shell

    poetry add --group dev exasol-toolbox

2. Provide a project configuration
++++++++++++++++++++++++++++++++++
Make sure you provide the required configuration. Configuration for the exasol-toolbox gets provided by creating
a ``noxconfig.py`` file in the workspace root. This file should be similar to the
example shown below.

.. note::

   For further details on plugins, see the customization section.

.. literalinclude:: ../../project-template/{{cookiecutter.repo_name}}/noxconfig.py
   :language: python3

3. Configure the tooling
++++++++++++++++++++++++
Configuration values for the tooling should be defined in the ``pyproject.toml``.
Copy the example below & adapt it for your project's specific needs.

.. literalinclude:: ../../project-template/{{cookiecutter.repo_name}}/pyproject.toml
  :language: toml
  :start-after: # Tooling

For further reference, see the specific configurations for:

* :ref:`formatting code <formatting_configuration>`


4. Make the toolbox tasks available
+++++++++++++++++++++++++++++++++++
To use the standard toolbox task via nox, just import them in your ``noxfile.py``.
If you only need the standard tasks provided by the toolbox, your ``noxfile.py`` is
straightforward, and you just can use the example ``noxfile.py`` below.

.. literalinclude:: ../../project-template/{{cookiecutter.repo_name}}/noxfile.py
   :language: python3


.. attention::

    Keep in mind that the current path may not be included in the :code:`PYTHONPATH`, depending on the operating system you are using. This is explained in more detail in this resource: https://fedoraproject.org/wiki/Changes/PythonSafePath. Thus, it might be necessary to properly set the :code:`PYTHONPATH` before running nox. This is because our nox tasks expect the `noxconfig` module to be located within the python path.

    For additional information on resolving this issue, please :ref:`refer to <faq_no_module_noxconfig>`.

5. Set up the pre-commit hooks [optional]
+++++++++++++++++++++++++++++++++++++++++

#. Add a :code:`.pre-commit-config.yaml` file to your project root

    If you want to reuse Nox tasks in the pre-commit hooks, feel free to get some inspiration from the Python toolbox itself:

    .. literalinclude:: ../../project-template/{{cookiecutter.repo_name}}/.pre-commit-config.yaml
       :language: yaml

#. Enable pre-commit hooks for your workspace

    .. code-block:: shell

        poetry run -- pre-commit install --hook-type pre-commit --hook-type pre-push

.. _toolbox tasks:

6. Set up deploying documentation (optional)
++++++++++++++++++++++++++++++++++++++++++++

See :ref:`documentation_configuration` for the required steps.

7. Set up Sonar
+++++++++++++++

Look at the configuration of Sonar for a:

* :ref:`configure_sonar_public_project`
* :ref:`configure_sonar_private_project`

8. Go 🥜
+++++++++++++
You are ready to use the toolbox. With ``nox -l`` you can list all available tasks.
