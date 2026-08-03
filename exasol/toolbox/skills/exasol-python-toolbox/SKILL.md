---
name: exasol-python-toolbox
description: Use this skill in Exasol Python projects that use exasol-toolbox/PTB. Use it for PTB setup, nox sessions, code checks, GitHub workflows, updates, releases, and PTB configuration. Use it when an agent must not replace PTB automation.
---

# Exasol Python Toolbox

Use PTB as the task interface for Exasol Python repositories. Use the nox
sessions, configuration, templates, and hooks from the installed
`exasol-toolbox` package. Do not replace them with manual commands. Use direct
tool commands only to isolate a failure.

Use controlled technical English. Use short sentences. Put one instruction in
one sentence when possible. Use the same term for the same item.

## Operating rules

1. Confirm that the project uses PTB before you act:
   - `pyproject.toml` contains a dependency on `exasol-toolbox`.
   - `noxfile.py` imports from `exasol.toolbox.nox.tasks`.
   - `noxconfig.py` defines `PROJECT_CONFIG`.
2. Run commands with Poetry. If the project gives a different command, use it.
3. Use `references/nox-sessions.md` for session names and command syntax.
4. Before you edit generated workflow files, use PTB workflow sessions,
   `.workflow-patcher.yml`, `PROJECT_CONFIG`, or PTB hooks.
5. Do not run Black, isort, Ruff, Pylint, Mypy, Pytest, Coverage, Sphinx,
   Poetry build, Twine, or zizmor directly when a PTB nox session does the same
   work. Use direct tool commands only for fault isolation.

## Task routing

Read only the reference that the task needs:

- Source files and resource files for exact PTB operation:
  `references/source-routing.md`
- Setup, code changes, CI fixes, releases, PTB updates, dependency updates, and
  workflow maintenance: `references/common-workflows.md`
- Nox session names, arguments, outputs, and limits:
  `references/nox-sessions.md`
- Coding rules, PTB design rules, and rules for PTB extension:
  `references/coding-guidelines.md`

## Source rule

The skill does not copy PTB source code. Source copies can become old. Use this
skill to find the correct file. Read the file from the repository before you
change or explain exact PTB operation.

## Release safety

`release:trigger` creates git tags. It pushes the tags. Run it only when the
user asks you to trigger a release.

Before you run `release:trigger`:

1. Confirm that `release:prepare` ran and its PR is merged.
2. Confirm that the current branch is the default branch.
3. Confirm that the current branch is at the latest remote commit.
4. Confirm that the current project version has no git tag and no GitHub
   release.
5. Confirm that the current project version is newer than the latest release,
   unless the user confirms a different release plan.

Use `references/common-workflows.md` for the release workflow.
