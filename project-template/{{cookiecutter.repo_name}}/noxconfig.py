from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Config:
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
    pyupgrade_args: Iterable[str] = ("--py{{cookiecutter.python_version_min | replace('.', '')}}-plus",)
    plugins: Iterable[object] = ()


PROJECT_CONFIG = Config()
