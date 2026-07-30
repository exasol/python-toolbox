# Common PTB Workflows

Use these workflows in an Exasol Python repository that uses PTB.
Use `nox-sessions.md` for nox command syntax.

## Set up PTB

For a new project, use the PTB Cookiecutter template.

```bash
cookiecutter https://github.com/exasol/python-toolbox.git \
  --checkout <ptb-release-tag> --directory project-template \
  --overwrite-if-exists
```

Use a released tag. This gives the same setup result each time.

After you create the project, run these commands:

```bash
poetry env use <python-version>
poetry install
```

For an existing project:

1. Add PTB as a development dependency:
   `poetry add --group dev exasol-toolbox`
2. Add or update `noxconfig.py`.
3. Define `PROJECT_CONFIG` in `noxconfig.py`.
4. Import the standard sessions in `noxfile.py`:
   `from exasol.toolbox.nox.tasks import *`
5. Move tool configuration to `pyproject.toml` where PTB expects it.
6. Run `poetry install`.
7. List the available nox sessions.
8. Add optional integrations only when the project needs them. Examples are
   pre-commit hooks, documentation, Sonar, and GitHub workflows.

If a project cannot use a PTB session without changes, use a local override
only as a short-term migration step. For a permanent solution, use
configuration, plugin hooks, or PTB extension points.

## Make a daily code change

1. Read `noxconfig.py`.
2. Read the related tool sections in `pyproject.toml`.
3. Make the requested code change, document change, or configuration change.
4. Run the smallest PTB session that checks the change.
5. Run `project:check` when the change affects shared operation.
6. Run `project:check` when the change affects release readiness.
7. Run `project:check` when the change affects CI operation.

When you remove or rename a documentation file, update each Sphinx `toctree`
that points to it. Then run `docs:build`.

Put more Pytest arguments after `--`.
Use `nox-sessions.md` for examples.

## Fix lint or format findings

Run the PTB formatter first. Then run the checks that match the failure.
Use `nox-sessions.md` for the exact session commands.

Do not adjust code manually to imitate Black, isort, or Ruff. Let PTB run these
tools. Use PTB configuration to exclude a file or directory.

## Prepare a release

Prepare a release with `release:prepare`.

This session does these actions:

1. It updates the version.
2. It moves content from `doc/changes/unreleased.md` to a versioned changes file.
3. It updates `doc/changes/changelog.md`.
4. It runs configured release hooks.
5. It commits the changes if you do not use `--no-add`.
6. It opens a PR if you do not use `--no-pr`.

Useful flags:

- `--no-branch`: Do not create or switch to a release branch.
- `--no-add`: Do not add or commit changes.
- `--no-pr`: Do not create a pull request.

If dependencies change after release preparation, update the versioned changes
file with `release:update`.

After the release PR is merged, apply the release safety rule from `SKILL.md`.

`release:trigger` checks out the default branch. It pulls the default branch. It
creates a version tag. It pushes the tag. It can update a `v<major>` tag if
`PROJECT_CONFIG` enables this function.

## Update PTB or dependencies

When you update `exasol-toolbox` in a project:

1. Read the PTB changelog for migration notes.
2. Update the dependency with Poetry. Example:
   `poetry update exasol-toolbox`
3. Generate or check PTB-managed workflows.
4. Run necessary validation sessions.
5. Update `doc/changes/unreleased.md` when the project requires a changelog
   entry.

For dependency updates that fix vulnerabilities, use the PTB vulnerability
sessions.

## Maintain GitHub workflows

PTB ships workflow templates. Generate workflows instead of editing generated
files manually.

Use the PTB workflow sessions.

Use `.workflow-patcher.yml` for supported project-specific workflow changes. If
multiple Exasol Python projects need the same change, consider a PTB template,
configuration field, or hook.

When you change workflow templates, custom workflows, or `.workflow-patcher.yml`,
check these items after generation:

- No `needs` entry points to a removed job.
- Required root-level and job-level `permissions` stay in the generated
  workflow.
- Scalar permission forms, for example `read-all` and `write-all`, are handled
  or rejected with a clear error.
- Release guards, for example tag checks, still run before release or extension
  jobs.
- Self-release workflows use an action reference that exists before the first
  release tag is pushed.
- Project tools run in the Poetry environment when the project dependencies are
  installed there.
