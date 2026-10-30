---
# Generated and maintained by the exasol-toolbox.
name: exasol-python-toolbox
description: "Use Exasol Python Toolbox (PTB) in projects that consume exasol-toolbox. Covers PTB setup, Poetry, PROJECT_CONFIG, Nox sessions, code checks, GitHub workflows, dependency updates, and releases."
---

# Exasol Python Toolbox

Use PTB as the task interface for Exasol Python projects. Use the Nox
sessions, configuration, templates, and hooks from the installed
`exasol-toolbox` package as the primary task interface. Reserve direct tool
commands for fault isolation.

## Project detection

Confirm that `pyproject.toml` depends on `exasol-toolbox`, `noxfile.py` imports
from `exasol.toolbox.nox.tasks`, and `noxconfig.py` defines `PROJECT_CONFIG`.

## Task routing

Select the reference that matches the task:

- Setup, code changes, CI fixes, releases, PTB updates, dependency updates, and
  workflow maintenance: `references/common-workflows.md`
- Nox session names, arguments, outputs, and limits:
  `references/nox-sessions.md`
- Project coding and extension rules for a project that uses PTB:
  `references/coding-guidelines.md`

## Operating rules

- Run commands with Poetry or the command specified by the project.
- Use the matching PTB Nox session for formatting, linting, testing,
  documentation, packaging, and workflow tasks. Reserve direct tool invocation
  for fault isolation.
- Change generated workflow behavior through PTB workflow sessions,
  `.workflow-patcher.yml`, `PROJECT_CONFIG`, or PTB hooks.

## Release safety

`release:trigger` creates and pushes git tags. Require an explicit user request
before running it.

Before you run `release:trigger`:

1. Confirm that `release:prepare` ran and its PR is merged.
2. Confirm that the current branch is the default branch.
3. Confirm that the current branch is at the latest remote commit.
4. Confirm that the current project version remains untagged and unpublished
   as a GitHub release.
5. Confirm that the current project version is newer than the latest release.
   Follow a different release plan after the user explicitly confirms it.

Use `references/common-workflows.md` for the release workflow.
