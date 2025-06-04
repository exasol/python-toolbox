"""Configuration for nox based task runner"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

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


@dataclass(frozen=True)
class Config:
    """Project specific configuration used by nox infrastructure"""

    root: Path = Path(__file__).parent
    doc: Path = Path(__file__).parent / "doc"
    source: Path = Path(__file__).parent / "exasol" / "toolbox"
    importlinter: Path = Path(__file__).parent / ".import_linter_config"
    version_file: Path = Path(__file__).parent / "exasol" / "toolbox" / "version.py"
    path_filters: Iterable[str] = (
        "metrics-schema",
        "project-template",
        "idioms",
    )
    python_versions = ["3.9", "3.10", "3.11", "3.12", "3.13"]
    exasol_versions = ["7.1.9"]
    plugins = [UpdateTemplates]
    # need --keep-runtime-typing, as pydantic with python3.9 does not accept str | None
    # format, and it is not resolved with from __future__ import annotations. pyupgrade
    # will keep switching Optional[str] to str | None leading to issues.
    pyupgrade_args = ("--py39-plus", "--keep-runtime-typing")


PROJECT_CONFIG = Config()
