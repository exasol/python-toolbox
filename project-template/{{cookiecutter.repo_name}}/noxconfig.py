from __future__ import annotations

from pathlib import Path
from typing import Iterable

from exasol.toolbox.config import BaseConfig


class Config(BaseConfig):
    root: Path = Path(__file__).parent
    doc: Path = Path(__file__).parent / "doc"
    source: Path = Path("exasol/{{cookiecutter.package_name}}")
    version_file: Path = (
            Path(__file__).parent
            / "exasol"
            / "{{cookiecutter.package_name}}"
            / "version.py"
    )

PROJECT_CONFIG = Config()
