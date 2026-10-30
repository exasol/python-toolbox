# PTB Maintainer Source Routing

Use this reference to find the source file for exact PTB behavior. Read the
implementation and related tests before changing or explaining it.

## Project entry points

- `pyproject.toml`: package data, dependencies, and tool configuration.
- `noxfile.py`: local Nox entry point.
- `noxconfig.py`: PTB's `PROJECT_CONFIG` and release hooks.
- `README.rst`: project overview.
- `doc/design.rst`: PTB design rules.

## Configuration

- `exasol/toolbox/config.py`: `BaseConfig`, computed configuration fields,
  supported versions, paths, workflow variables, and plugin validation.
- `exasol/toolbox/nox/plugin.py`: Nox plugin hooks.

## Nox session modules

- `exasol/toolbox/nox/_artifacts.py`: artifact validation, copy, and Sonar
  upload sessions.
- `exasol/toolbox/nox/_dependencies.py`: dependency, vulnerability, license,
  and SBOM sessions.
- `exasol/toolbox/nox/_documentation.py`: documentation, links, and changelog
  sessions.
- `exasol/toolbox/nox/_format.py`: format fix and check sessions.
- `exasol/toolbox/nox/_lint.py`: code, typing, and security lint sessions.
- `exasol/toolbox/nox/_matrix.py`: matrix output sessions for CI.
- `exasol/toolbox/nox/_package.py`: package validation.
- `exasol/toolbox/nox/_release.py`: release preparation, update, and trigger
  sessions.
- `exasol/toolbox/nox/_skills.py`: packaged-skill validation and installation
  sessions.
- `exasol/toolbox/nox/_test.py`: unit, integration, and coverage sessions.
- `exasol/toolbox/nox/_workflow.py`: workflow check, generation, and audit
  sessions.

## Nox support files

- `exasol/toolbox/nox/_shared.py`: historical shared helpers. Put new reusable
  logic below `exasol/toolbox/util/` when more than one session needs it.
- `exasol/toolbox/nox/tasks.py`: exported session list. Import new session
  modules here so downstream `noxfile.py` files can import the standard tasks.
  Implement sessions in dedicated `_*.py` modules.

## Packaged and repository-local skills

- `.agents/skills/`: repository-local maintenance skills.
- `exasol/toolbox/skills/`: skills packaged in the wheel and installed into
  downstream projects.
- `exasol/toolbox/util/skill_eval.py`: evaluation-case models.
- `exasol/toolbox/util/skills.py`: skill discovery, validation, and
  installation helpers.
- `test/resources/skills/`: evaluation cases for packaged skills.
- `test/unit/skills_test.py`: package, installation, and skill-specific tests.
- `test/unit/util/skill_test.py`: shared validation and installation tests.

## Tools and reusable logic

- `exasol/toolbox/tools/issue.py`: issue-template CLI.
- `exasol/toolbox/tools/replace_version.py`: version replacement helpers.
- `exasol/toolbox/tools/security.py`: security issue conversion and creation.
- `exasol/toolbox/tools/tbx.py`: CLI root.
- `exasol/toolbox/tools/template.py`: template list, show, diff, install, and
  update helpers.
- `exasol/toolbox/util/dependencies/`: dependency audit, licenses, changes,
  vulnerability tracking, and updates.
- `exasol/toolbox/util/git.py`: Git helpers.
- `exasol/toolbox/util/release/`: changelog, release notes, and Cookiecutter
  version helpers.
- `exasol/toolbox/util/version.py`: version parsing and upgrades.

## Workflows, documentation, and templates

- `exasol/toolbox/templates/github/workflows/`: packaged workflow templates.
- `exasol/toolbox/templates/github/`: other packaged GitHub templates and
  zizmor configuration.
- `exasol/toolbox/util/workflows/`: workflow rendering, patching, validation,
  and custom-workflow extraction.
- `.workflow-patcher.yml`: workflow patch configuration for this repository.
- `.github/workflows/`: generated repository workflows.
- `.github/actions/`: repository GitHub actions.
- `doc/user_guide/`: user tasks and feature documentation.
- `doc/developer_guide/`: maintainer and plugin documentation.
- `doc/api/`: API documentation entry points.
- `doc/changes/`: changelog files.
- `project-template/`: Cookiecutter template for new PTB projects.

## Tests

- `test/unit/`: unit tests for PTB behavior.
- `test/integration/`: integration tests.
- `test/integration/project-template/`: generated-project tests.
