from __future__ import annotations

from pathlib import Path
from typing import Iterable

from exasol.toolbox.config import BaseConfig


class Config(BaseConfig):
    plugins: Iterable[object] = ()

PROJECT_CONFIG = Config(
    project_name="{{cookiecutter.package_name}}",
    root_path=Path(__file__).parent,
)
