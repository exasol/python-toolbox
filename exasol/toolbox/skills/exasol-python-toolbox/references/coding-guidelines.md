# Coding Guidelines for PTB Work

PTB is a development dependency. PTB is also a task interface. Keep project
automation aligned with PTB conventions. Change the convention only if the
project has a clear reason.

Use controlled technical English in user-facing text. Use short sentences. Put
one instruction in one sentence when possible. Use consistent terms.

## Sources to read

- `doc/design.rst`: PTB design rules and task boundaries.
- `doc/user_guide/getting_started.rst`: setup and integration.
- `doc/user_guide/features/formatting_code/index.rst`: format tools and format
  sessions.
- `doc/user_guide/features/creating_a_release.rst`: release procedure.
- Exasol Python styleguide tooling reference:
  `https://exasol.github.io/python-styleguide/guides/tooling.html`

## Design rules to keep

- Treat PTB as development tooling.
- Do not import PTB from production package code.
- Use conventions first.
- Add configuration only when a convention is not sufficient.
- Use `pyproject.toml` for static tool configuration.
- Use `noxconfig.py` and `PROJECT_CONFIG` for dynamic project configuration.
- Use plugin hooks or PTB extension points for project-specific work.
- Make project-specific work operate with standard sessions.
- Keep GitHub workflows as orchestration.
- Put shared task logic in Python functions or nox sessions.
- Do not put shared task logic directly in workflow YAML.
- Do not make nox sessions notify other nox sessions for shared task logic.
- Put shared nox logic in functions that receive the nox `Session`.
- Add a PTB feature only when a real project needs it.
- Move logic into PTB when more than one project needs it.

## Code change rules

Use PTB sessions to format and validate code.

When you change public operation, update the related tests. Update
`doc/changes/unreleased.md` when the project requires a changelog entry.

For workflow-template changes, check generated workflows. Generate workflows
only when you intend to change them. Use `nox-sessions.md` for command syntax.

## Project-specific differences

If a standard PTB session is not correct for a project:

1. Check whether existing `BaseConfig` or `PROJECT_CONFIG` fields solve the
   issue.
2. Check whether a PTB plugin hook applies.
3. Use `.workflow-patcher.yml` for supported workflow changes.
4. Use a local nox override only as a short-term migration step.
5. If multiple projects need the same change, consider a PTB template,
   configuration field, or hook.
