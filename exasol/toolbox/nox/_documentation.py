from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import webbrowser
from pathlib import Path

import nox
from nox import Session

from exasol.toolbox.nox._shared import DOCS_OUTPUT_DIR
from noxconfig import (
    PROJECT_CONFIG,
    Config,
)


def _build_docs(session: nox.Session, config: Config) -> None:
    session.run(
        "sphinx-build",
        "-W",
        "-b",
        "html",
        f"{config.doc}",
        DOCS_OUTPUT_DIR,
    )


def _build_multiversion_docs(session: nox.Session, config: Config) -> None:
    session.run(
        "sphinx-multiversion",
        f"{config.doc}",
        DOCS_OUTPUT_DIR,
    )
    session.run("touch", f"{DOCS_OUTPUT_DIR}/.nojekyll")


def _git_diff_changes_main() -> int:
    """
    Check if doc/changes is changed and return the exit code of command git diff.
    The exit code is 0 if there are no changes.
    """
    p = subprocess.run(
        [
            "git",
            "diff",
            "--quiet",
            "origin/main",
            "--",
            PROJECT_CONFIG.root / "doc/changes",
        ],
        capture_output=True,
    )
    return p.returncode


@nox.session(name="docs:multiversion", python=False)
def build_multiversion(session: Session) -> None:
    """Builds the multiversion project documentation"""
    _build_multiversion_docs(session, PROJECT_CONFIG)


@nox.session(name="docs:build", python=False)
def build_docs(session: Session) -> None:
    """Builds the project documentation"""
    _build_docs(session, PROJECT_CONFIG)


@nox.session(name="docs:open", python=False)
def open_docs(session: Session) -> None:
    """Opens the built project documentation"""
    docs_folder = PROJECT_CONFIG.root / DOCS_OUTPUT_DIR
    if not docs_folder.exists():
        session.error(f"No documentation could be found. {docs_folder} is missing")
    index = docs_folder / "index.html"
    webbrowser.open_new_tab(index.as_uri())


@nox.session(name="docs:clean", python=False)
def clean_docs(_session: Session) -> None:
    """Removes the documentations build folder"""
    docs_folder = PROJECT_CONFIG.root / DOCS_OUTPUT_DIR
    if docs_folder.exists():
        shutil.rmtree(docs_folder)


def _docs_list_links(doc_config: Path):
    with tempfile.TemporaryDirectory() as path:
        tmpdir = Path(path)
        sp = subprocess.run(  # nosec
            [
                "sphinx-build",
                "-b",
                "linkcheck",
                "-D",
                "linkcheck_ignore=.*",
                doc_config,
                tmpdir,
            ],
            capture_output=True,
            text=True,
        )
        if sp.returncode >= 2:
            return sp.returncode, sp.stderr
        output = tmpdir / "output.json"
        links = output.read_text().split("\n")
        file_links = []
        for link in links:
            if link != "":
                line = json.loads(link)
                if not line["uri"].startswith("#"):
                    file_links.append(line)
        file_links.sort(key=lambda file: file["filename"])
        return 0, "\n".join(
            f"filename: {fl['filename']}:{fl['lineno']} -> uri: {fl['uri']}"
            for fl in file_links
        )


def _docs_links_check(doc_config: Path, args):
    with tempfile.TemporaryDirectory() as path:
        tmpdir = Path(path)
        sp = subprocess.run(  # nosec
            [
                "sphinx-build",
                "-b",
                "linkcheck",
                doc_config,
                tmpdir,
            ],
        )
        if args.output and sp.returncode <= 1:
            result_json = tmpdir / "output.json"
            dst = Path(args.output) / "link-check-output.json"
            shutil.copyfile(result_json, dst)
            print(f"file generated at path: {result_json.resolve()}")
        return sp.returncode, (
            None if sp.returncode >= 2 else (tmpdir / "output.txt").read_text()
        )


@nox.session(name="links:list", python=False)
def docs_list_links(session: Session) -> None:
    """List all the links within the documentation."""
    r_code, text = _docs_list_links(PROJECT_CONFIG.doc)
    print(text)
    if r_code != 0:
        session.error()


@nox.session(name="links:check", python=False)
def docs_links_check(session: Session) -> None:
    """Checks whether all links in the documentation are accessible."""
    parser = argparse.ArgumentParser(
        prog="nox -s links:check",
        usage="nox -s links:check -- [-h] [-o |--output]",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-o", "--output", type=Path, help="path to copy the output json", default=None
    )
    args = parser.parse_args(session.posargs)
    r_code, problems = _docs_links_check(PROJECT_CONFIG.doc, args)
    if r_code >= 2:
        session.error(2)
    if r_code == 1 or problems != "":
        escape_red = "\033[31m"
        print(escape_red + "errors:")
        print(problems)
        session.error(1)


@nox.session(name="changelog:updated", python=False)
def updated(_session: Session) -> None:
    """Checks if the change log has been updated"""
    if _git_diff_changes_main() == 0:
        print(
            "Changelog is not updated.\n"
            "Please describe your changes in the changelog!"
        )
        sys.exit(1)
