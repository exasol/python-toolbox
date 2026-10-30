---
name: maintain-ptb
description: "Maintain and extend the Exasol Python Toolbox repository itself. Covers PTB source code, Nox sessions, configuration, workflow templates, packaged agent skills, tests, documentation, and the project template."
---

# Maintain Exasol Python Toolbox

Use this skill for changes to the `python-toolbox` repository. Use the packaged
`exasol-python-toolbox` skill in downstream projects that consume PTB.

## Task routing

Select the reference that matches the task:

- To locate implementation, templates, tests, or documentation, read
  `references/source-routing.md`.
- To change PTB design, source code, Nox sessions, workflow templates, the
  project template, or packaged skills, read `references/coding-guidelines.md`.

## Maintenance rules

- Read the implementation and its tests before changing or explaining exact
  behavior.
- Preserve the standard PTB task interface used by downstream projects.
- Run `project:check` when a change affects shared behavior, CI, or release
  readiness.
- Update tests, user documentation, and `doc/changes/unreleased.md` with public
  behavior changes.
- Keep repository-maintenance guidance in this local skill. Limit skills below
  `exasol/toolbox/skills/` to downstream usage guidance.
