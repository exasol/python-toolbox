from inspect import cleandoc

import pytest

from exasol.toolbox.util.release.markdown import (
    IllegalChild,
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
    expected_children=["## Child"],
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
    expected_children=["## C1", "## C2"],
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
    expected_children=["## Child A", "## Child B"],
)


@pytest.fixture
def sample_child() -> Markdown:
    return Markdown(title="## New", intro="intro")


@pytest.fixture
def illegal_child() -> Markdown:
    return Markdown(title="# Top-level", intro="intro")


def test_no_title_error():
    with pytest.raises(ParseError, match="First line of markdown file must be a title"):
        Markdown.parse("body\n# title")


def test_additional_line_error():
    expected_error = (
        'additional line "# Another Title" after top-level section "# Title".'
    )
    with pytest.raises(ParseError, match=expected_error):
        Markdown.parse(INVALID_MARKDOWN)


def test_constructor_illegal_child(illegal_child: Markdown):
    with pytest.raises(IllegalChild):
        Markdown("# title", children=[illegal_child])


ALL_SCENARIOS = [MINIMAL, WITH_CHILD, TWO_CHILDREN, NESTED]


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


def test_replace_illegal_child(illegal_child):
    testee = WITH_CHILD.create_testee()
    with pytest.raises(IllegalChild):
        testee.replace_child(illegal_child)


@pytest.mark.parametrize("scenario", ALL_SCENARIOS)
def test_replace_existing_child(scenario: Scenario):
    testee = WITH_CHILD.create_testee()
    old_child = testee.children[0]
    old_rendered = testee.rendered
    new_child = Markdown(old_child.title, "new intro")
    expected = old_rendered.replace(old_child.rendered, new_child.rendered)
    testee.replace_child(new_child)
    assert testee.rendered == expected


@pytest.mark.parametrize("scenario", ALL_SCENARIOS)
def test_replace_non_existing_child(scenario: Scenario, sample_child: Markdown):
    testee = scenario.create_testee()
    expected = len(testee.children) + 1
    testee.replace_child(sample_child)
    assert len(testee.children) == expected
    assert testee.children[-1] == sample_child


@pytest.mark.parametrize("scenario", ALL_SCENARIOS)
def test_add_illegal_child(illegal_child: Markdown, scenario: Scenario):
    testee = scenario.create_testee()
    with pytest.raises(IllegalChild):
        testee.add_child(illegal_child)


def test_nested():
    testee = NESTED.create_testee()
    assert testee.child("## Child A").child("### Grand Child") is not None
