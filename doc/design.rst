.. _design_document:

Design Document
===============

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
.. todo:: Add diagram configuration and tasks (noxfile.py + noxconfig.py + exasol.toolbox)

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
.. todo:: Add diagram of github workflows and interaction


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


Known Issues
------------

This section documents flaws, sins, and known issues with the current design and/or its current implementation that were either known upfront or surfaced through the course of implementing it. Additionally, it attempts to explain why certain choices were made at the time, so one can better understand whether it may be reasonable to make changes now or in the future.

Passing files as individual arguments on the CLI
++++++++++++++++++++++++++++++++++++++++++++++++

**Description:**

As of today selection of python files for litting formatting etc. is done by passing all relevant python files as individual argument(s)
to the tools used/invoked by the python toolbox.

**Downsides:**

- Most shells have limitations on the number of arguments and their length.
- Noisey output, making it hard to decipher the actual command.
- Not ideal for all use cases.

**Rationale/History:**

- The current method of passing files as individual arguments by default offers ease in collection and filtering. It also allows users to simply provide or replace the selection mechanism fairly easily.

- Every tool used by the toolbox (e.g., `black`, `isort`) used to support passing files by argument. However, not all of them provided the same mechanism for selection or deselection patterns (e.g., "glob").

**Ideas/Solutions:**

- Develop a wrapper that allows for different selection mechanisms


Inconsistent Naming
+++++++++++++++++++

**Description:**

The naming is not consistent across the project name (python-toolbox) and the PyPI package name (exasol-toolbox).

**Downsides:**

- Misalignment between the PyPI package name and the project name causes confusion when discussing or referring to the project/package.

**Rationale/History:**

- Initially, this was a proof of concept (POC) to verify a few ideas, and the naming was not well thought out at the time.
- Later, when publishing the first package for distribution, the project name was unavailable on PyPI, resulting in a different name being used on PyPI.

**Ideas/Solutions:**

- `Issue-325 <https://github.com/exasol/python-toolbox/issues/325>`_

Project Configuration
+++++++++++++++++++++

**Description:**
Currently, the documentation regarding the configuration of projects using the toolbox has various gaps and does not follow a clear configuration hierarchy or structure.

**Downsides:**

- Multiple scattered configuration points make management and understanding difficult.
- Configurations overlap or conflict with unclear priorities.
- Tool leakage (e.g., the ``[isort]`` section in ``pyproject.toml``).
  (If everything were done via toolbox config file(s), backing tools could be swapped more easily).

**Rationale/History:**

- Initial decisions aimed to simplify individual adjustments in the projects until we had a better understanding of what needed to be configured.
- Scattering configuration across various files and tools was a hasty decision to expedite development and accommodate various tools.

**Ideas/Solutions:**

Currently used methods to configure toolbox-based projects:

#. Project configuration: ``noxconfig.py``
#. Tool-specific configuration files or sections in ``pyproject.toml``
#. Implementing plugin extension points
#. Overwriting nox tasks with custom implementations
#. Replacing with customized workflows of the same name (only applicable for action/workflows)

Refinement:

- Centralize all toolbox based configurations in a toolbox config file (``noxconfig.py``).
- Rename the toolbox config file from ``noxconfig.py`` to a more appropriate name that reflects its purpose.
- Document configuration hierarchy and usage.


Nox Task Runner
+++++++++++++++

**Description:**
While Nox isn't a perfect fit, it still meets most of our requirements for a task runner.

**Downsides:**

- Imports over top-level modules are problematic as all contained tasks are imported.
- Passing and receiving additional arguments to a task is clunky.
- The default behavior of creating a venv for tasks is undesirable.
- Nox does not support grouping.

**Rationale/History:**

Why Nox was choosen:

- No Additional Language(s) Required: There was no need to introduce extra programming languages or binaries, simplifying the development process.
- Python-based: Being Python-based, Nox can be extended and understood by Python developers.
- Python code: As Nox tasks are defined via Python code, existing scripts can be reused and code can be shared easily.
- Simplicity: Nox is relatively "small" in functionality, making it somewhat simple to use and understand.

**Ideas/Solutions:**

Grouping:

Since Nox doesn't natively support task grouping, we need a strategy to group commands.
Therefore, a naming convention to indicate grouping should be adopted.

    Suggestion: Groups will be separated using a :code:`:` (colon) because :code:`-` (dash) might already be used within task names.

Imports:

Consider modularizing tasks to handle top-level imports better.

Others Issues:

Generally, one may consider addressing the other issues by choosing another task runner or creating a small set of CLI tools and extension points manually provided by the toolbox.


Poetry for Project Management
+++++++++++++++++++++++++++++

**Description:**
The commonly used

**Downsides:**

- There's a potential for another tool that addresses the issues better in the future.
- poetry slightly diverges from stardanrd poetproject.toml e.g. [popetry...]
- no workspaces support

**Rationale/History:**

- Poetry was chosen for project management; however, adjustments and reevaluations might be necessary.
- Initial choice for ease of dependency management and project configuration.

**Ideas/Possible Solutions:**

- uv, workspaces,  scripts ...
- Continuously evaluate alternative tools that might better serve the project's needs.
- Stay updated on the development and new features of Poetry and its competitors.


Code Formatting
+++++++++++++++

**Description:**

Currently we use Black and Isort for code formatting, though running them on a larger code base as pre-commit hooks or such can take quite a bit of time.

**Downsides:**

- Two tools and an aligned configuration of them are required to cleanly and correctly format the codebase.
- Code needs to be processed at least twice as we apply two individual tools.
- The performance of Black and Isort is okay but not great compared to other tools.

**Rationale/History:**

- Black and Isort have been used because they are battle-tested and widely used
- When we opted for Black and Isort, ``ruff`` wasn't "a thing" yet and at best in its early stages.
- Black and Isort already have been known by most python devs when we where selecting the tools

**Ideas/Solutions:**

As `Ruff <https://docs.astral.sh/ruff/>`_ is fairly stable and also tested and used by many Python projects
we should consider transitioning to it.

Advantages:

- Well-tested
- Widely used
- Excellent performance
- Single tool for imports and formatting the codebase
- Simplifies adopting ruff for linting


Pylint Instead of Ruff
+++++++++++++++++++++++

**Description:**

**Downsides:**

- Pylint slower and less usable in pre-commit hooks.

**Rationale/History:**

- Transitioning to Ruff provides better usability and speed for linting processes.
- Pylint was used, but Ruff's emergence offers superior performance in many areas.

**Ideas/Possible Solutions:**

- Tentatively use Ruff for linting:
  - Evaluate impacts on scoring and migration strategy adjustments.
  - Continue using Pylint for evaluation/rating while Ruff is integrated for linting.


Workflows Dependency Structure
++++++++++++++++++++++++++++++

**Description:**

**Downsides:**

- Lack of clear documentation and structure for workflow dependencies.

**Rationale/History:**

- Proper documentation will streamline workflow management and dependency tracing.
- Workflow dependencies were initially structured without thorough documentation.

**Ideas/Possible Solutions:**

- Work out and document dependencies and structure thoroughly.
- Develop a visual or diagrammatic representation to aid comprehension.
- Regularly review and update the documentation to stay current with project evolution.
