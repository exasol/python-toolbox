from subprocess import CalledProcessError
from unittest.mock import patch

import pytest

from exasol.toolbox.error import ToolboxError
from exasol.toolbox.release import poetry


@patch("exasol.toolbox.release.which", return_value=None)
def test_poetry_decorator_no_poetry_executable(mock):
    @poetry("test")
    def test(result):
        pass

    with pytest.raises(ToolboxError):
        test()


@patch("exasol.toolbox.release.which", return_value="")
@patch(
    "exasol.toolbox.release.subprocess.run",
    side_effect=CalledProcessError(returncode=1, cmd=["test"]),
)
def test_poetry_decorator_subprocess(mockSR, mockW):
    @poetry("test")
    def test(result):
        pass

    with pytest.raises(ToolboxError):
        test()
