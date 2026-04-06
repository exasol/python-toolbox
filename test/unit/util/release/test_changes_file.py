from inspect import cleandoc

import pytest

from exasol.toolbox.util.release.changes_file import (
    ChangesFile,
    ParseError,
    Section,
)

import pytest


class Scenario:
    def __init__(self, initial: str, expected_output: str, expected_sections: list[str]):
        self.testee = ChangesFile.parse(cleandoc(initial))
        self.expected_output = cleandoc(expected_output)
        self.expected_sections = expected_sections


EMPTY = Scenario(
    initial="",
    expected_output="",
    expected_sections=[],
)

MINIMAL = Scenario(
    initial="""
    # title
    body
    """,
    expected_output="""
    # title

    body
    """,
    expected_sections=["title"],
)

SPECIAL_CHAR_TITLE = "+ special [char] * title"

SPECIAL_CHAR_SECTION = Scenario(
    initial=f"""
    # {SPECIAL_CHAR_TITLE}
    body
    """,
    expected_output="""
    # {SPECIAL_CHAR_TITLE}

    body
    """,
    expected_sections=[SPECIAL_CHAR_TITLE],
)

WITH_SUBSECTION = Scenario(
        initial="""
        # title
        body
        ## subtitle
        paragraph

        * item 1
        * item 2
        """,
        expected_output="""
        # title

        body

        ## subtitle

        paragraph

        * item 1
        * item 2
        """,
        expected_sections=["title","subtitle"]
    )


def test_parse_error() -> None:
    with pytest.raises(ParseError, match="Found body line without preceding title"):
        ChangesFile.parse("body line")


@pytest.mark.parametrize("scenario", [EMPTY, MINIMAL, WITH_SUBSECTION])
def test_number_of_sections(scenario: Scenario):
    assert len(scenario.testee.sections) == len(scenario.expected_sections)


@pytest.mark.parametrize("scenario", [EMPTY, MINIMAL, SPECIAL_CHAR_SECTION, WITH_SUBSECTION])
def test_get(scenario: Scenario):
    assert all(scenario.testee.get(s) for s in scenario.expected_sections)


@pytest.mark.parametrize("scenario", [EMPTY, MINIMAL, WITH_SUBSECTION])
def test_missing_section(scenario: Scenario):
    assert scenario.testee.get("non existing") is None


@pytest.mark.parametrize("scenario", [EMPTY, MINIMAL, WITH_SUBSECTION])
def test_render(scenario: Scenario):
    assert scenario.testee.rendered == scenario.expected_output


@pytest.fixture
def sample_section():
    return Section("# blabla", "body")


@pytest.mark.parametrize("scenario", [MINIMAL, WITH_SUBSECTION])
def test_add_non_empty(scenario: Scenario, sample_section):
    scenario.testee.add(sample_section)
    assert scenario.testee.sections[1] == sample_section


@pytest.mark.parametrize("scenario", [EMPTY])
def test_add_empty(scenario: Scenario, sample_section):
    scenario.testee.add(sample_section)
    assert scenario.testee.sections[0] == sample_section

