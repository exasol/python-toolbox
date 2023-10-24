import json
import re
import subprocess
import sys
from inspect import cleandoc
from typing import (
    Generator,
    Iterable,
    Tuple,
)

import typer
from rich.console import Console

stdout = Console()
stderr = Console(stderr=True)

ISSUE_CLI = typer.Typer()

from dataclasses import (
    asdict,
    dataclass,
)


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
        stderr.print(f"{ex}")
        raise ex

    cve_pattern = re.compile(r"CVE-\d{4}-\d{4,7}")
    issues = json.loads(result.stdout.decode("utf-8"))
    issues = (
        (issue["id"], cve_pattern.search(issue["title"]).group())  # type: ignore
        for issue in issues
        if cve_pattern.search(issue["title"])
    )
    return issues


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
    issues = input.read()
    issues = (line for line in issues.split("\n"))
    issues = (json.loads(raw) for raw in issues)
    issues = (Issue(**obj) for obj in issues)
    yield from issues


def _issues_as_json_str(issues):
    for issue in issues:
        issue = asdict(issue)  # type: ignore
        yield json.dumps(issue)


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


@ISSUE_CLI.command(name="convert")
def convert(
        format: str = typer.Argument(..., help="input format to be converted."),
) -> None:
    if format == "maven":
        issues = from_maven(sys.stdin.read())
        for issue in _issues_as_json_str(issues):
            stdout.print(issue)
    else:
        stderr.print(f"Unsupported format: {format}")
        sys.exit(-1)


@ISSUE_CLI.command(name="filter")
def filter(
        type: str = typer.Argument(..., help="filter type to apply"),
) -> None:
    if type != "github":
        stderr.print(
            f"warning: Invalid filter type: {type}, falling back to pass through mode."
        )
        for line in sys.stdin:
            stdout.print(line, end="")

    to_be_filtered = list(gh_security_issues())
    filtered_issues = [
        issue for issue in _issues(sys.stdin) if issue.cve not in to_be_filtered
    ]

    for issue in _issues_as_json_str(filtered_issues):
        stdout.print(issue)


@ISSUE_CLI.command(name="create")
def create() -> None:
    for line in sys.stdin:
        stdout.print(line, end="")

    title = "🔐 {cve}: {coordinates}"

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
    body = "another test"
    command = [
        "gh",
        "issue",
        "create",
        "--label",
        "security",
        "--title",
        title.format(cve="CVE-TEST", coordinates="some-package"),
        "--body",
        body.format(
            cve="CVE-TEST",
            cwe="CWE-TEST",
            description="Some detailed description",
            references="\n".join(f"- {ref}" for ref in ''),
        ),
    ]

    result = subprocess.run(command, check=True)
    print(result)


CLI = typer.Typer()
CLI.add_typer(ISSUE_CLI, name='issuet s')

if __name__ == "__main__":
    CLI()
