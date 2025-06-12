import subprocess
from pathlib import Path
import sys

def _run(command: str):
    p = subprocess.run(command.split(), encoding="utf-8", capture_output=True)
    if p.returncode != 0:
        print(
            f'Command "{command}"'
            f' terminated with exit code {p.returncode}:'
            f'\n{p.stderr}',
            file=sys.stderr,
        )
        sys.exit(1)
    return p.stdout.strip()


def latest_tag():
    return _run("git describe --tags --abbrev=0")


def git_cat_file(path: Path, tag: str):
    """
    Get the contents of the specified file ``path`` at the point in time
    specified by git tag ``tag``.
    """
    return _run(f"git cat-file blob {tag}:{path}")
