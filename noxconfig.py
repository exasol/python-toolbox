"""Configuration for nox based task runner"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from exasol.toolbox.nox.plugin import hookimpl
from exasol.toolbox.tools.replace_version import update_workflow


class UpdateTemplates:
    TEMPLATE_PATH: Path = Path(__file__).parent / "exasol" / "toolbox" / "templates"

    @property
    def workflows(self):
        gh_workflows = self.TEMPLATE_PATH / "github" / "workflows"
        gh_workflows = [f for f in gh_workflows.iterdir() if f.is_file()]
        return gh_workflows

    @hookimpl
    def prepare_release_update_version(self, session, config, version):
        for workflow in self.workflows:
            update_workflow(workflow, version)

    @hookimpl
    def prepare_release_add_files(self, session, config):
        return self.workflows


@dataclass(frozen=True)
class Config:
    """Project specific configuration used by nox infrastructure"""

    root: Path = Path(__file__).parent
    doc: Path = Path(__file__).parent / "doc"
    version_file: Path = Path(__file__).parent / "exasol" / "toolbox" / "version.py"
    path_filters: Iterable[str] = ("dist", ".eggs", "venv", "metrics-schema", "cookie-cutter-template")
    plugins = [UpdateTemplates]


PROJECT_CONFIG = Config()
