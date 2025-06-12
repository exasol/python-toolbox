import re
from pathlib import Path
from typing import List
from _util import _section


def read_pyproject(path: Path) -> List[str]:
    relevant = False
    suffixes = [
        "dependencies",
        "dev-dependencies",
        ".*\\.dependencies",
    ]
    dependency_groups = [ f"tool\\.poetry\\.{s}" for s in suffixes ]
    regex = re.compile("|".join(dependency_groups))
    result = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        section = _section(line)
        if section:
            relevant = regex.match(section)
        elif relevant:
            d = re.split(" *= *", line, 1)[0]
            result.append(d)
    return result

