import pytest
from exasol.toolbox.tools import replace_version


def test_retrieve_issue_templates():
    lines = ["first/line\n", "second/line@0.0.0\n",""]
    expected = ["first/line\n", "second/line@9.9.9\n",""]
    replace_version._replace(lines, "second/line", "9.9.9")
    actual = lines
    assert actual == expected

