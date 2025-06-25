# 1.5.0 - 2025-06-18

## Summary
This version of the PTB adds nox task `sonar:check`, see #451. This allows us to
use SonarQube Cloud to analyze, visualize, & track linting, security, & coverage. To
set it up, you'll need to execute the following instructions.

### For a public project
1. Specify in the `noxconfig.py` the relative path to the project's source code in `Config.source`
    ```python
        source: Path = Path("exasol/<project-source-folder>")
   ```
2. Add the 'SONAR_TOKEN' to the 'Organization secrets' in GitHub (this requires a person being a GitHub organization owner)
3. Activate the [SonarQubeCloud App](https://github.com/apps/sonarqubecloud)
4. Create a project on SonarCloud
5. Add the following information to the project's file `pyproject.toml`
    ```toml

        [tool.sonar]
        projectKey = "com.exasol:<project-key>"
        hostUrl = "https://sonarcloud.io"
        organization = "exasol"
   ```
6. Post-merge, update the branch protections to include SonarQube analysis

### For a private project
1. Specify in the `noxconfig.py` the relative path to the project's source code in `Config.source`
    ```python
        source: Path = Path("exasol/<project-source-folder>")
   ```
2. Add the 'PRIVATE_SONAR_TOKEN' to the 'Organization secrets' in GitHub (this requires a person being a GitHub organization owner)
3. Activate the [exasonarqubeprchecks App](https://github.com/apps/exasonarqubeprchecks)
4. Create a project on https://sonar.exasol.com
5. Add the following information to the project's file `pyproject.toml`
    ```toml
        [tool.sonar]
        projectKey = "com.exasol:<project-key>"
        hostUrl = "https://sonar.exasol.com"
        organization = "exasol"
   ```
6. Post-merge, update the branch protections to include SonarQube analysis from exasonarqubeprchecks

## ✨ Features
* #451: Added nox task to execute pysonar & added Sonar to the CI

## ⚒️ Refactorings
* #451: Reduced scope of nox tasks `lint:code` (pylint) and `lint:security` (bandit) to analyze only the package code
