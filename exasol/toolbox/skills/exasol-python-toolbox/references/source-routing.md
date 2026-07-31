# Source Routing

Use this reference to find the source file for exact PTB operation.
Read the source file before you change code.
Read the source file before you explain a detailed rule.

## Project entry points

- `pyproject.toml`: package data, dependencies, tool configuration, and
  packaged resources.
- `noxfile.py`: local nox entry point.
- `noxconfig.py`: local `PROJECT_CONFIG` and release hooks.
- `README.rst`: project overview.
- `doc/design.rst`: PTB design rules.

## PTB configuration

- `exasol/toolbox/config.py`: `BaseConfig`, computed configuration fields,
  supported versions, paths, workflow variables, and plugin validation.
- `exasol/toolbox/nox/plugin.py`: nox plugin hooks.

## PTB nox sessions

- `exasol/toolbox/nox/_artifacts.py`: artifact validation, artifact copy, and
  Sonar upload sessions.
- `exasol/toolbox/nox/_dependencies.py`: dependency audit, license,
  vulnerability, and SBOM sessions.
- `exasol/toolbox/nox/_documentation.py`: documentation, link check, and
  changelog sessions.
- `exasol/toolbox/nox/_format.py`: `format:fix` and `format:check`.
- `exasol/toolbox/nox/_lint.py`: `lint:code`, `lint:typing`, and
  `lint:security`.
- `exasol/toolbox/nox/_matrix.py`: matrix output sessions for CI usage.
- `exasol/toolbox/nox/_package.py`: package validation.
- `exasol/toolbox/nox/_release.py`: release preparation, release update, and
  release trigger sessions.
- `exasol/toolbox/nox/_test.py`: `test:unit`, `test:integration`, and
  `test:coverage`.
- `exasol/toolbox/nox/_workflow.py`: workflow check, generation, and audit
  sessions.

## PTB nox support files

- `exasol/toolbox/nox/_shared.py`: old shared nox helpers. Prefer
  `exasol/toolbox/util/` for new code that more than one session uses.
- `exasol/toolbox/nox/tasks.py`: exported nox session list. Import new nox
  session modules here so projects that use PTB can import them with
  `from exasol.toolbox.nox.tasks import *`. Do not add new session code here.

## PTB tools

Do not add new functions under `exasol/toolbox/tools/`. Put reusable code in
`exasol/toolbox/util/`. Prefer a nox session for new user-facing operations.

- `exasol/toolbox/tools/issue.py`: issue template CLI.
- `exasol/toolbox/tools/replace_version.py`: version replacement helpers.
- `exasol/toolbox/tools/security.py`: security issue conversion and creation.
- `exasol/toolbox/tools/tbx.py`: CLI root.
- `exasol/toolbox/tools/template.py`: template list, show, diff, install, and
  update helpers.

## Workflow templates and helpers

- `exasol/toolbox/templates/github/workflows/`: packaged GitHub workflow
  templates.
- `exasol/toolbox/templates/github/`: packaged GitHub templates and zizmor
  configuration.
- `exasol/toolbox/util/workflows/`: workflow rendering, patching, validation,
  and custom workflow extraction.
- `.workflow-patcher.yml`: PTB workflow patch configuration for this repository.
- `.github/workflows/`: generated repository workflows.
- `.github/actions/`: repository GitHub actions.

## Release and dependency helpers

- `exasol/toolbox/util/dependencies/`: dependency audit, license report,
  dependency change, vulnerability tracking, and dependency update helpers.
- `exasol/toolbox/util/git.py`: git helper functions.
- `exasol/toolbox/util/release/`: changelog, release notes, and Cookiecutter
  version helpers.
- `exasol/toolbox/util/version.py`: version parsing and version upgrade logic.

## Documentation and project template

- `doc/user_guide/`: user tasks and feature documentation.
- `doc/developer_guide/`: developer and plugin documentation.
- `doc/api/`: API documentation entry points.
- `doc/changes/`: changelog files.
- `project-template/`: Cookiecutter template for new PTB projects.

## Tests

- `test/unit/`: unit tests for PTB operation.
- `test/integration/`: integration tests.
- `test/integration/project-template/`: tests for the Cookiecutter project
  template.
