from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import (
    Any,
    Iterable,
    MutableMapping,
)

from exasol.toolbox.nox.plugin import hookimpl
from nox import Session


class IntegrationTestsPlugin:
    @hookimpl
    def pre_integration_tests_hook(self, session, config, context):
        with TemporaryDirectory() as tmp_dir:
            tmp_dir = Path(tmp_dir)
            checkout_name = "ITDE"
            with session.chdir(tmp_dir):
                session.run(
                    "git",
                    "clone",
                    "https://github.com/exasol/integration-test-docker-environment.git",
                    checkout_name,
                )
            with session.chdir(tmp_dir / checkout_name):
                session.run(
                    "./start-test-env",
                    "spawn-test-environment",
                    "--environment-name",
                    "test",
                    "--database-port-forward",
                    "8888",
                    "--{{cookiecutter.package_name}}-port-forward",
                    "6666",
                    "--db-mem-size",
                    "4GB",
                )

    @hookimpl
    def post_integration_tests_hook(self, session, config, context):
        session.run("docker", "kill", "db_container_test", external=True)


@dataclass(frozen=True)
class Config:
    root: Path = Path(__file__).parent
    doc: Path = Path(__file__).parent / "doc"
    version_file: Path = Path(__file__).parent / "exasol" / "{{cookiecutter.package_name}}" / "version.py"
    path_filters: Iterable[str] = (
        "dist",
        ".eggs",
        "venv",
    )

    plugins = [IntegrationTestsPlugin]


PROJECT_CONFIG = Config()
