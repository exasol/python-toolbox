from inspect import cleandoc

import pytest

from exasol.toolbox.util.release.markdown import (
    HierarchyError,
    Markdown,
    ParseError,
)


class Scenario:
    def __init__(
        self, initial: str, expected_output: str, expected_children: list[str]
    ):
        self.initial = cleandoc(initial)
        self.expected_output = cleandoc(expected_output)
        self.expected_children = expected_children

    def create_testee(self) -> Markdown:
        return Markdown.parse(self.initial)


INVALID_MARKDOWN = cleandoc("""
    # Title

    Some text.

    # Another Title
    """)

MINIMAL = Scenario(
    initial="""
    # title
    body
    """,
    expected_output="""
    # title

    body
    """,
    expected_children=[],
)

WITH_CHILD = Scenario(
    initial="""
    # Parent
    text
    ## Child
    paragraph

    * item 1
    * item 2
    """,
    expected_output="""
    # Parent

    text

    ## Child

    paragraph

    * item 1
    * item 2
    """,
    expected_children=["Child"],
)

TWO_CHILDREN = Scenario(
    initial="""
    # Parent
    text
    ## C1
    aaa
    ## C2
    bbb
    """,
    expected_output="""
    # Parent

    text

    ## C1

    aaa

    ## C2

    bbb
    """,
    expected_children=["C1", "C2"],
)


NESTED = Scenario(
    initial="""
    # Parent
    text
    ## Child A
    aaa
    ### Grand Child
    ccc
    ## Child B
    bbb
    """,
    expected_output="""
    # Parent

    text

    ## Child A

    aaa

    ### Grand Child

    ccc

    ## Child B

    bbb
    """,
    expected_children=["Child A", "Child B"],
)


SPECIAL_CHAR_TITLE = "+ special [char] * title"
SPECIAL_CHAR_CHILD = Scenario(
    initial=f"""
    # title

    ## {SPECIAL_CHAR_TITLE}
    body
    """,
    expected_output=f"""
    # title

    ## {SPECIAL_CHAR_TITLE}

    body
    """,
    expected_children=[SPECIAL_CHAR_TITLE],
)


def test_no_title_error():
    with pytest.raises(ParseError, match="First line of markdown file must be a title"):
        Markdown.parse("body\n# title")


def test_additional_line_error():
    expected_error = (
        'additional line "# Another Title" after top-level section "# Title".'
    )
    with pytest.raises(ParseError, match=expected_error):
        Markdown.parse(INVALID_MARKDOWN)


ALL_SCENARIOS = [MINIMAL, WITH_CHILD, TWO_CHILDREN, NESTED, SPECIAL_CHAR_CHILD]


@pytest.mark.parametrize("scenario", ALL_SCENARIOS)
def test_number_of_children(scenario: Scenario):
    assert len(scenario.create_testee().children) == len(scenario.expected_children)


@pytest.mark.parametrize("scenario", ALL_SCENARIOS)
def test_non_existing_child(scenario: Scenario):
    assert scenario.create_testee().child("non existing") is None


@pytest.mark.parametrize("scenario", ALL_SCENARIOS)
def test_valid_child(scenario: Scenario):
    assert all(scenario.create_testee().child(c) for c in scenario.expected_children)


@pytest.mark.parametrize("scenario", ALL_SCENARIOS)
def test_rendered(scenario: Scenario):
    assert scenario.create_testee().rendered == scenario.expected_output


@pytest.fixture
def sample_child() -> Markdown:
    return Markdown(title="## New", intro="intro", items="", children=[])


@pytest.mark.parametrize(
    "scenario, pos",
    [
        (MINIMAL, 0),
        (WITH_CHILD, 1),
        (TWO_CHILDREN, 1),
    ],
)
def test_add_child(sample_child: Markdown, scenario: Scenario, pos: int):
    testee = scenario.create_testee()
    testee.add_child(sample_child)
    assert testee.children[pos] == sample_child


@pytest.fixture
def illegal_child() -> Markdown:
    return Markdown(title="# Top-level", intro="intro", items="", children=[])


@pytest.mark.parametrize("scenario", ALL_SCENARIOS)
def test_illegal_child(illegal_child: Markdown, scenario: Scenario):
    testee = scenario.create_testee()
    with pytest.raises(HierarchyError):
        testee.add_child(illegal_child)


def test_nested():
    testee = NESTED.create_testee()
    assert testee.child("Child A").child("Grand Child") is not None
