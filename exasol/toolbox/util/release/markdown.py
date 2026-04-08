"""
A project's Changelog is expected to list the changes coming with each of
the project's releases. The Changelog contains a file changelog.md with the
table of contents. and zero or more changes files.

Each changes file is named changes_*.md and describes the changes for a
specific release. The * in the file name equals the version number of the
related release.

All files are in Markdown syntax, divided into sections.  Each section is
identified by its title which should be unique as is represented by class
Markdown.

A section may consist of a prefix and a suffix, either might be empty. The
prefix are some introductory sentences, the suffix is the list of issues in
this section. Optionally each section can contain subsections as children.

Method Markdown.replace_prefix() adds such a prefix or replaces it, when the
section already has one.

The first line of each changes file must be the title describing the version
number, date and name of the release, followed by zero or multiple
sections. The first section is a summary, each other section lists the issues
(aka. tickets) of a particular category the are resolved by this
release. Categories are security, bugfixes, features, documentation, and
refactorings.
"""

from __future__ import annotations

import io


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
    return line and line.startswith("#")


def is_list_item(line: str) -> bool:
    return line and (line.startswith("#") or line.startswith("-"))


def is_intro(line: str) -> bool:
    return line and not is_title(line) and not is_list_item(line)


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

    def add_child(self, child: Markdown, pos: int = 1) -> None:
        """
        Insert the specified section as child at the specified position.
        """

        self.children.insert(pos, self._check(child))

    def replace_child(self, child: Markdown) -> Markdown:
        """
        If there is a child with the same title then replace this child
        otherwise append the specified child.
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
        return isinstance(other, Markdown) and self.rendered == other.rendered

    @classmethod
    def read(cls, path: Path) -> Markdown:
        return cls.parse(path.read_text())

    @classmethod
    def parse(cls, content: str) -> Markdown:
        stream = io.StringIO(content)
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
            while not is_title(line):
                items += line
                line = stream.readline()
        while is_title(line) and level(title) < level(line):
            child, line = Markdown._parse(stream, title=line)
            children.append(child)
        return Markdown(title, intro.strip("\n"), items.strip("\n"), children), line


def sample():
    content = ""
    changes = Markdown.parse(content)
    resolved_vulnerabilities = ""
    intro = resolved_vulnerabilities
    title = "# title"
    if section := changes.child(title):
        section.intro = intro
    else:
        changes.add_child(Markdown(title, intro))
