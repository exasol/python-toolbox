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
^^^^^^^^^^^^^^^^^^^^^^^^
1. Specify in the ``noxconfig.py`` the relative path to the project's source code in ``Config.source``
    .. code-block:: python

        source: Path = Path("exasol/<project-source-folder>")
2. Add the 'SONAR_TOKEN' to the 'Organization secrets' in GitHub
3. Activate the `SonarQubeCloud App <https://github.com/apps/sonarqubecloud>`__
4. Create a project on `SonarCloud <https://sonarcloud.io>`__
5. Add the following information to the project's file ``pyproject.toml``
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

.. _configure_sonar_private_project:

**Private** project
^^^^^^^^^^^^^^^^^^^
.. note::
    As of 2025-07-29, we do not currently have a private project configured. Thus,
    these instructions should be scrutinized and refined upon the configuration of one.

1. Specify in the ``noxconfig.py`` the relative path to the project's source code in ``Config.source``
    .. code-block:: python

        source: Path = Path("exasol/<project-source-folder>")
2. Add the individual 'PRIVATE_SONAR_TOKEN' to the 'Organization secrets' in GitHub
3. Activate the `exasonarqubeprchecks App <https://github.com/apps/exasonarqubeprchecks>`__
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

.. _Exasol Way: https://sonarcloud.io/organizations/exasol/quality_gates/show/AXxvLH-3BdtLlpiYmZhh
