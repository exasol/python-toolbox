from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import webbrowser
from itertools import repeat
from pathlib import Path
from typing import (
    Container,
    Iterable,
    Optional,
    Tuple,
)
import argparse

import nox
import requests   # type: ignore
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


def _check_failed_links(results: list[str]):
    errors = []
    for line, result in enumerate(results):
        if result.startswith("{") and "}" in result:
            data = json.loads(result)
            if not (data["status"] == "working") or (data["status"] == "ignored"):
                match = re.search(r"https?://[^\s\"\'<>]+", data["uri"])
                if match:
                    try:
                        request = requests.head(match.group(), timeout=15)
                        if request.status_code == 200:
                            data["status"] = "working"
                            data["code"] = request.status_code
                        results[line] = json.dumps(data)
                    except requests.exceptions.Timeout:
                        pass
                if (data["status"] == "broken") or data["status"] == "timeout":
                    errors.append(result)
    return results, errors


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


@nox.session(name="docs:links", python=False)
def docs_list_links(session: Session) -> None:
    """List all the links within the documentation."""
    with tempfile.TemporaryDirectory() as path:
        tmpdir = Path(path)
        sp = subprocess.run(
            [
                "sphinx-build",
                "-b",
                "linkcheck",
                "-D",
                "linkcheck_ignore=.*",
                PROJECT_CONFIG.root / "doc",
                tmpdir,
            ],
        )
        print(sp.returncode)
        if sp.returncode >= 2:
            print(sp.stderr)
            session.error(2)
        output = tmpdir / "output.json"
        links = output.read_text().split("\n")
        file_links = []
        for link in links:
            if link != "":
                line = json.loads(link)
                if not line["uri"].startswith("#"):
                    file_links.append(line)
        file_links.sort(key=lambda file: file["filename"])
        print(
            "\n".join(
                f"filename: {fl['filename']} -> uri: {fl['uri']}" for fl in file_links
            )
        )


@nox.session(name="docs:links:check", python=False)
def docs_links_check(session: Session) -> None:
    """Checks whether all links in the documentation are accessible."""
    parser = argparse.ArgumentParser(
        prog="nox -s release:prepare",
        usage="nox -s release:prepare -- [-h] [-o |--output]",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="path to output file",
        default="",
    )
    args = parser.parse_args(session.posargs)
    with tempfile.TemporaryDirectory() as path:
        tmpdir = Path(path)
        sp = subprocess.run(
            [
                "sphinx-build",
                "-b",
                "linkcheck",
                PROJECT_CONFIG.root / "doc",
                tmpdir,
            ],
        )
        if sp.returncode >= 2:
            print(sp.stderr)
            session.error(2)
        output = tmpdir / "output.json"
        out = output.read_text().split("\n")
        results, errors = _check_failed_links(out)
        if hasattr(args, "output"):
            outputfile = Path(args.output) / "link-check-output.json"
            if not outputfile.exists():
                outputfile.parent.mkdir(parents=True, exist_ok=True)
                outputfile.touch()
            outputfile.write_text("\n".join(result for result in results))
            print(f"file generated at path: {outputfile.resolve()}")
        if errors:
            print("Error" + "s" if len(errors) > 1 else "")
            print("\n".join(error for error in errors))
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
