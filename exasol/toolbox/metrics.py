import datetime
import json
import re
from collections import defaultdict
from dataclasses import (
    asdict,
    dataclass,
)
from enum import (
    Enum,
    auto,
)
from functools import singledispatch
from inspect import cleandoc
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Union,
)


class Rating(Enum):
    """
    A = Excellent
    B = Good
    C = Satisfactory (Ok, could be better though)
    D = Poor (Improvement necessary)
    E = Bad (Need for action)
    F = Broken (Get it fixed!)
    N/A = Rating is not available
    """

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    NotAvailable = "N/A"

    def __format__(self, format_spec: str) -> str:
        if format_spec == "n":
            return f"{self.value}"
        return str(self)

    @staticmethod
    def from_score(score: float) -> "Rating":
        if 0 <= score < 1:
            return Rating.F
        elif 1 <= score < 3:
            return Rating.E
        elif 3 <= score < 4:
            return Rating.D
        elif 4 <= score < 6:
            return Rating.C
        elif 6 <= score < 8:
            return Rating.B
        elif 8 <= score <= 10:
            return Rating.A
        else:
            raise ValueError(
                "Uncategorized score, score should be in the following interval [0,10]."
            )

    @staticmethod
    def bandit_rating(score: float) -> "Rating":
        score = round(score, 3)
        if score == 0:
            return Rating.F
        elif 0 < score <= 2:
            return Rating.E
        elif 2 < score <= 4:
            return Rating.D
        elif 4 < score <= 5:
            return Rating.C
        elif 5 < score <= 6:
            return Rating.B
        elif 6 < score <= 7:
            return Rating.A
        else:
            raise ValueError(
                "Uncategorized score, score should be in the following interval [0,7]."
            )


@dataclass(frozen=True)
class Report:
    commit: str
    date: datetime.datetime
    coverage: float
    maintainability: Rating
    reliability: Rating
    security: Rating
    technical_debt: Rating


def total_coverage(file: Union[str, Path]) -> float:
    with TemporaryDirectory() as tmpdir:
        tmp_dir = Path(tmpdir)
        report = tmp_dir / "coverage.json"
        run(
            ["coverage", "json", f"--data-file={file}", "-o", f"{report}"],
            capture_output=True,
            check=True,
        )
        with open(report, encoding="utf-8") as r:
            data = json.load(r)
            total: float = data["totals"]["percent_covered"]

        return total


def _static_code_analysis(file: Union[str, Path]) -> Rating:
    def pylint(f: Union[str, Path]) -> Rating:
        expr = re.compile(r"^Your code has been rated at (\d+.\d+)/.*", re.MULTILINE)
        with open(f, encoding="utf-8") as results:
            data = results.read()

        matches = expr.search(data)
        if matches:
            groups = matches.groups()
        try:
            group = groups[0]
            score = Rating.from_score(float(group))
        except Exception:
            score = Rating.NotAvailable

        return score

    pylint_score = pylint(file)
    return pylint_score


def maintainability(file: Union[str, Path]) -> Rating:
    return _static_code_analysis(file)


def reliability() -> Rating:
    return Rating.NotAvailable


def security(file: Union[str, Path]) -> Rating:
    with open(file) as json_file:
        security_lint = json.load(json_file)
    return Rating.bandit_rating(bandit_scoring(security_lint["results"]))


def bandit_scoring(ratings: List[Dict[str, Any]]) -> float:
    evaluation = {"LL": 0, "LM": 0, "LH": 0, "ML": 0, "MM": 0, "MH": 0}
    multiplier = {"LL": 6, "LM": 5, "LH": 4, "ML": 3, "MM": 2, "MH": 1}
    for infos in ratings:
        if infos["issue_severity"] == "HIGH":
            return 0.0
        elif infos["issue_severity"] == "MEDIUM":
            severity = "M"
        elif infos["issue_severity"] == "LOW":
            severity = "L"
        else:
            severity = "H"
        if infos["issue_confidence"] == "HIGH":
            confidence = "H"
        elif infos["issue_confidence"] == "MEDIUM":
            confidence = "M"
        elif infos["issue_confidence"] == "LOW":
            confidence = "L"
        else:
            confidence = "H"
        evaluation[f"{severity}{confidence}"] += 1

    print(evaluation)
    weighting = {
        "MH": evaluation["MH"] * (1 / (2 ** (1 / 4))) ** 5,
        "MM": evaluation["MM"] * (1 / (2 ** (1 / 4))) ** 4,
        "ML": evaluation["ML"] * (1 / (2 ** (1 / 4))) ** 3,
        "LH": evaluation["LH"] * (1 / (2 ** (1 / 4))) ** 2,
        "LM": evaluation["LM"] * (1 / (2 ** (1 / 4))) ** 1,
        "LL": evaluation["LL"] * (1 / (2 ** (1 / 4))) ** 0,
    }
    score = 0.0
    quantity = 0.0
    for level in weighting:
        score += weighting[level] * multiplier[level]
        quantity += weighting[level]
    if quantity == 0:
        return 7
    return score / quantity


