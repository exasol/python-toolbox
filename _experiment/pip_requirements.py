import re
from pathlib import Path
from typing import Dict
from git_access import git_cat_file

class PipRequirements:
    def __init__(self, path: Path):
        self.path = path

    def from_working_copy(self) -> Dict[str, str]:
        content = self.path.read_text()
        return self._parse(content)

    def from_tag(self, tag: str) -> Dict[str, str]:
        content = git_cat_file(self.path, tag)
        return self._parse(content)

    def _parse(self, content: str) -> Dict[str, str]:
        regex = re.compile(r'^(.*) *(==|>=|>) *([^ ]*)')
        result = {}
        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            match = regex.match(line)
            if match:
                result[match.group(1)] = match.group(3)
        return result
