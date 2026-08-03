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
When you add a temporary local override, create an issue in the project to
replace it with configuration, a plugin hook, or a PTB extension point later.

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

## Use git hooks

If `.pre-commit-config.yaml` exists, the project can run hooks on commit and
push.

- On commit, pre-commit hooks can apply format fixes. Add the changed files and
  commit again.
- On push, pre-push hooks can run checks such as type checks and lint checks.
  Fix failures and push again.

## Fix lint or format findings

Run the PTB formatter first. Then run the checks that match the failure.
Use `nox-sessions.md` for the exact session commands.

Do not adjust code manually to imitate Black, isort, or Ruff. Let PTB run these
tools. To exclude a Python file or directory, use
`PROJECT_CONFIG.add_to_excluded_python_paths` in `noxconfig.py`.

## Prepare a release

Prepare a release with `release:prepare`.

This session does these actions:

1. It updates the version.
2. It creates a release branch and sets it as the current Git branch unless you
   use `--no-branch` or `--no-add`.
3. It moves content from `doc/changes/unreleased.md` to a versioned changes file.
4. It updates `doc/changes/changelog.md`.
5. It runs configured release hooks.
6. It commits the changes if you do not use `--no-add`.
7. It opens a PR if you do not use `--no-pr`.

Useful flags:

- `--no-branch`: Do not create a release branch and do not set it as current.
- `--no-add`: Do not add or commit changes. This also prevents release branch
  creation.
- `--no-pr`: Do not create a pull request.

If dependencies change after release preparation, update the versioned changes
file with `release:update`.

After the release PR is merged, apply the release safety rule from `SKILL.md`.

`release:trigger` checks out the default branch. It pulls the default branch. It
creates a version tag. It pushes the tag. It updates a `v<major>` tag if
`PROJECT_CONFIG.create_major_version_tags` is `True`.

## Update PTB or dependencies

When you update `exasol-toolbox` in a project:

1. Read the PTB changelog for migration notes.
2. Check the `exasol-toolbox` version range in `pyproject.toml`.
3. Update the dependency with Poetry. Example:
   `poetry update exasol-toolbox`
4. If Poetry does not update PTB, adjust the version range intentionally. This
   is usually necessary for a new PTB major version.
5. Generate or check PTB-managed workflows.
6. Run necessary validation sessions.
7. Update `doc/changes/unreleased.md` when the project requires a changelog
   entry.

For dependency updates that fix vulnerabilities, use the PTB vulnerability
sessions.

## Maintain GitHub workflows

PTB has two workflow groups:

- PTB-provided workflows: Do not edit generated files by hand. Use
  `.workflow-patcher.yml` for supported project-specific changes. Use
  `PROJECT_CONFIG`, a PTB template, or a hook for shared behavior. Then run
  `workflow:generate` and `workflow:check`.
- Custom workflows: The project owns these files. Edit the custom file directly.
  Prefer workflow extension files that PTB can call from a PTB-provided
  workflow. Use a separate workflow trigger only when the project owns the merge
  protection decision for that workflow. Put GitHub `permissions` in the jobs
  that need them. Declare reusable-workflow secrets under
  `on.workflow_call.secrets`.

After workflow changes, run `workflow:audit`.