def technical_debt() -> Rating:
    return Rating.NotAvailable


def create_report(
    commit: str,
    date: Optional[datetime.datetime] = None,
    coverage_report: Union[str, Path] = ".coverage",
    pylint_report: Union[str, Path] = ".lint.txt",
    bandit_report: Union[str, Path] = ".security.json",
) -> Report:
    return Report(
        commit=commit,
        date=date if date is not None else datetime.datetime.now(),
        coverage=total_coverage(coverage_report),
        maintainability=maintainability(pylint_report),
        reliability=reliability(),
        security=security(bandit_report),
        technical_debt=technical_debt(),
    )


class Format(Enum):
    Text = auto()
    Json = auto()
    Markdown = auto()

    @staticmethod
    def from_string(value: str) -> "Format":
        key = value.lower()
        dispatcher = {
            "json": Format.Json,
            "markdown": Format.Markdown,
            "text": Format.Text,
        }
        try:
            fmt = dispatcher[key]
        except KeyError as ex:
            raise ValueError(f"No known conversion for [{value}]") from ex
        return fmt


@singledispatch
def color(value: Any) -> str:
    return ""


@color.register
def _rating_color(value: Rating) -> str:
    return {
        Rating.A: "brightgreen",
        Rating.B: "green",
        Rating.C: "yellowgreen",
        Rating.D: "yellow",
        Rating.E: "orange",
        Rating.F: "red",
        Rating.NotAvailable: "black",
    }[value]


@color.register(float)
@color.register(int)
def _coverage_color(value: Union[float, int]) -> str:
    if 0 <= value < 20:
        return _rating_color(Rating.F)
    elif 20 <= value < 50:
        return _rating_color(Rating.E)
    elif 50 <= value < 70:
        return _rating_color(Rating.D)
    elif 70 <= value < 80:
        return _rating_color(Rating.C)
    elif 80 <= value < 90:
        return _rating_color(Rating.B)
    elif 90 <= value <= 100:
        return _rating_color(Rating.A)
    else:
        return _rating_color(Rating.NotAvailable)


def _json(report: Report) -> str:
    def identity(obj: Any) -> Any:
        return obj

    transformation: Dict[type, Callable[[Any], Any]] = defaultdict(
        lambda: identity,
        {
            Rating: lambda value: f"{value:n}",
            datetime.datetime: lambda value: str(value),
        },
    )
    data = asdict(report)
    normalized = {k: transformation[type(v)](v) for k, v in data.items()}
    return json.dumps(normalized)


def _markdown(report: Report) -> str:
    col1_width = 25
    col2_width = 75

    def _key(name: str) -> str:
        return name.lower().replace(" ", "_")

    data = asdict(report)
    colors = {name: color(data[name]) for name in data}
    entries = {
        "Commit": "{value}",
        "Date": "{value}",
        "Coverage": "![Coverage](https://img.shields.io/badge/-{value:.2f}%25-{color})",
        "Maintainability": "![Maintainability](https://img.shields.io/badge/-{value:n}-{color})",
        "Reliability": "![Reliability](https://img.shields.io/badge/-{value:n}-{color})",
        "Security": "![Security](https://img.shields.io/badge/-{value:n}-{color})",
        "Technical Debt": "![Technical Debt](https://img.shields.io/badge/-{value:n}-{color})",
    }
    row = f"| {{0:<{col1_width}}} | {{1:<{col2_width}}} | "
    rows = (
        row.format(name, entry.format(value=data[_key(name)], color=colors[_key(name)]))
        for name, entry in entries.items()
    )

    return cleandoc(
        """
    {heading}
    {seperator}
    {entries}
    """
    ).format(
        heading=row.format("Category", "Status"),
        seperator=row.format("-" * col1_width, "-" * col2_width),
        entries="\n".join(rows),
    )


def _text(report: Report) -> str:
    def _name(key: str) -> str:
        return f"{key[0].upper()}{key[1:]}:"

    def _value(value: Any) -> str:
        if isinstance(value, (int, float)):
            return f"{value:.2f}%"
        elif isinstance(value, Rating):
            return f"{value:n}"
        return str(value)

    line = "{0:<25}{1:<75}"
    entries = asdict(report)
    return "\n".join(
        [line.format(_name(key), _value(value)) for key, value in entries.items()]
    )


def format_report(report: Report, fmt: Format) -> str:
    dispatcher = {Format.Json: _json, Format.Markdown: _markdown, Format.Text: _text}
    return dispatcher[fmt](report)
