from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import (
    Any,
    MutableMapping,
)

from nox import Session


@dataclass(frozen=True)
class Config:
    root: Path = Path(__file__).parent
    doc: Path = Path(__file__).parent / "doc"
    build: Path = Path(__file__).parent / "build"
    version_file: Path = Path(__file__).parent / "exasol" / "toolbox" / "version.py"

    @staticmethod
    def pre_integration_tests_hook(
        session: Session, config: Config, context: MutableMapping[str, Any]
    ) -> bool:
        """Implement if project specific behaviour is required"""
        return True

    @staticmethod
    def post_integration_tests_hook(
        session: Session, config: Config, context: MutableMapping[str, Any]
    ) -> bool:
        """Implement if project specific behaviour is required"""
        return True


PROJECT_CONFIG = Config()
