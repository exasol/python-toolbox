.. _sonarqube_analysis:

SonarQube analysis
==================

The PTB supports using SonarQube Cloud to analyze, visualize, & track linting, security,
& coverage. All of our Python projects should be evaluated against the `Exasol Way`_
and subscribe to the
`Clean as You Code <https://docs.sonarsource.com/sonarqube-server/9.8/user-guide/clean-as-you-code/>`__
methodology. If code modified in a PR does not satisfy the aforementioned criteria, we
will receiving a failing (red) SonarQube analysis.

Additionally, per project, we enact a GitHub bot (differs based on :ref:`configuration`,
which reports the status of the Sonar analysis into a PR as a stylized comment and as
a workflow result. Depending on the overall state of a project (i.e. new vs established),
we can require the passing of the workflow result in the branch protections, which means
that a passing Sonar analysis would be required for merging a PR.

.. _configuration:

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
    at a state in which enforced code coverage would not be a burden. For new projects,
    we recommend creating an issue to add the SonarQube analysis to the branch protections
    at a later point. In such scenarios, SonarQube analysis will still report its analysis
    results to the PR, but it will not prevent the PR from being merged.

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
        hostUrl = "https://sonarcloud.io"
        organization = "exasol"
        exclusions = "<source-directory>/version.py,<source_directory>/<directory-to-ignore>/*"

.. _configure_sonar_private_project:

**Private** GitHub repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. note::
    As of 2025-07-29, we do not currently have a private project configured. Thus,
    these instructions should be scrutinized and refined upon the configuration of one.

In GitHub
"""""""""
A GitHub Admin will need to:

#. Add the individual 'PRIVATE_SONAR_TOKEN' to the 'Organization secrets'
#. Activate the `exasonarqubeprchecks App <https://github.com/apps/exasonarqubeprchecks>`__
#. **Post-merge**: update the branch protections to include SonarQube analysis.

  * This should only be done when tests exist for the project, & that the project is
    at a state in which enforced code coverage would not be a burden. For new projects,
    we recommend creating an issue to add the SonarQube analysis to the branch protections
    at a later point. In such scenarios, SonarQube analysis will still report its analysis
    results to the PR, but it will not prevent the PR from being merged.

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
        hostUrl = "https://sonar.exasol.com"
        organization = "exasol"
        exclusions = "<source-directory>/version.py,<source_directory>/<directory-to-ignore>/*"

.. _Exasol Way: https://sonarcloud.io/organizations/exasol/quality_gates/show/AXxvLH-3BdtLlpiYmZhh
