# Coding Guidelines for PTB Maintenance

PTB is a development dependency and a task interface for Exasol Python
projects. Preserve the conventions that let projects use the same commands and
automation.

Use `doc/design.rst` for PTB design principles. Use the matching user-guide
feature page for current public behavior.

## Design rules

- Treat PTB as development tooling. Keep PTB imports in development code.
- Prefer conventions. Add configuration when a project needs behavior beyond
  the convention.
- Use `pyproject.toml` for static tool configuration.
- Use `noxconfig.py` and `PROJECT_CONFIG` for dynamic project configuration.
- Use plugin hooks or explicit extension points for project-specific work.
- Keep GitHub workflows as orchestration. Put shared task logic in Python
  functions or Nox sessions.
- Add PTB features in response to concrete project needs. Move project logic
  into PTB when multiple projects need the same behavior.
- Define user-facing Nox sessions in `exasol/toolbox/nox/`. Put reusable logic
  below `exasol/toolbox/util/` in functions that receive the Nox `Session` when
  needed.

## Generated projects and workflows

- Check generated workflows after workflow-template changes. Generate them
  when the source template, configuration, or patch intentionally changes
  their output.
- Update the project-template tests when a change affects newly created
  projects.

## Agent skills

- Put downstream runtime skills below `exasol/toolbox/skills/`. The
  `skills:install` session installs every skill in that package into consuming
  projects.
- Put PTB repository skills below `.agents/skills/` so they remain local to the
  repository.
- Limit packaged skills to downstream workflows and public PTB interfaces.
- Cover packaged-skill changes with evaluation cases, packaging tests,
  installation tests, and user documentation.
