import re
from typing import Dict
from pathlib import Path
from _util import _section
from git_access import git_cat_file


class LockPackage():
    def __init__(self):
        self.name = ""
        self.version = ""

    def read(self, line):
        def get(attr: str) -> str:
            regex = re.compile(rf'^{attr} *= *"(.*)"')
            match = regex.match(line)
            return match.group(1) if match else ""

        self.name = self.name or get("name")
        self.version = self.version or get("version")


class PoetryLock:
    def __init__(self, path: Path):
        self.path = path

    def from_working_copy(self) -> Dict[str, str]:
        content = self.path.read_text()
        return self._parse(content)

    def from_tag(self, tag: str) -> Dict[str, str]:
        content = git_cat_file(self.path, tag)
        return self._parse(content)

    def _parse(self, content: str) -> Dict[str, str]:
        relevant = False
        result = {}
        pckg = None
        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            section = _section(line)
            if section:
                if pckg:
                    result[pckg.name] = pckg.version
                relevant = (section == "[package]")
                pckg = LockPackage() if relevant else None
            elif relevant:
                pckg.read(line)

        if pckg:
            result[pckg.name] = pckg.version
        return result
