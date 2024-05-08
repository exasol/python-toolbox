"""Configuration for nox based task runner"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import (
    Any,
    Iterable,
    MutableMapping,
)

from nox import Session

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
    def prepare_release_add_files(self, session, config, add):
        add(session, self.workflows)


@dataclass(frozen=True)
class Config:
    """Project specific configuration used by nox infrastructure"""

    root: Path = Path(__file__).parent
    doc: Path = Path(__file__).parent / "doc"
    version_file: Path = Path(__file__).parent / "exasol" / "toolbox" / "version.py"
    path_filters: Iterable[str] = ("dist", ".eggs", "venv", "metrics-schema")
    plugins = [UpdateTemplates]

    @staticmethod
    def pre_integration_tests_hook(
        _session: Session, _config: Config, _context: MutableMapping[str, Any]
    ) -> bool:
        """Implement if project specific behaviour is required"""
        return True

    @staticmethod
    def post_integration_tests_hook(
        _session: Session, _config: Config, _context: MutableMapping[str, Any]
    ) -> bool:
        """Implement if project specific behaviour is required"""
        return True


PROJECT_CONFIG = Config()
