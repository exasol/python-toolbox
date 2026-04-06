from inspect import cleandoc

import pytest

from exasol.toolbox.util.release.changes_file import Section


class Scenario:
    def __init__(self, body: str, expected_suffix: str):
        self.body = cleandoc(body)
        self.expected_suffix = (
            f"\n\n{cleandoc(expected_suffix)}" if expected_suffix else ""
        )

    def create_testee(self) -> Section:
        return Section("# title", self.body)


WITHOUT_MATCHING_PREFIX = pytest.param(
    Scenario("body", expected_suffix="body"),
    id="without_matching_prefix",
)

MATCHING_PREFIX_BUT_WITHOUT_LIST = pytest.param(
    Scenario(
        body="""
        Prefix first line

        Another line
        """,
        expected_suffix="",
    ),
    id="matching_prefix_but_without_list",
)

MATCHING_PREFIX_AND_LIST = pytest.param(
    Scenario(
        """
        Prefix first line

        Another line

        * item 1
        * item 2
        """,
        expected_suffix="""
        * item 1
        * item 2
        """,
    ),
    id="matching_prefix_and_list",
)


SAMPLE_PREFIX = cleandoc(
    """
    Prefix first line

    | col 1 | col 2 |
    |-------|-------|
    | abc   | 123   |
    """
)


@pytest.mark.parametrize(
    "scenario",
    [
        WITHOUT_MATCHING_PREFIX,
        MATCHING_PREFIX_BUT_WITHOUT_LIST,
        MATCHING_PREFIX_AND_LIST,
    ],
)
def test_replace_prefix(scenario):
    testee = scenario.create_testee()
    testee.replace_prefix(SAMPLE_PREFIX)
    assert testee.body == f"{SAMPLE_PREFIX}{scenario.expected_suffix}"
