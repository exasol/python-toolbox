# 0.16.0 - 2024-11-15

## 🚨 Breaking Changes

* Dropped python 3.8 support
* Changed names of all nox tasks

    | Old Name           | New Name               | Description                                                    |
    |--------------------|------------------------|----------------------------------------------------------------|
    | fix                | project:fix            | Runs all automated fixes on the code base                      |
    | check              | project:check          | Runs all available checks on the project                       |
    | report             | project:report         | Collects and generates metrics summary for the workspace       |
    | unit-tests         | test:unit              | Runs all unit tests                                            |
    | integration-tests  | test:integration       | Runs all the integration tests                                 |
    | coverage           | test:coverage          | Runs all tests (unit + integration) and reports the code coverage |
    | lint               | lint:code              | Runs the static code analyzer on the project                   |
    | type-check         | lint:typing            | Runs the type checker on the project                           |
    | security           | lint:security          | Runs the security linter on the project                        |
    | build-build        | docs:build             | Builds the project documentation                               |
    | open-open          | docs:open              | Opens the built project documentation                          |
    | clean-docs         | docs:clean             | Removes the documentations build folder                        |
    | prepare-release    | release:prepare        | Prepares the project for a new release                         |

## ✨ Added

* Added support for multi version Documentation
* Added nox tasks for building multi-version documentation

## 🐞 Fixed

* Fixed CD workflow template
* Fixed the selection of the latest version in Multi-Version Documentation

## 📚 Documentation

* Added Documentation on Metrics
* Added additional details regarding adjusted sphinx-multiversion 
* Restructured documentation

## 🔩 Internal

* Relocked dependencies