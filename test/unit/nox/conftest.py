from typing import Any
from unittest import mock

import pytest
from nox import (
    Session,
    _options,
    manifest,
    virtualenv,
)
from nox.sessions import (
    SessionRunner,
)


class FakeEnv(mock.MagicMock):
    # Extracted from nox testing
    _get_env = virtualenv.VirtualEnv._get_env


def make_fake_env(venv_backend: str = "venv", **kwargs: Any) -> FakeEnv:
    # Extracted from nox testing
    return FakeEnv(
        spec=virtualenv.VirtualEnv,
        env={},
        venv_backend=venv_backend,
        **kwargs,
    )


@pytest.fixture
def nox_session_runner_posargs() -> list[str]:
    return []


@pytest.fixture
def nox_session_runner(tmp_path, nox_session_runner_posargs):
    return SessionRunner(
        name="test",
        signatures=["test"],
        func=mock.Mock(spec=["python"], python="3.10"),
        global_config=_options.options.namespace(
            posargs=nox_session_runner_posargs,
            error_on_external_run=False,
            install_only=False,
            invoked_from=tmp_path,
        ),
        manifest=mock.create_autospec(manifest.Manifest),
    )


@pytest.fixture
def nox_session(nox_session_runner):
    # Extracted from nox testing
    nox_session_runner.venv = make_fake_env(bin_paths=["/no/bin/for/you"])
    yield Session(nox_session_runner)
