import typer
import json
from pathlib import Path
from inspect import cleandoc
from dataclasses import dataclass
from collections.abc import Iterable

CLI = typer.Typer()


@dataclass(frozen=True)
class LintIssue:
    type: str
    module: str
    obj: str
    line: int
    column: int
    endLine: int
    endColumn: int
    path: str
    symbol: str
    message: str
    message_id: str


def lint_issue_from_json(data: str) -> Iterable[LintIssue]:
    issues = json.loads(data)
    for issue in issues:
        yield LintIssue(
            type=issue["type"],
            module=issue["module"],
            obj=issue["obj"],
            line=issue["line"],
            column=issue["column"],
            endLine=issue["endLine"],
            endColumn=issue["endColumn"],
            path=issue["path"],
            symbol=issue["symbol"],
            message=issue["message"],
            message_id=issue["message-id"],
        )


def lint_issue_to_markdown(lint_issues: Iterable[LintIssue]) -> str:
    def _header() -> str:
        header = "# Static Code Analysis\n\n"
        header += "|File|line/ column|id|message|\n"
        header += "|---|:-:|:-:|---|\n"
        return header

    def _rows(issues: Iterable[LintIssue]) -> str:
        rows = ""
        for issue in issues:
            rows += f"|{issue.path}"
            rows += f"|line: {issue.line}/<br>column: {issue.column}/"
            rows += f"|{issue.message_id}"
            rows += f"|{issue.message}|\n"
        return rows
    template = cleandoc(
        """
        {header}{rows}
        """
    )
    lint_issues = sorted(
        lint_issues,
        key=lambda i: (i.path, i.message_id, i.line)
    )
    return template.format(header=_header(), rows=_rows(lint_issues))


@CLI.command(name="pretty-print")
def lint_json_to_markdown(
    path: Path = typer.Argument(default=Path(".lint.json"), help="path to lint.json"),
) -> None:
    """converts the lint json to a Markdown table"""
    issues = lint_issue_from_json(path.read_text())
    print(lint_issue_to_markdown(issues))


if __name__ == "__main__":
    CLI()
