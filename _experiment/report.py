import argparse
import sys

from pathlib import Path
from git_access import latest_tag

from dependencies import DependencyChanges, DependencyReport
from pyproject import read_pyproject
from poetry_lock import PoetryLock
from pip_requirements import PipRequirements


def arg_parser():
    parser = argparse.ArgumentParser("Report dependency changes")
    parser.add_argument(
        "--pyproject", type=Path, default=Path("pyproject.toml"),
        help="pyproject.toml to read direct dependencies from",
    )
    parser.add_argument(
        "--tag", help="branch or tag to use in stead of latest tag",
    )
    return parser


def pyproject_dep_changes(pyproject_file: Path, tag: str):
    poetry_lock = PoetryLock(pyproject_file.parent / "poetry.lock")
    result = DependencyChanges(f"File `{pyproject_file.name}`")
    result.dependencies = read_pyproject(pyproject_file)
    result.old = poetry_lock.from_tag(tag)
    result.new = poetry_lock.from_working_copy()
    return result


def pip_req_changes(file: Path, tag: str):
    pip_requirements = PipRequirements(file)
    result = DependencyChanges(f"File `{file.name}`")
    result.old = pip_requirements.from_tag(tag)
    result.new = pip_requirements.from_working_copy()
    dependencies = set(result.new.keys()).union(result.old.keys())
    result.dependencies = list(dependencies)
    return result


if __name__ == "__main__":
    args = arg_parser().parse_args()
    tag = args.tag or latest_tag()

    report = DependencyReport(tag)
    report.add_changes(
        pyproject_dep_changes(args.pyproject, tag)
    )

    dir = args.pyproject.parent / "exasol/ds/sandbox/runtime/ansible/roles/jupyter/files"
    if dir.is_dir():
        report.add_changes(pip_req_changes(dir / "jupyter_requirements.txt", tag))
        report.add_changes(pip_req_changes(dir / "notebook_requirements.txt", tag))

    report.generate()


