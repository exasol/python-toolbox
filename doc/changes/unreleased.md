# Unreleased

## Summary
This version of the PTB adds nox task `sonar:check`, see #451. This allows us to
use SonarQube Cloud to analyze, visualize, & track linting, security, & coverage. In
order to properly set it up, you'll need to do the following instruction for each **public** project.
At this time, PTB currently does not support setting up SonarQube for a **private** project.

1. Specify in the `noxconfig.py` the relative path to the project's source code in `Config.source`
    ```python
        source: Path = Path("exasol/toolbox")
    ```
2. Add the 'SONAR_TOKEN' to the 'Organization secrets' in GitHub (this requires a person being a GitHub organization owner).
3. Activate the SonarQubeCloud App
4. Create a project on SonarCloud
5. Add the following information to the project's file `pyproject.toml`
    ```toml
        [tool.sonar]
        projectKey = "com.exasol:<project-key>"
        hostUrl = "https://sonarcloud.io"
        organization = "exasol"
    ```
6. Post-merge, update the branch protections to include SonarQube analysis

## ✨ Features
* #451: Added nox task to execute pysonar & added Sonar to the CI
* #409: Doc link & checks

## ⚒️ Refactorings
* #451: Reduced scope of nox tasks `lint:code` (pylint) and `lint:security` (bandit) to analyze only the package code