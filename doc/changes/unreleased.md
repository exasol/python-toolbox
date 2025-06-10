# Unreleased

## Summary
This version of the PTB adds nox task `artifacts:sonar`, see #451. This allows us to
use SonarQube Cloud to analyze, visualize, & track linting, security, & coverage. In
order to properly set it up, you'll need to do the following instruction for each **public** project.
At this time, we do not currently support setting up SonarQube for a **private** project.

1. specify in the `noxconfig.py` the relative path to the project's source code in `Config.source`
    ```python
        source: Path = Path("exasol/toolbox")
    ```
2. add the 'SONAR_TOKEN' to the 'Organization secrets'
3. activate the SonarQubeCloud App
4. create a project on SonarCloud
5. add the following information to the project's `pyproject.toml`
    ```toml
        [tool.sonar]
        projectKey = "com.exasol:<project-key>"
        hostUrl = "https://sonarcloud.io"
        organization = "exasol"
    ```
6. post-merge, update the branch protections to include SonarQube analysis

## ✨ Features
* #451: Added nox task to execute pysonar & added Sonar to the CI

## ⚒️ Refactorings
* #451: Reduced scope of nox tasks `lint:code` (pylint) and `lint:security` (bandit) to analyze only the package code