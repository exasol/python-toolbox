import subprocess
from typing import Iterable


def tags() -> Iterable[str]:
    """
    Returns a list of all tags, sorted from [0] oldest to [-1] newest.
    PreConditions:
    - the git cli tool is installed and can be found via `$PATH`
    - the code is executed where the working directory is within a git repository
    """
    command = ["git", "tag", "--sort=committerdate"]
    result = subprocess.run(command, capture_output=True, check=True)
    return [tag.strip() for tag in result.stdout.decode("utf-8").splitlines()]
