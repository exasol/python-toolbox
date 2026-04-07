"""
A project's Changelog is expected to list the changes coming with each of
the project's releases. The Changelog contains a file changelog.md with the
table of contents. and zero or more changes files. All files are in Markdown
syntax.

Each changes file is named changes_*.md and describes the changes for a
specific release. The * in the file name is identical to the version number of
the related release.

Each changes file starts with a section describing the version number, date
and name of the release and one or more subsections. The first subsection is a
summary, each other subsection lists the issues (aka. tickets) of a particular
category the are resolved by this release. Categories are security, bugfixes,
features, documentation, and refactorings.

For the sake of simplicity, class ChangesFile maintains the sections as a
sequence, ignoring their hierarchy.

Each section may consist of a prefix and a suffix, either might be empty. The
prefix are some introductory sentences, the suffix is the list of issues in
this section.

Method Section.replace_prefix() adds such a prefix or replaces it, when the
section already has one.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from inspect import cleandoc


class ParseError(Exception):
    """
    Indicates inconsistencies when parsing a changelog from raw
    text. E.g. a section with a body but no title.
    """


@dataclass
class Section:
    title: str
    body: str

    @property
    def rendered(self) -> str:
        return f"{self.title}\n\n{self.body}"

    def replace_prefix(self, prefix: str) -> None:
        """
        Prepends the specified prefix to the body of the section.

        If the body starts with the first line of the specified prefix, then
        replace the body's prefix. The body's prefix is all text before a
        markdown list.
        """
        flags = re.DOTALL | re.MULTILINE
        if not self.body.startswith(prefix.splitlines()[0]):
            self.body = f"{prefix}\n\n{self.body}" if self.body else prefix
        elif re.search(r"^[*-] ", self.body, flags=flags):
            suffix = re.sub(r".*?^([*-])", r"\1", self.body, count=1, flags=flags)
            self.body = f"{prefix}\n\n{suffix}"
        else:
            self.body = prefix


@dataclass
class ChangesFile:
    """
    Represents file unreleased.md or changes_*.py in folder doc/changes/.
    """

    sections: list[Section]

    def get_section(self, title: str) -> Section | None:
        """
        Retrieve the section with the specified title.
        """

        pattern = re.compile(f"#+ {re.escape(title)}$")
        return next((s for s in self.sections if pattern.match(s.title)), None)

    def add_section(self, section: Section, pos: int = 1) -> None:
        """
        Insert the specified section at the specified position.
        """

        self.sections.insert(pos, section)

    @property
    def rendered(self) -> str:
        return "\n\n".join(s.rendered for s in self.sections)

    @classmethod
    def parse(cls, content: str) -> ChangesFile:
        title = None
        body = []
        sections = []

        def is_body(line: str) -> bool:
            return not line.startswith("#")

        def process_section():
            nonlocal sections
            if title:
                sections.append(Section(title, cleandoc("\n".join(body))))

        for line in content.splitlines():
            if is_body(line):
                if not title:
                    raise ParseError(f"Found body line without preceding title: {line}")
                body.append(line)
                continue
            # found new title
            process_section()
            title = line
            body = []

        process_section()
        return ChangesFile(sections)


def sample():
    changes = ChangesFile.parse(content)
    if section := changes.get_section(title):
        section.replace_prefix(body)
    else:
        changes.add_section(Section(title, body))
