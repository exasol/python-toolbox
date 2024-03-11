import subprocess
from inspect import cleandoc
from unittest.mock import patch

import pytest

from exasol.toolbox import git


@pytest.fixture
def git_tag():
    result = subprocess.CompletedProcess(
        args=["git", "tag", "--sort=comitterdate"],
        returncode=0,
        stdout=cleandoc(
            """
            0.1.0
            0.2.0
            0.3.0
            0.4.0
            0.5.0
            0.6.0
            0.6.1
            0.6.2
            0.7.0
            0.8.0
            """
        ),
        stderr="",
    )
    yield result


def test_git_tags(git_tag):
    expected = sorted(
        [
            "0.1.0",
            "0.2.0",
            "0.3.0",
            "0.4.0",
            "0.5.0",
            "0.6.0",
            "0.6.1",
            "0.6.2",
            "0.7.0",
            "0.8.0",
        ]
    )
    with patch("subprocess.run", return_value=git_tag):
        actual = sorted(git.tags())

    assert expected == actual
