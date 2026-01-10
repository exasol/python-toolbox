.. _sonarqube_analysis:

SonarQube Analysis
==================

The PTB supports using `SonarQube Cloud <https://docs.sonarsource.com/sonarqube-server>`__
to analyze, visualize, & track linting, security, & coverage. All of our Python projects
should be evaluated against the `Exasol Way`_ and subscribe to the
`Clean as You Code <https://docs.sonarsource.com/sonarqube-server/9.8/user-guide/clean-as-you-code/>`__
methodology. If code modified in a PR does not satisfy the aforementioned criteria, the
SonarQube analysis fails.

The PTB includes instructions to set up a GitHub bot to display the results of the
Sonar analysis in your pull requests as a stylized comment and workflow result.
Section :ref:`sonar_configuration` gives instructions for public and private repositories.

.. _sonar_configuration:

Configuration
+++++++++++++

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
#. In the ``noxconfig.py``, the relative path to the project's source code is defined with ``Config.sonar_code_path``.
#. Add the following to the project's file ``pyproject.toml``
    .. code-block:: toml

        [tool.sonar]
        projectKey = "<sonar-project-key>"
        host.url = "https://sonarcloud.io"
        organization = "exasol"
        exclusions = "<source_code_directory>/version.py,<source_code_directory>/<directory-to-ignore>/*"

.. note::
    For more information, see the :ref:`General remarks <configuration_general_remarks>` section.


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

.. note::
    For more information, see the :ref:`General remarks <configuration_general_remarks>` section.

.. _Exasol Way: https://sonarcloud.io/organizations/exasol/quality_gates/show/AXxvLH-3BdtLlpiYmZhh
.. _Sonar Matching Patterns: https://docs.sonarsource.com/sonarqube-server/project-administration/adjusting-analysis/setting-analysis-scope/defining-matching-patterns

.. _configuration_general_remarks:

General remarks
^^^^^^^^^^^^^^^^^^^
For additional configuration information, see `Sonar's analysis parameters <https://docs.sonarsource.com/sonarqube-server/2025.1/analyzing-source-code/analysis-parameters>`__ page.

``exclusions``
""""""""""""""
With the value of ``exclusions``, you can exclude files and directories of your
project from Sonar's analysis:

* You can use wildcards, e.g. ``<root>/dir/*.py`` or ``<root>/**/*.py``
* Multiple exclusions can be comma-separated (as shown above).
* For excluding arbitrary directories and files below a specific directory, please use two asterisks, e.g. ``root/abc/**``.

See the `Sonar Matching Patterns`_ for more details.

By default, the nox session ``sonar:check`` only analyses the source code,
as specified by the ``PROJECT_CONFIG.sonar_code_path``, so directories outside of this
are already excluded from being analyzed.
