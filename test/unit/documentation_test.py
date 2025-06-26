import shutil
from unittest.mock import (
    MagicMock,
    patch,
)

import pytest

import exasol.toolbox.nox._documentation
from exasol.toolbox.nox._documentation import (
    _docs_links_check,
    _docs_list_links,
)
from noxconfig import Config


@pytest.fixture()
def file1():
    return """
https://examle.invalid
:ref:`Test`"""


@pytest.fixture()
def index():
    return """.. _Test:
    
Test
____

.. toctree::
   :maxdepth: 1
   :hidden:

   file"""


@pytest.fixture()
def expected1():
    return """filename: file.rst:2 -> uri: https://examle.invalid"""


def config(index, file, tmp_path):
    test_doc = tmp_path / "doc"
    test_doc.mkdir()
    (test_doc / "_static").mkdir()
    shutil.copyfile(Config.doc / "conf.py", test_doc / "conf.py")
    rst_index = test_doc / "index.rst"
    rst_file1 = test_doc / "file.rst"
    rst_index.touch()
    rst_file1.touch()
    rst_index.write_text(index)
    rst_file1.write_text(file)


def test_docs_links(index, file1, expected1, tmp_path):
    config(index, file1, tmp_path)
    r_code, text = _docs_list_links(tmp_path / "doc")
    assert (text == expected1) and not r_code


@pytest.mark.parametrize(
    "file2, expected2",
    [
        ("https://github.com/exasol/python-toolbox", (0, "")),
        (
            "http://nox.thea.codes/en/stable/",
            (
                0,
                "file.rst:1: [redirected with Found] http://nox.thea.codes/en/stable/ to https://nox.thea.codes/en/stable/\n",
            ),
        ),
        (
            "https://github.com/exasol/python-toolbox/pull",
            (
                0,
                "file.rst:1: [redirected permanently] https://github.com/exasol/python-toolbox/pull to https://github.com/exasol/python-toolbox/pulls\n",
            ),
        ),
        (
            "https://github.com/exasol/python-toolbox/asdf",
            (
                1,
                "file.rst:1: [broken] https://github.com/exasol/python-toolbox/asdf: 404 Client Error: Not Found for url: https://github.com/exasol/python-toolbox/asdf\n",
            ),
        ),
    ],
)
def test_docs_links_check(index, file2, expected2, tmp_path):
    config(index, file2, tmp_path)
    args = MagicMock
    args.output = None
    actual = _docs_links_check(tmp_path / "doc", args)
    assert actual == expected2
