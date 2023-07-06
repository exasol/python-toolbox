from __future__ import annotations

from dataclasses import dataclass
from inspect import cleandoc
from pathlib import Path
from typing import (
    Any,
    Iterable,
    MutableMapping,
)

from nox import Session


@dataclass(frozen=True)
class Config:
    root: Path = Path(__file__).parent
    doc: Path = Path(__file__).parent / "doc"
    version_file: Path = Path(__file__).parent / "exasol" / "toolbox" / "version.py"
    path_filters: Iterable[str] = ("dist", ".eggs", "venv")

    audit_licenses = ["Apache Software License"]
    audit_exceptions = {
        "pylint": cleandoc(
            """
            The project only makes use of pylint command line.
            
            It only was added as normal dependency to save the "clients" the step
            of manually adding it as dependency.
            
            Note(s): 
            
                Pylint could be marked, added as optional (extra) dependency to make it obvious
                that it is an opt in, controlled by the "user/client". 
            
                Replacing pylint with an alternative (like `ruff <https://github.com/astral-sh/ruff>`_)
                with a more would remove the ambiguity and need for justification.
        """
        )
    }

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
