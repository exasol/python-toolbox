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


NO_MATCHING_PREFIX = Scenario("body", expected_suffix="body")

MATCHING_PREFIX_BUT_NO_LIST = Scenario(
    body="""
    Prefix first line

    Another line
    """,
    expected_suffix="",
)

MATCHING_PREFIX_AND_LIST = Scenario(
    body="""
    Prefix first line

    Another line

    * item 1
    * item 2
    """,
    expected_suffix="""
    * item 1
    * item 2
    """,
)


LIST_WITH_DASHES = Scenario(
    body="""
    Prefix first line

    Another line

    - item 1
    - item 2
    """,
    expected_suffix="""
    - item 1
    - item 2
    """,
)


SAMPLE_PREFIX = cleandoc("""
    Prefix first line

    | col 1 | col 2 |
    |-------|-------|
    | abc   | 123   |
    """)


@pytest.mark.parametrize(
    "scenario",
    [
        pytest.param(NO_MATCHING_PREFIX, id="no_matching_prefix"),
        pytest.param(MATCHING_PREFIX_BUT_NO_LIST, id="matching_prefix_but_no_list"),
        pytest.param(MATCHING_PREFIX_AND_LIST, id="matching_prefix_and_list"),
        pytest.param(LIST_WITH_DASHES, id="list_with_dashes"),
    ],
)
def test_replace_prefix(scenario):
    testee = scenario.create_testee()
    testee.replace_prefix(SAMPLE_PREFIX)
    expected = f"{SAMPLE_PREFIX}{scenario.expected_suffix}"
    assert testee.body == f"{SAMPLE_PREFIX}{scenario.expected_suffix}"
