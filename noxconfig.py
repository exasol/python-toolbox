"""Configuration for nox based task runner"""

from __future__ import annotations

from pathlib import Path

from pydantic import computed_field

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


ROOT_PATH = Path(__file__).parent


class Config(BaseConfig):
    @computed_field  # type: ignore[misc]
    @property
    def importlinter(self) -> Path:
        """
        Path for the import lint configuration file.
        This is an experimental feature that requires further scrutiny. This will
        be done in:
            https://github.com/exasol/python-toolbox/issues/628
        """
        return self.root_path / ".import_linter_config"


PROJECT_CONFIG = Config(
    root_path=ROOT_PATH,
    project_name="toolbox",
    add_to_excluded_python_paths=(
        # The cookiecutter placeholders do not work well with checks.
        # Instead, the format & linting are checked in the
        # ``test.integration.project-template``.
        "project-template",
        # This file comes from poetry (https://install.python-poetry.org/),
        # so we should not modify it.
        "get_poetry.py",
    ),
    create_major_version_tags=True,
    # The PTB does not have integration tests run with an Exasol DB,
    # so for running in the CI, we take the first element.
    exasol_versions=("7.1.30",),
    plugins_for_nox_sessions=(UpdateTemplates,),
)
