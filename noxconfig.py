"""Configuration for nox based task runner"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.nox.plugin import hookimpl
from exasol.toolbox.tools.replace_version import update_github_yml


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
    def prepare_release_update_version(self, session, config, version):
        for workflow in self.template_workflows:
            update_github_yml(workflow, version)

        for action in self.actions:
            update_github_yml(action, version)

    @hookimpl
    def prepare_release_add_files(self, session, config):
        return self.template_workflows + self.actions


# BaseConfig
#   - Includes validation of the Exasol/Python version format and max/min Python version.
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
    path_filters: Iterable[str] = (
        "metrics-schema",
        "project-template",
        "idioms",
    )
    plugins: Iterable[object] = (UpdateTemplates,)
    # need --keep-runtime-typing, as pydantic with python3.9 does not accept str | None
    # format, and it is not resolved with from __future__ import annotations. pyupgrade
    # will keep switching Optional[str] to str | None leading to issues.
    pyupgrade_args: Iterable[str] = ("--py39-plus", "--keep-runtime-typing")


PROJECT_CONFIG = Config()
