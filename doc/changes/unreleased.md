# Unreleased

## Summary

This version of the PTB adds nox task `artifacts:sonar`, see #451.
This requires the following changes for each public project:
1. specify in the `noxconfig.py` the path to its source code in `Config.source`
2. add the 'SONAR_TOKEN' to the 'Organization secrets' 
3. activate the SonarQubeCloud App
4. create a project on SonarCloud
5. add the following information to their `pyproject.toml`
6. post-merge, update the branch protections to include SonarQube analysis
```toml
[tool.sonar]
projectKey = "com.exasol:<project-key>"
hostUrl = "https://sonarcloud.io"
organization = "exasol"
```

## ✨ Features

* #426: Allowed configuring the python version used for coverage
* #451: Added nox task to execute pysonar & added Sonar to the PTB CI
