import json
from collections.abc import Iterable
from dataclasses import dataclass

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
