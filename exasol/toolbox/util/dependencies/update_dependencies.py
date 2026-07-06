from __future__ import annotations

import subprocess  # nosec: B404 - risk of subprocess is accepted
from pathlib import Path

from pydantic import (
    BaseModel,
    ConfigDict,
    computed_field,
)

from exasol.toolbox.util.dependencies.audit import Vulnerabilities
from exasol.toolbox.util.dependencies.shared_models import PoetryFiles
from exasol.toolbox.util.git import Git


class DependencyUpdater(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    root_path: Path

    @computed_field  # type: ignore[misc]
    @property
    def poetry_lock_path(self) -> Path:
        return self.root_path / PoetryFiles.poetry_lock

    def _get_report_json(self) -> str:
        vulnerabilities = Vulnerabilities.load_from_pip_audit(self.root_path)
        return vulnerabilities.report_json

    def _run_poetry_update(self) -> None:
        subprocess.run(  # nosec: B603 - fixed poetry command is trusted here
            ["poetry", "update"],
            cwd=self.root_path,
            check=True,
        )

    def update_vulnerable_dependencies(self) -> str | None:
        """
        Check for vulnerable dependencies, and if present, attempt to update dependencies.
        """
        initial_report = self._get_report_json()
        print(initial_report)
        if initial_report == "[]":
            return None

        self._run_poetry_update()
        post_update_report = self._get_report_json()
        print(post_update_report)

        if Git.has_uncommitted_path_changes((self.poetry_lock_path,)):
            Git.add((self.poetry_lock_path,))
            Git.commit("Updated poetry.lock")

        return post_update_report
