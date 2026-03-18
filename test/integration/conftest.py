import subprocess
from pathlib import Path

import pytest

from exasol.toolbox.config import BaseConfig


@pytest.fixture(scope="session")
def poetry_path() -> str:
    result = subprocess.run(["which", "poetry"], capture_output=True, text=True)
    poetry_path = result.stdout.strip()
    return poetry_path


@pytest.fixture(scope="session")
def ptb_minimum_python_version() -> str:
    """
    Some integration tests create a sample poetry project and need to
    specify its minimum python version in property "requires-python" in file
    pyproject.toml.

    This fixture returns a value including all python versions supported by
    the PTB.
    """
    return BaseConfig(root_path=Path(), project_name="toolbox").minimum_python_version
