import subprocess

import pytest


@pytest.fixture(scope="session")
def poetry_path() -> str:
    result = subprocess.run(["which", "poetry"], capture_output=True, text=True)
    poetry_path = result.stdout.strip()
    return poetry_path
