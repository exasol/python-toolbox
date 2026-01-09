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
Section :ref:`sonarqube_configuration` gives instructions for public and private repositories.

.. _Exasol Way: https://sonarcloud.io/organizations/exasol/quality_gates/show/AXxvLH-3BdtLlpiYmZhh
