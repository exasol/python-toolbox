import os
from pathlib import Path

import pytest

from exasol.toolbox.nox._shared import _deny_filter


@pytest.fixture
def directory_tree(tmp_path):
    directories = {
        "d1": ["d1-f1.txt", "d1-f2.py"],
        "d2": ["d2-f1.txt", "d2-f2.py"],
        ".d3": [".d3-f1.txt", ".d3-f2.py"],
    }
    file_list = []
    for directory, files in directories.items():
        directory_path = tmp_path / directory
        directory_path.mkdir()
        for file_name in files:
            file_path = directory_path / file_name
            file_path.touch()
            file_list.append(file_path)

    yield tmp_path, file_list


@pytest.mark.parametrize(
    "deny_list,expected",
    [
        (["d1"], {"d2-f1.txt", "d2-f2.py", ".d3-f1.txt", ".d3-f2.py"}),
        (["d2"], {"d1-f1.txt", "d1-f2.py", ".d3-f1.txt", ".d3-f2.py"}),
        ([".d3"], {"d1-f1.txt", "d1-f2.py", "d2-f1.txt", "d2-f2.py"}),
        (["d1", "d2"], {".d3-f1.txt", ".d3-f2.py"}),  # Added missing test case
        (["d2", ".d3"], {"d1-f1.txt", "d1-f2.py"}),
        (["d1", ".d3"], {"d2-f1.txt", "d2-f2.py"}),
        (["d1", "d2", ".d3"], set()),
    ],
)
def test_deny_filter(directory_tree, deny_list, expected):
    root, files = directory_tree
    actual = {f.name for f in _deny_filter(files, deny_list)}
    assert actual == expected
