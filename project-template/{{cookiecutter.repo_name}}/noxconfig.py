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
    path_filters: Iterable[str] = ()
    pyupgrade_args: Iterable[str] = (
    "--py{{cookiecutter.python_version_min | replace('.', '')}}-plus",)
    plugins: Iterable[object] = ()
    create_major_version_tags = False


PROJECT_CONFIG = Config()
