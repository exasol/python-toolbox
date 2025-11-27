"""Configuration for nox based task runner"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.nox.plugin import hookimpl
from exasol.toolbox.tools.replace_version import update_github_yml
from exasol.toolbox.util.version import Version


class UpdateTemplates:
    TEMPLATE_PATH: Path = Path(__file__).parent / "exasol" / "toolbox" / "templates"
    PARENT_PATH: Path = Path(__file__).parent

    @property
    def template_workflows(self) -> list[Path]:
        gh_workflows = self.TEMPLATE_PATH / "github" / "workflows"
        return [f for f in gh_workflows.iterdir() if f.is_file()]

    @property
    def actions(self) -> list[Path]:
        gh_actions = self.PARENT_PATH / ".github" / "actions"
        return [f for f in gh_actions.rglob("*") if f.is_file()]

    @hookimpl
    def prepare_release_update_version(self, session, config, version: Version) -> None:
        for workflow in self.template_workflows:
            update_github_yml(workflow, version)

        for action in self.actions:
            update_github_yml(action, version)

    @hookimpl
    def prepare_release_add_files(self, session, config):
        return self.template_workflows + self.actions


# BaseConfig
#   - Use
#       Project_Config = BaseConfig()
#   - modify
#       Project_Config = BaseConfig(python_versions=["3.12"])
#   - expand (Do not overwrite the attributes of BaseConfig)
#       class ProjectConfig(BaseConfig):
#           extra_data: list[str] = ["data"]


class Config(BaseConfig):
    """Project specific configuration used by nox infrastructure"""

    root: Path = Path(__file__).parent
    doc: Path = Path(__file__).parent / "doc"
    source: Path = Path("exasol/toolbox")
    importlinter: Path = Path(__file__).parent / ".import_linter_config"
    version_file: Path = Path(__file__).parent / "exasol" / "toolbox" / "version.py"
    plugins: Iterable[object] = (UpdateTemplates,)


PROJECT_CONFIG = Config(
    addition_to_excluded_paths=(
        # The cookiecutter placeholders do not work well with checks.
        # Instead, the format & linting are checked in the
        # ``test.integration.project-template``.
        "project-template",
    ),
    create_major_version_tags=True,
    # The PTB does not have integration tests run with an Exasol DB,
    # so for running in the CI, we take the first element.
    exasol_versions=(BaseConfig().exasol_versions[0],),
)
