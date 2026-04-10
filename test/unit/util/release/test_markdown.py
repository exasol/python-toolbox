from inspect import cleandoc

import pytest

from exasol.toolbox.util.release.markdown import (
    IllegalChild,
    Markdown,
    ParseError,
)


def _markdown(text: str) -> Markdown:
    return Markdown.from_text(cleandoc(text))


class Scenario:
    def __init__(
        self, initial: str, expected_output: str, expected_children: list[str]
    ):
        self.initial = cleandoc(initial)
        self.expected_output = cleandoc(expected_output)
        self.expected_children = expected_children

    def create_testee(self) -> Markdown:
        return Markdown.from_text(self.initial)


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

FULL = Scenario(
    initial="""
    # title
    intro
    * item one
    * item two
    ## Child
    cintro
    - item c1
    - item c2
    """,
    expected_output="""
    # title

    intro

    * item one
    * item two

    ## Child

    cintro

    - item c1
    - item c2
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

CHILD = _markdown("""
    ## Sample Child
    child intro.
    """)

ILLEGAL_CHILD = _markdown("""
   # Top-level
   intro
   """)


def test_no_title_error():
    with pytest.raises(ParseError, match="First line of markdown file must be a title"):
        Markdown.from_text("body\n# title")


def test_additional_line_error():
    invalid_markdown = cleandoc("""
    # Title
    Some text.
    # Another Title
    """)
    
    expected_error = (
        'additional line "# Another Title" after top-level section "# Title".'
    )
    with pytest.raises(ParseError, match=expected_error):
        Markdown.from_text(invalid_markdown)


def test_constructor_illegal_child():
    with pytest.raises(IllegalChild):
        Markdown("# title", children=[ILLEGAL_CHILD])


@pytest.mark.parametrize("content, expected", [
    pytest.param(
        """
        # title
        """,
        Markdown("# title"),
        id="only_title",
    ),
    pytest.param(
        """
        # title
        intro
        """,
        Markdown("# title", "intro"),
        id="intro",
    ),
    pytest.param(
        """
        # title
        * item 1
        """,
        Markdown("# title", "", "* item 1"),
        id="items",
    ),
    pytest.param(
        """
        # title
        intro
        * item 1
        * item 2
        """,
        Markdown("# title", "intro", "* item 1\n* item 2"),
        id="intro_and_items",
    ),
    pytest.param(
        """
        # title
        intro
        - item 1
        - item 2
        """,
        Markdown("# title", "intro", "- item 1\n- item 2"),
        id="intro_dash_items",
    ),
])
def test_equals(content: str, expected: Markdown) -> None:
    assert Markdown.from_text(cleandoc(content)) == expected


@pytest.mark.parametrize(
    "attr, value",
    [
        ("title", "# other"),
        ("intro", "other"),
        ("items", "- aaa"),
        ("children", []),
    ],
)
def test_different(attr, value) -> None:
    testee = FULL.create_testee()
    other = FULL.create_testee()
    setattr(other, attr, value)
    assert testee != other


def test_test_read(tmp_path) -> None:
    file = tmp_path / "sample.md"
    file.write_text(MINIMAL.initial)
    assert Markdown.read(file) == MINIMAL.create_testee()


ALL_SCENARIOS = [MINIMAL, FULL, TWO_CHILDREN, NESTED]


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
        (FULL, 1),
        (TWO_CHILDREN, 1),
    ],
)
def test_add_child(scenario: Scenario, pos: int):
    testee = scenario.create_testee()
    testee.add_child(CHILD)
    assert testee.children[pos] == CHILD


def test_replace_illegal_child():
    testee = FULL.create_testee()
    with pytest.raises(IllegalChild):
        testee.replace_or_append_child(ILLEGAL_CHILD)


@pytest.mark.parametrize("scenario", ALL_SCENARIOS)
def test_replace_existing_child(scenario: Scenario):
    testee = FULL.create_testee()
    old_child = testee.children[0]
    old_rendered = testee.rendered
    new_child = Markdown(old_child.title, "new intro")
    expected = old_rendered.replace(old_child.rendered, new_child.rendered)
    testee.replace_or_append_child(new_child)
    assert testee.rendered == expected


@pytest.mark.parametrize("scenario", ALL_SCENARIOS)
def test_replace_non_existing_child(scenario: Scenario):
    testee = scenario.create_testee()
    expected = len(testee.children) + 1
    testee.replace_or_append_child(CHILD)
    assert len(testee.children) == expected
    assert testee.children[-1] == CHILD


@pytest.mark.parametrize("scenario", ALL_SCENARIOS)
def test_add_illegal_child(scenario: Scenario):
    testee = scenario.create_testee()
    with pytest.raises(IllegalChild):
        testee.add_child(ILLEGAL_CHILD)


def test_nested():
    testee = NESTED.create_testee()
    assert testee.child("## Child A").child("### Grand Child") is not None
