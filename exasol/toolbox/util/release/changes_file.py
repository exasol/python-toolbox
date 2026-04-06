from __future__ import annotations

import re
from dataclasses import dataclass
from inspect import cleandoc


class ParseError(Exception):
    ...


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
        elif re.search(r"^\*", self.body, flags=flags):
            suffix = re.sub(r".*?^\*", "*", self.body, count=1, flags=flags)
            self.body = f"{prefix}\n\n{suffix}"
        else:
            self.body = prefix


@dataclass
class ChangesFile:
    """
    Represents file unreleased.md or changes_*.py in folder doc/changes/.
    """

    sections: list[Section]

    def get(self, title: str) -> Section | None:
        """
        Retrieve the section with the specified title.
        """

        pattern = re.compile(f"#+ {re.escape(title)}$")
        return next((s for s in self.sections if pattern.match(s.title)), None)

    def add(self, section: Section, pos: int = 1) -> None:
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
    changes = ChangesFile()
    if section := changes.section(name):
        section.replace_prefix(body)
    else:
        changes.add_section(name, body)
