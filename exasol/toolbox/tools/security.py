"""This module contains security related CLI tools and code"""
import json
from enum import Enum
import re
import subprocess
import sys
from dataclasses import (
    asdict,
    dataclass,
)
from functools import partial
from inspect import cleandoc
from typing import (
    Generator,
    Iterable,
    Tuple,
)

import typer

stdout = print
stderr = partial(print, file=sys.stderr)


# Note:
# In the long term we may want to adapt the official CVE json schema,
# support for this could be generated using pydantic.
# See here: https://github.com/CVEProject/cve-schema/blob/master/schema/v5.0/CVE_JSON_5.0_schema.json
@dataclass(frozen=True)
class Issue:
    cve: str
    cwe: str
    description: str
    coordinates: str
    references: tuple


def _issues(input) -> Generator[Issue, None, None]:
    for line in input:
        obj = json.loads(line)
        yield Issue(**obj)


def _issues_as_json_str(issues):
    for issue in issues:
        issue = asdict(issue)  # type: ignore
        yield json.dumps(issue)


def gh_security_issues() -> Generator[Tuple[str, str], None, None]:
    """
    Yields issue-id, cve-id pairs for all (closed, open) issues associated with CVEs

    Return:
        A generator which yield tuples of (id,title).

    Raises:
        subprocess.CalledProcessError: If the underlying command fails.
    """
    command = [
        "gh",
        "issue",
        "list",
        "--label",
        "security",
        "--search",
        "CVE",
        "--json",
        "id,title",
        "--limit",
        "1000",
        "--state",
        "all",
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True)
    except FileNotFoundError as ex:
        msg = "Command 'gh' not found. Please make sure you have installed the github cli."
        raise FileNotFoundError(msg) from ex
    except subprocess.CalledProcessError as ex:
        stderr(f"{ex}")
        raise ex

    cve_pattern = re.compile(r"CVE-\d{4}-\d{4,7}")
    issues = json.loads(result.stdout.decode("utf-8"))
    issues = (
        (issue["id"], cve_pattern.search(issue["title"]).group())  # type: ignore
        for issue in issues
        if cve_pattern.search(issue["title"])
    )
    return issues


def from_maven(report: str) -> Iterable[Issue]:
    # Note: Consider adding warnings if there is the same cve with multiple coordinates
    report = json.loads(report)
    dependencies = report["vulnerable"]  # type: ignore
    for _, dependency in dependencies.items():  # type: ignore
        for v in dependency["vulnerabilities"]:  # type: ignore
            references = [v["reference"]] + v["externalReferences"]
            yield Issue(
                cve=v["cve"],
                cwe=v["cwe"],
                description=v["description"],
                coordinates=dependency["coordinates"],
                references=tuple(references),
            )


def security_issue_title(issue: Issue) -> str:
    return f"🔐 {issue.cve}: {issue.coordinates}"


def security_issue_body(issue: Issue) -> str:
    def as_markdown_listing(elements: Iterable[str]):
        return "\n".join(f"- {element}" for element in elements)

    body = cleandoc(
        """
        ## Summary
        {description}

        CVE: {cve}
        CWE: {cwe}

        ## References
        {references}
        """
    )
    return body.format(
        cve=issue.cve,
        cwe=issue.cwe,
        description=issue.description,
        references=as_markdown_listing(issue.references),
    )


def create_security_issue(issue: Issue) -> Tuple[str, str]:
    command = [
        "gh",
        "issue",
        "create",
        "--label",
        "security",
        "--title",
        security_issue_title(issue),
        "--body",
        security_issue_body(issue),
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True)
    except FileNotFoundError as ex:
        msg = "Command 'gh' not found. Please make sure you have installed the github cli."
        raise FileNotFoundError(msg) from ex
    except subprocess.CalledProcessError as ex:
        stderr(f"{ex}")
        raise ex

    std_err = result.stderr.decode("utf-8")
    std_out = result.stdout.decode("utf-8")

    return std_err, std_out


CLI = typer.Typer()
CVE_CLI = typer.Typer()
CLI.add_typer(CVE_CLI, name="cve", help="Work with CVE's")


class Format(str, Enum):
    Maven = 'maven'


# pylint: disable=redefined-builtin
@CVE_CLI.command(name="convert")
def convert(
        format: Format = typer.Argument(..., help="input format to be converted."),
) -> None:
    def _maven():
        issues = from_maven(sys.stdin.read())
        for issue in _issues_as_json_str(issues):
            stdout(issue)
        raise typer.Exit(code=0)

    actions = {Format.Maven: _maven}
    action = actions[format]
    action()


class Filter(str, Enum):
    Github = 'github'
    PassThrough = 'pass-through'


# pylint: disable=redefined-builtin
@CVE_CLI.command(name="filter")
def filter(
        type: Filter = typer.Argument(help="filter type to apply"),
) -> None:
    """
    Filter specific CVE's from the input

    Args:
        type:  of filter which shall be applied.
    """

    def _github():
        to_be_filtered = {cve for _, cve in gh_security_issues()}
        stderr(
            "Filtering:\n{issues}".format(
                issues="\n".join(f"- {i}" for i in to_be_filtered)
            )
        )
        filtered_issues = [
            issue for issue in _issues(sys.stdin) if issue.cve not in to_be_filtered
        ]
        for issue in _issues_as_json_str(filtered_issues):
            stdout(issue)

        raise typer.Exit(code=0)

    def _pass_through():
        for line in sys.stdin:
            stdout(line)

        raise typer.Exit(code=0)

    actions = {Filter.Github: _github, Filter.PassThrough: _pass_through()}
    action = actions[type]
    action()


@CVE_CLI.command(name="create")
def create() -> None:
    """Create GitHub issues for CVE's"""
    for issue in _issues(sys.stdin):
        std_err, std_out = create_security_issue(issue)
        stderr(std_err)
        stdout(std_out)


if __name__ == "__main__":
    CLI()
