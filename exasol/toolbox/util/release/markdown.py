"""
Class Markdown represents a file in Markdown syntax with some additional
constraints:

* The file must start with a title in the first line.
* Each subsequent title must be of a higher level, i.e. start with more "#"
  characters than the top-level title.

Each title starts a section, optionally containing an additional intro and a
bullet list of items.

Each section can also contain subsections as children, hence sections can be
nested up to the top-level section representing the whole file.
"""

from __future__ import annotations

import io
import re
from pathlib import Path


class ParseError(Exception):
    """
    Indicates inconsistencies when parsing a changelog from raw
    text. E.g. a section with a body but no title.
    """


class IllegalChild(Exception):
    """
    When adding a child to a parent with higher level title.
    """


def is_title(line: str) -> bool:
    return (line != "") and line.startswith("#")


def is_list_item(line: str) -> bool:
    return bool(re.match(r"^([*-]|[0-9]+\.)", line))


def is_intro(line: str) -> bool:
    return (line != "") and not is_title(line) and not is_list_item(line)


def level(title: str) -> int:
    """
    Return the hierarchical level of the title, i.e. the number of "#"
    chars at the beginning of the title.
    """
    return len(title) - len(title.lstrip("#"))


class Markdown:
    """
    Represents a Markdown file or a section within a Markdown file.
    """

    def __init__(
        self,
        title: str,
        intro: str = "",
        items: str = "",
        children: list[Markdown] | None = None,
    ):
        self.title = title.rstrip("\n")
        self.intro = intro
        self.items = items
        children = children or []
        for child in children:
            self._check(child)
        self.children = children

    def can_contain(self, child: Markdown) -> bool:
        return level(self.title) < level(child.title)

    def find(self, child_title: str) -> tuple[int, Markdown] | None:
        """
        Return index and child having the specified title, or None if
        there is none.
        """
        for i, child in enumerate(self.children):
            if child.title == child_title:
                return i, child
        return None

    def child(self, title: str) -> Markdown | None:
        """
        Retrieve the child with the specified title.
        """
        return found[1] if (found := self.find(title)) else None

    def _check(self, child: Markdown) -> Markdown:
        if not self.can_contain(child):
            raise IllegalChild(
                f'Markdown section "{self.title}" cannot have "{child.title}" as child.'
            )
        return child

    def add_child(self, child: Markdown, pos: int = 1) -> Markdown:
        """
        Insert the specified section as child at the specified position.
        """

        self.children.insert(pos, self._check(child))
        return self

    def replace_or_append_child(self, child: Markdown) -> Markdown:
        """
        If there is a child with the same title, then replace this child;
        otherwise, append the specified child.
        """

        self._check(child)
        if found := self.find(child.title):
            self.children[found[0]] = child
        else:
            self.children.append(child)
        return self

    @property
    def rendered(self) -> str:
        def elements():
            yield from (self.title, self.intro, self.items)
            yield from (c.rendered for c in self.children)

        return "\n\n".join(e for e in elements() if e)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Markdown)
            and other.title == self.title
            and other.intro == self.intro
            and other.items == self.items
            and other.children == self.children
        )

    def __str__(self) -> str:
        return self.rendered

    @classmethod
    def read(cls, file: Path) -> Markdown:
        """
        Parse Markdown instance from the provided file.
        """

        with file.open("r") as stream:
            return cls.parse(stream)

    @classmethod
    def from_text(cls, text: str) -> Markdown:
        """
        Parse Markdown instance from the provided text.
        """

        return cls.parse(io.StringIO(text))

    @classmethod
    def parse(cls, stream: io.TextIOBase) -> Markdown:
        """
        Parse Markdown instance from the provided stream.
        """

        line = stream.readline()
        if not is_title(line):
            raise ParseError(
                f'First line of markdown file must be a title, but is "{line}"'
            )

        section, line = cls._parse(stream, line)
        if not line:
            return section
        raise ParseError(
            f'Found additional line "{line}" after top-level section "{section.title}".'
        )

    @classmethod
    def _parse(cls, stream: io.TextIOBase, title: str) -> tuple[Markdown, str]:
        intro = ""
        items = ""
        children = []

        line = stream.readline()
        while is_intro(line):
            intro += line
            line = stream.readline()
        if is_list_item(line):
            while line and not is_title(line):
                items += line
                line = stream.readline()
        while is_title(line) and level(title) < level(line):
            child, line = Markdown._parse(stream, title=line)
            children.append(child)
        return cls(title, intro.strip("\n"), items.strip("\n"), children), line
