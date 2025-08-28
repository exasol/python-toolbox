from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

import nox
from nox import Session

from exasol.toolbox.nox._shared import (
    Mode,
    _version,
)
from exasol.toolbox.nox.plugin import NoxTasks
from exasol.toolbox.util.git import Git
from exasol.toolbox.util.release.changelog import Changelogs
from exasol.toolbox.util.version import (
    ReleaseTypes,
    Version,
)
from noxconfig import PROJECT_CONFIG


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nox -s release:prepare",
        usage="nox -s release:prepare -- [-h] [-t | --type {major,minor,patch}]",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-t",
        "--type",
        type=ReleaseTypes,
        help="specifies which type of upgrade is to be performed",
        required=True,
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--no-add",
        default=False,
        action="store_true",
        help="Neither add nor commit the changes",
    )
    parser.add_argument(
        "--no-branch",
        default=False,
        action="store_true",
        help="Do not create a branch to commit the changes on",
    )
    parser.add_argument(
        "--no-pr",
        default=False,
        action="store_true",
        help="Do not create a pull request for the changes",
    )
    return parser


def _update_project_version(session: Session, version: Version) -> Version:
    session.run("poetry", "version", f"{version}")
    _version(session, Mode.Fix)
    return version


def _add_files_to_index(session: Session, files: list[Path]) -> None:
    for file in files:
        session.run("git", "add", f"{file}")


class ReleaseError(Exception):
    """Error during trigger release"""


def _trigger_release(project_config) -> Version:
    def run(*args: str):
        try:
            return subprocess.run(
                args, capture_output=True, text=True, check=True
            ).stdout
        except subprocess.CalledProcessError as ex:
            raise ReleaseError(
                f"failed to execute command {ex.cmd}\n\n{ex.stderr}"
            ) from ex

    branches = run("git", "remote", "show", "origin")
    if not (result := re.search(r"HEAD branch: (\S+)", branches)):
        raise ReleaseError("default branch could not be found")
    default_branch = result.group(1)

    run("git", "checkout", default_branch)
    run("git", "pull")

    release_version: Version = Version.from_poetry()
    print(f"release version: {release_version}")

    if re.search(rf"{release_version}", run("git", "tag", "--list")):
        raise ReleaseError(f"tag {release_version} already exists")
    if re.search(rf"{release_version}", run("gh", "release", "list")):
        raise ReleaseError(f"release {release_version} already exists")

    run("git", "tag", str(release_version))
    run("git", "push", "origin", str(release_version))

    if (
        hasattr(project_config, "create_major_version_tags")
        and project_config.create_major_version_tags
    ):
        major_release_version = f"v{release_version.major}"
        run("git", "tag", "-f", str(major_release_version))
        run("git", "push", "-f", "origin", str(major_release_version))

    return release_version


@nox.session(name="release:prepare", python=False)
def prepare_release(session: Session) -> None:
    """
    Prepare the project for a new release.
    """
    parser = _create_parser()
    args = parser.parse_args(session.posargs)
    new_version = Version.upgrade_version_from_poetry(args.type)

    if not args.no_branch and not args.no_add:
        Git.create_and_switch_to_branch(f"release/prepare-{new_version}")

    _ = _update_project_version(session, new_version)

    changelogs = Changelogs(
        changes_path=PROJECT_CONFIG.doc / "changes",
        root_path=PROJECT_CONFIG.root,
        version=new_version,
    )
    changelogs.update_changelogs_for_release()
    changed_files = changelogs.get_changed_files()

    pm = NoxTasks.plugin_manager(PROJECT_CONFIG)
    pm.hook.prepare_release_update_version(
        session=session, config=PROJECT_CONFIG, version=new_version
    )

    if args.no_add:
        return

    changed_files += [
        PROJECT_CONFIG.root / "pyproject.toml",
        PROJECT_CONFIG.version_file,
    ]
    results = pm.hook.prepare_release_add_files(session=session, config=PROJECT_CONFIG)
    changed_files += [f for plugin_response in results for f in plugin_response]
    _add_files_to_index(
        session,
        changed_files,
    )
    session.run("git", "commit", "-m", f"Prepare release {new_version}")

    if not args.no_pr:
        session.run(
            "gh",
            "pr",
            "create",
            "--title",
            f"Prepare release {new_version}",
            "--body",
            '""',
        )


@nox.session(name="release:trigger", python=False)
def trigger_release(session: Session) -> None:
    """trigger an automatic project release"""
    print(f"new version: {_trigger_release(PROJECT_CONFIG)}")
