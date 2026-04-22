import json
from collections.abc import Iterable
from dataclasses import dataclass
from inspect import cleandoc

import typer

CLI = typer.Typer()


@dataclass(frozen=True)
class Finding:
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


def lint_issue_from_json(data: str) -> Iterable[Finding]:
    issues = json.loads(data)
    for issue in issues:
        yield Finding(
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


def lint_issue_to_markdown(lint_issues: Iterable[Finding]) -> str:
    def _header() -> str:
        header = "# Static Code Analysis\n\n"
        header += "|File|line/<br>column|id|message|\n"
        header += "|---|:-:|:-:|---|\n"
        return header

    def _rows(findings: Iterable[Finding]) -> str:
        rows = ""
        for finding in findings:
            rows += f"|{finding.path}"
            rows += f"|line: {finding.line}/<br>column: {finding.column}"
            rows += f"|{finding.message_id}"
            rows += f"|{finding.message}|\n"
        return rows

    template = cleandoc("""
        {header}{rows}
        """)
    lint_issues = sorted(lint_issues, key=lambda i: (i.path, i.message_id, i.line))
    return template.format(header=_header(), rows=_rows(lint_issues))
