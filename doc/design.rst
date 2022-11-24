📗 Design Document
==================

Motivation
----------
`Unifying tooling <https://exasol.github.io/python-styleguide/guides/tooling.html>`_ is just a the first step
when it comes to reducing cognitive and administrative overhead for maintaining and working on projects.
As a natural next step, common development tasks(e.g. CI/CD), the maintenance of those tasks and updating the tooling
needs to simplified in order to keep the complexity and development & maintenance effort manageable.

This project serves as such a simplification by providing common dev tooling, task, and configuration based on
which common automation (e.g. CI/CD) is provided.

.. note::

    It is obvious that not each project is exactly the same, and we will need to deal with project specifics.
    Still the basic "Developer Front End" (e.g. build automation tasks, CI, etc.) should look the same, but
    may have project specific additions, which ideally reuse existing building blocks of this project.

Overview
---------
This project mainly serves three main purposes:

#. Provide library code, scripts and commands for common developer tasks within a python project.
#. Provide and maintain commonly required functionality for python project
    * Common Projects Tasks
        - apply code formatters
        - lint project
        - type check project
        - run unit tests
        - run integration tests
        - determine code coverage
        - build-, open-, clean- documentation
    * CI (verify PR's and merges)
    * CI/CD (verify and publish releases)
    * Build & Publish Documentation (verify and publish documentation)
    * Provide and enforce configuration settings (code formatter & co.)
#. Provide usage examples of this common functionality


Design
------

Design Principles
+++++++++++++++++
* This project needs to be thought of as development dependency only!
    - Library code should not imported/used in non development code of the projects
* Convention over configuration
    - Being able to assume conventions reduces the code base/paths significantly
    - First thought always should be: Can it be done easily by using/applying convention(s)
    - Use configuration if it's more practical or if it simplifies transitioning projects
* Provide extension points (hooks) where for project specific behaviour
    - If it can't be a convention or configuration setting
    - If having something as a convention or configuration significantly complicates the implementation
    - If you have a obvious use case within at least one project
* KISS (Keep It Stupid Simple)
    - This project shall simplify the work of the developer, not add a burden on top
    - Try to automate as much as possible
    - Try to built on tools which are already in use
        - E.g. documentation related issues ideally should be addressed by extending sphinx

    .. note::

        It is clear that not everything can and will be automated right from the beginning,
        but there should be continues effort to improve the work of the developers.

        e.g.:

             **Template > Generator > Automated Updater**

* YAGNI (You Ain't Gonna Need It)
    - Only add settings, features, extension points etc. when they are explicitly needed

    .. note::

        Every feature needs to have at least one project using it.
        Still if a feature only is used by a single project it is likely rather
        done within that project specifically, once a second project requiring it
        it makes sense to move it into this project.

        Having at least two projects using a feature also will more clearly
        show the commonalities which need to be provided/dealt with.


* SoC (Separation of Concerns)
    .. note::
        Due the nature of the project different concern will be covered by this project

        * Library code
        * Tools
        * Tasks
        * Workflows
        * ...

        Still in order to achieve a specific outcome clear boundaries need to be made/established.

        E.g. when it comes to CI/CD, the infrastructure/tool (Github workflows & actions),
        should only assemble, provide and orchestrate the CI/CD execution.
        The actual task(s) run by this infrastructure/tool, should be an individual defined task
        which can be executed on any machine providing the appropriate environment (e.g. *make* or nox *task*).

* Iteration
    .. note::

        Generally we want to use an integrative approach when adding and developing new functionality.
        E.g.:

        1. Add template(s) and instructions
        2. Provide tooling to generate files, settings etc.
        3. Provide tooling to automagically update und sync files, settings etc.


Design Decisions
++++++++++++++++
* Whenever possible tools provided or required by the toolbox should get their configuration from the projects *pyproject.toml* file.
* Whenever a more dynamic configuration is needed it should be made part of the config object in the projects *noxconfig.py* file.
* The required standard tooling used within the toolbox will obey what have been agreed upon in the exasol `python-styleguide <https://exasol.github.io/python-styleguide/guides/tooling.html>`_.
* As Task runner the toolbox will be using nox
    .. warning:: Known Issue(s)

        Nox tasks should not call (notify) other nox tasks. This can lead to unexpected behaviour
        due to the fact that the job/task queue will `execute a task only once <https://nox.thea.codes/en/stable/config.html#nox.sessions.Session.notify>`_.

        Therefore all functionality which need to be reused or called multiple times within or by different nox tasks,
        should be provided by python code (e.g. functions) which is receiving a nox session as argument
        but isn't  annotated as a nox session/task (`@nox.session <https://nox.thea.codes/en/stable/config.html#defining-sessions>`_).

    .. note::

        Nox was chosen as a task runner because:

        * It is configured in code
        * It is functionality is straightforward and compact
        * It is already used by a couple of our projects, so the team is familiar with it
        * The author of the toolbox is very familiar with it

        That said, no in depth evaluation of other tools haven been done.


* Workflows (CI/CD & Co.) will be github actions based
    - This is the standard tool within the exasol integration team
* Workflows only shall provide an execution environment and orchestrate the execution itself

Detailed Design
+++++++++++++++

Tasks
~~~~~
**TBD:** Add diagram configuration and tasks (noxfile.py + noxconfig.py + exasol.toolbox)

.. list-table::
    :header-rows: 1
    :widths: 30 70

    * - Tasks
      - Description
    * - fix
      - Runs all automated fixes on the code base
    * - check
      - Runs all available checks on the project
    * - lint
      - Runs the linter on the project
    * - type-check
      - Runs the type checker on the project
    * - unit-tests
      - Runs all unit tests
    * - integration-tests
      - Runs the all integration tests
    * - coverage
      - Runs all tests (unit + integration) and reports the code coverage
    * - build-docs
      - Builds the project documentation
    * - open-docs
      - Opens the built project documentation
    * - clean-docs
      - Removes the documentations build folder

Workflows
~~~~~~~~~
**TBD:** Add diagram of github workflows and interaction


Available Workflows
___________________

.. list-table::
    :header-rows: 1
    :widths: 30 70

    * - Workflow
      - Description
    * - checks.yml
      - Verifies the project consistency (tests, linting, etc.)
    * - build-and-publish.yml
      - Builds and publishes releases of the project
    * - gh-pages.yml
      - Builds and publishes the project documentation

Available Actions
_________________

.. list-table::
    :header-rows: 1
    :widths: 30 70

    * - Action
      - Description
    * - python-environment
      - Sets up an appropriate poetry based python environment
