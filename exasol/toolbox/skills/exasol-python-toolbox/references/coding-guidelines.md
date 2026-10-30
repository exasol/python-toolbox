# Guidelines for Projects That Use PTB

PTB is a development dependency. PTB is also a task interface. Keep project
automation aligned with PTB conventions. Change a convention when the project
has a clear reason.

## Configuration and extension

- Keep PTB imports in development code.
- Use `pyproject.toml` for static tool configuration.
- Use `noxconfig.py` and `PROJECT_CONFIG` for dynamic project configuration.
- Use plugin hooks or PTB extension points for project-specific work.
- Keep GitHub workflows as orchestration.

## Project-specific behavior

When a project needs behavior beyond a standard PTB session:

1. Check whether existing `BaseConfig` or `PROJECT_CONFIG` fields solve the
   issue.
2. Check whether a PTB plugin hook applies.
3. Use `.workflow-patcher.yml` for supported workflow changes.
4. Keep a local Nox override scoped to a short-term migration. Create a project
   issue to replace it with configuration, a plugin hook, or a PTB extension
   point.
5. When multiple projects need the same change, consider a PTB template,
   configuration field, or hook.
