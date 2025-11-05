.. _sonarqube_analysis:

SonarQube analysis
==================

The PTB supports using `SonarQube Cloud <https://docs.sonarsource.com/sonarqube-server>`__
to analyze, visualize, & track linting, security, & coverage. All of our Python projects
should be evaluated against the `Exasol Way`_ and subscribe to the
`Clean as You Code <https://docs.sonarsource.com/sonarqube-server/9.8/user-guide/clean-as-you-code/>`__
methodology. If code modified in a PR does not satisfy the aforementioned criteria, the
SonarQube analysis fails.

The PTB includes instructions to set up a GitHub bot to display the results of the
Sonar analysis in your pull requests as a stylized comment and workflow result.
Section :ref:`configuration` gives instructions for public and private repositories.

.. _configuration:

Configuration
+++++++++++++

.. note::
   For additional configuration information, see
   `Sonar's analysis parameters <https://docs.sonarsource.com/sonarqube-server/2025.1/analyzing-source-code/analysis-parameters>`__ page.

.. _configure_sonar_public_project:

**Public** GitHub repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In GitHub
"""""""""
A GitHub Admin will need to:

#. Inherit organization secret 'SONAR_TOKEN'
#. Activate the `SonarQubeCloud App <https://github.com/apps/sonarqubecloud>`__
#. **Post-merge**: update the branch protections to include SonarQube analysis.

  * This should only be done when tests exist for the project, & that the project is
    at a state in which enforced code coverage would not be a burden. If you do
    not enact branch protections, it is recommended to create an issue to do so later.

In Sonar
""""""""
#. Create a project on `SonarCloud <https://sonarcloud.io>`__

  * Project key should follow this pattern, e.g. ``com.exasol:python-toolbox``
  * To alter the project further, you will need the help of a SonarQube Admin.

In the code
"""""""""""
#. Specify in the ``noxconfig.py`` the relative path to the project's source code in ``Config.source``
    .. code-block:: python

        source: Path = Path("exasol/<source-directory>")
#. Add the following to the project's file ``pyproject.toml``
    .. code-block:: toml

        [tool.sonar]
        projectKey = "<sonar-project-key>"
        host.url = "https://sonarcloud.io"
        organization = "exasol"
        exclusions = "<source-directory>/version.py,<source_directory>/<directory-to-ignore>/*"

.. _configure_sonar_private_project:

**Private** GitHub repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. note::
    As of 2025-07-29, these instructions have not been used. Thus, they should be
    scrutinized and refined when they are used to configure a private repository.

In GitHub
"""""""""
A GitHub Admin will need to:

#. Add the individual 'PRIVATE_SONAR_TOKEN' to the 'Organization secrets'
#. Activate the `exasonarqubeprchecks App <https://github.com/apps/exasonarqubeprchecks>`__
#. **Post-merge**: update the branch protections to include SonarQube analysis.

  * This should only be done when tests exist for the project, & that the project is
    at a state in which enforced code coverage would not be a burden. If you do
    not enact branch protections, it is recommended to create an issue to do so later.

In Sonar
""""""""
An IT Admin will need to:

#. Create a project on https://sonar.exasol.com

  * Project key should follow this pattern, e.g. ``com.exasol:python-toolbox``


In the code
"""""""""""
#. Specify in the ``noxconfig.py`` the relative path to the project's source code in ``Config.source``
    .. code-block:: python

        source: Path = Path("exasol/<source-directory>")

#. Add the following to the project's file ``pyproject.toml``
    .. code-block:: toml

        [tool.sonar]
        projectKey = "com.exasol:<project-key>"
        host.url = "https://sonar.exasol.com"
        organization = "exasol"
        exclusions = "<source-directory>/version.py,<source_directory>/<directory-to-ignore>/*"

.. _Exasol Way: https://sonarcloud.io/organizations/exasol/quality_gates/show/AXxvLH-3BdtLlpiYmZhh
