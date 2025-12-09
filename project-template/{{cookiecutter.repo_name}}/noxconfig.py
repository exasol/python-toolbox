from __future__ import annotations

from pathlib import Path

from exasol.toolbox.config import BaseConfig




PROJECT_CONFIG = BaseConfig(
    project_name="{{cookiecutter.package_name}}",
    root_path=Path(__file__).parent,
)
