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
     --directory project-template

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
a ``noxconfig.py`` file in the workspace root. This file should contain at least
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

3. Configure the tooling
++++++++++++++++++++++++
In order to make all standard task work properly, you need add the configuration settings below to your ``pyproject.toml``,
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

4. Make the toolbox tasks available
+++++++++++++++++++++++++++++++++++
In order to use the standard toolbox task via nox, just import them in your ``noxfile.py``.
If you only need the standard tasks provided by the toolbox, your ``noxfile.py`` is straight
forward, and you just can use the example ``noxfile.py`` below.

.. literalinclude:: ../../noxfile.py
   :language: python3
   :end-before: # entry point for debugging


.. attention::

    Keep in mind that the current path may not be included in the :code:`PYTHONPATH`, depending on the operating system you are using. This is explained in more detail in this resource: https://fedoraproject.org/wiki/Changes/PythonSafePath. Thus, it might be necessary to properly set the :code:`PYTHONPATH` before running nox. This is because our nox tasks expect the `noxconfig` module to be located within the python path.

    For additional information on resolving this issue, please :ref:`refer to <faq_no_module_noxconfig>`.



5. Set up the pre-commit hooks [optional]
+++++++++++++++++++++++++++++++++++++++++

#. Add a :code:`.pre-commit-config.yaml` file to your project root

    If you want to reuse Nox tasks in the pre-commit hooks, feel free to get some inspiration from the Python toolbox itself:

    .. literalinclude:: ../../.pre-commit-config.yaml
       :language: yaml

#. Enable pre-commit hooks for your workspace

    .. code-block:: shell

        poetry run -- pre-commit install --hook-type pre-commit --hook-type pre-push

.. _toolbox tasks:

6. Set up deploying documentation (optional)
++++++++++++++++++++++++++++++++++++++++++++

See :ref:`documentation_configuration` for the required steps.

7. Set up for Sonar
+++++++++++++++++++
PTB supports using SonarQube Cloud to analyze, visualize, & track linting, security, &
coverage. All of our Python projects are evaluated against the
`Exasol Way <https://sonarcloud.io/organizations/exasol/quality_gates/show/AXxvLH-3BdtLlpiYmZhh>`__
and subscribe to the
`Clean as You Code <https://docs.sonarsource.com/sonarqube-server/9.8/user-guide/clean-as-you-code/>`__
methodology, which means that SonarQube analysis will fail and, if its included in the branch protections, block a PR
if code modified in that PR does not meet the standards of the Exasol Way.

In order to set up Sonar, you will need to perform the following instructions.

For a **public** project
^^^^^^^^^^^^^^^^^^^^^^^^
1. Specify in the `noxconfig.py` the relative path to the project's source code in `Config.source`
    .. code-block:: python

        source: Path = Path("exasol/<project-source-folder>")
2. Add the 'SONAR_TOKEN' to the 'Organization secrets' in GitHub (this requires a person being a GitHub organization owner)
3. Activate the `SonarQubeCloud App <https://github.com/apps/sonarqubecloud>`_
4. Create a project on SonarCloud
5. Add the following information to the project's file `pyproject.toml`
    .. code-block:: toml

        [tool.sonar]
        projectKey = "com.exasol:<project-key>"
        hostUrl = "https://sonarcloud.io"
        organization = "exasol"
        exclusions = "<source-directory>/version.py,<source_directory>/<directory-to-ignore>/*"
6. Post-merge, update the branch protections to include SonarQube analysis

  * This should only be done when tests exist for the project, & that the project is
    at a state in which enforced code coverage would not be a burden. For new projects,
    we recommend creating an issue to add the SonarQube analysis to the branch protections
    at a later point. In such scenarios, SonarQube analysis will still report its analysis
    results to the PR, but it will not prevent the PR from being merged.

For a **private** project
^^^^^^^^^^^^^^^^^^^^^^^^^
1. Specify in the `noxconfig.py` the relative path to the project's source code in `Config.source`
    .. code-block:: python

        source: Path = Path("exasol/<project-source-folder>")
2. Add the 'PRIVATE_SONAR_TOKEN' to the 'Organization secrets' in GitHub (this requires a person being a GitHub organization owner)
3. Activate the `exasonarqubeprchecks App <https://github.com/apps/exasonarqubeprchecks>`_
4. Create a project on https://sonar.exasol.com
5. Add the following information to the project's file `pyproject.toml`
    .. code-block:: toml

        [tool.sonar]
        projectKey = "com.exasol:<project-key>"
        hostUrl = "https://sonar.exasol.com"
        organization = "exasol"
        exclusions = "<source-directory>/version.py,<source_directory>/<directory-to-ignore>/*"
6. Post-merge, update the branch protections to include SonarQube analysis from exasonarqubeprchecks

  * This should only be done when tests exist for the project, & that the project is
    at a state in which enforced code coverage would not be a burden. For new projects,
    we recommend creating an issue to add the SonarQube analysis to the branch protections
    at a later point. In such scenarios, SonarQube analysis will still report its analysis
    results to the PR, but it will not prevent the PR from being merged.

8. Go 🥜
+++++++++++++
You are ready to use the toolbox. With ``nox -l`` you can list all available tasks.

.. code-block:: console

    $ nox -l
    Sessions defined in <PATH_TO_YOUR_PROJECT>/noxfile.py:

    * project:fix -> Runs all automated fixes on the code base
    - project:check -> Runs all available checks on the project
    - project:report -> Collects and generates metrics summary for the workspace
    - test:unit -> Runs all unit tests
    - test:integration -> Runs the all integration tests
    - test:coverage -> Runs all tests (unit + integration) and reports the code coverage
    - lint:code -> Runs the static code analyzer on the project
    - lint:typing -> Runs the type checker on the project
    - lint:security -> Runs the security linter on the project
    - lint:dependencies -> Checks if only valid sources of dependencies are used
    - docs:multiversion -> Builds the multiversion project documentation
    - docs:build -> Builds the project documentation
    - docs:open -> Opens the built project documentation
    - docs:clean -> Removes the documentations build folder
    - release:prepare -> Prepares the project for a new release.

    sessions marked with * are selected, sessions marked with - are skipped.


Enjoy!

.. note::

    The targets and their names may change over time, so the list below may not be up to date, as it is not automatically generated yet. Therefore, if you find discrepancies, please `submit a quick PR <https://github.com/exasol/python-toolbox/compare>`_ to address them.
