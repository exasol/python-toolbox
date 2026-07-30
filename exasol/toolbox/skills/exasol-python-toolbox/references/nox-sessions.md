# PTB Nox Sessions

Always list the sessions in the current project:

```bash
poetry run -- nox -l
```

The sessions below match the PTB version that includes this skill.

## Project and quality sessions

| Session | Use | Notes |
| --- | --- | --- |
| `project:check` | Run large local checks or CI checks. | It runs format check, Pylint, Mypy, and coverage for unit and integration tests. |
| `format:fix` | Apply Python format changes. | It runs pyupgrade, Ruff fixes, isort, and Black. |
| `format:check` | Check Python format. | It runs Ruff check, isort check, and Black check. |
| `lint:code` | Run static code analysis. | It runs Pylint on `PROJECT_CONFIG.source_code_path` and writes `.lint.json`. |
| `lint:typing` | Run type checks. | It runs Mypy on filtered project Python files. |
| `lint:security` | Run security lint. | It runs Bandit and writes `.security.json`. |
| `lint:dependencies` | Check legacy dependency sources. | This session is deprecated. It is scheduled for removal on 2026-10-08. Do not add new use. |

## Test sessions

| Session | Use | Notes |
| --- | --- | --- |
| `test:unit` | Run unit tests. | It runs `pytest -v test/unit`. Put Pytest arguments after `--`. |
| `test:integration` | Run integration tests. | It runs `pytest -v test/integration`. It supports PTB integration test hooks. |
| `test:coverage` | Run all tests with coverage. | It runs unit and integration tests with coverage. It prints `coverage report -m`. |

Test command examples:

```bash
poetry run -- nox -s test:unit
poetry run -- nox -s test:unit -- --coverage
poetry run -- nox -s test:unit -- test/unit/path_test.py -k scenario
poetry run -- nox -s test:integration -- --db-version 8.34.0
```

## Documentation and changelog sessions

| Session | Use | Notes |
| --- | --- | --- |
| `docs:build` | Build current documentation. | It runs Sphinx HTML build. It makes warnings errors. |
| `docs:multiversion` | Build multiversion documentation. | It runs `sphinx-multiversion` and creates `.nojekyll`. |
| `docs:open` | Open built documentation in a browser. | It requires `.html-documentation`. It can require GUI approval. |
| `docs:clean` | Remove generated documentation. | It deletes `.html-documentation`. |
| `links:list` | List documentation links. | It uses Sphinx linkcheck. It ignores link failures. |
| `links:check` | Validate documentation links. | It can write JSON output with `-- -o <directory>`. |
| `changelog:updated` | Check that the changelog changed. | It fails if `doc/changes` did not change when compared with `origin/main`. |

## Release sessions

| Session | Use | Notes |
| --- | --- | --- |
| `release:prepare` | Prepare a release PR. | It requires `-- --type major`, `minor`, or `patch`. It creates a branch, commit, and PR if flags do not disable these actions. |
| `release:update` | Update a prepared release changelog. | It updates the latest versioned changelog after dependency changes. |
| `release:trigger` | Trigger a release from the default branch. | It creates and pushes git tags. |

Release command examples:

```bash
poetry run -- nox -s release:prepare -- --type patch
poetry run -- nox -s release:prepare -- --type minor --no-pr --no-branch --no-add
poetry run -- nox -s release:update
```

## Workflow sessions

| Session | Use | Notes |
| --- | --- | --- |
| `workflow:check` | Check generated workflows. | It requires one workflow name or `all`. It fails when files differ from PTB templates. |
| `workflow:generate` | Generate or update workflows. | It requires one workflow name or `all`. |
| `workflow:audit` | Audit workflows and actions. | It runs zizmor with PTB configuration. It sends more zizmor arguments to zizmor. |

Workflow command examples:

```bash
poetry run -- nox -s workflow:check -- all
poetry run -- nox -s workflow:generate -- checks
poetry run -- nox -s workflow:audit -- --fix=safe
```

## Dependency, artifact, package, and matrix sessions

| Session | Use | Notes |
| --- | --- | --- |
| `dependency:licenses` | Report dependency licenses. | It prints a Markdown license report. |
| `dependency:audit` | Report vulnerabilities. | It prints known vulnerabilities as JSON. |
| `vulnerabilities:update` | Update vulnerable dependencies. | It can write a JSON report file inside the repository. |
| `vulnerabilities:resolved` | Report vulnerabilities that are resolved since the latest tag. | Use it during release preparation. |
| `dependency:sbom` | Generate SBOM files. | It writes `bom.cdx.json` and `bom.spdx.json`. |
| `artifacts:validate` | Validate CI artifacts. | It checks `.coverage`, `.lint.json`, and `.security.json`. |
| `artifacts:copy` | Copy and combine CI artifacts. | It requires an artifact directory argument. |
| `sonar:check` | Upload artifacts to Sonar. | It uses `SONAR_TOKEN` and prepares `ci-coverage.xml`. |
| `package:check` | Validate the package long description. | It runs `poetry build` and `twine check`. |
| `matrix:generate` | Print selected config values as JSON arrays. | Use this session for matrix output. |
| `matrix:python` | Print legacy Python matrix output. | This session is deprecated. It is scheduled for removal on 2026-09-15. |
| `matrix:exasol` | Print legacy Exasol matrix output. | This session is deprecated. It is scheduled for removal on 2026-09-15. |
| `matrix:all` | Print legacy Python and Exasol matrix output. | This session is deprecated. It is scheduled for removal on 2026-09-15. |
