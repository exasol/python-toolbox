import json
import re
import subprocess
import sys
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

from dataclasses import (
    asdict,
    dataclass,
)


# Note:
# In the long term we may want to adapt the official CVE json schema,
# support for this could be generated using pydantic.
# See here: https://github.com/CVEProject/cve-schema/blob/master/schema/v5.0/CVE_JSON_5.0_schema.json
@dataclass(frozen=True)
class Issue:
    # Note: Add support additional (custom) information e.g. dependency tree etc.
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
ISSUE_CLI = typer.Typer()
CLI.add_typer(ISSUE_CLI, name="issue")


@ISSUE_CLI.command(name="convert")
def convert(
    format: str = typer.Argument(..., help="input format to be converted."),
) -> None:
    if format == "maven":
        issues = from_maven(sys.stdin.read())
        for issue in _issues_as_json_str(issues):
            stdout(issue)
    else:
        stderr(f"Unsupported format: {format}")
        sys.exit(-1)


@ISSUE_CLI.command(name="filter")
def filter(
    type: str = typer.Argument(..., help="filter type to apply"),
) -> None:
    if type != "github":
        stderr(
            f"warning: Invalid filter type: {type}, falling back to pass through mode."
        )
        for line in sys.stdin:
            stdout(line)

    to_be_filtered = list(gh_security_issues())
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


@ISSUE_CLI.command(name="create")
def create() -> None:
    for issue in _issues(sys.stdin):
        std_err, std_out = create_security_issue(issue)
        stderr(std_err)
        stdout(std_out)


if __name__ == "__main__":
    CLI()
