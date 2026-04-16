import datetime
import json
import re
import subprocess
import sys
from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import (
    Any,
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
        if score <= 0.2:
            return Rating.F
        elif 0.2 < score <= 1.6:
            return Rating.E
        elif 1.6 < score <= 3:
            return Rating.D
        elif 3 < score <= 4.4:
            return Rating.C
        elif 4.4 < score <= 5.8:
            return Rating.B
        elif 5.8 < score <= 6:
            return Rating.A
        else:
            raise ValueError(
                "Uncategorized score, score should be in the following interval [0,6]."
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


def total_coverage(file: str | Path) -> float:
    with TemporaryDirectory() as tmpdir:
        tmp_dir = Path(tmpdir)
        report = tmp_dir / "coverage.json"
        p = subprocess.run(
            ["coverage", "json", f"--data-file={file}", "-o", f"{report}"],
            capture_output=True,
            check=False,
            encoding="utf-8",
        )
        stdout = p.stdout.strip()

        if p.returncode != 0:
            message = (
                f"The following command"
                f" returned non-zero exit status {p.returncode}:\n"
                f'  {" ".join(p.args)}\n'
                f"{stdout}"
            )
            if (p.returncode == 1) and (stdout == "No data to report."):
                print(f"{message}\nReturning total coverage 100 %.", file=sys.stderr)
                return 100.0
            else:
                raise RuntimeError(message)

        with open(report, encoding="utf-8") as r:
            data = json.load(r)
            total: float = data["totals"]["percent_covered"]

        return total


def _static_code_analysis(file: str | Path) -> Rating:
    def pylint(f: str | Path) -> Rating:
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


def maintainability(file: str | Path) -> Rating:
    return _static_code_analysis(file)


def reliability() -> Rating:
    return Rating.NotAvailable


def security(file: str | Path) -> Rating:
    with open(file) as json_file:
        security_lint = json.load(json_file)
    return Rating.bandit_rating(_bandit_scoring(security_lint["results"]))


def _bandit_scoring(ratings: list[dict[str, Any]]) -> float:
    def char(value: str, default: str = "H") -> str:
        if value in ["HIGH", "MEDIUM", "LOW"]:
            return value[0]
        return default

    weight = {
        "LL": 1 / 18,
        "LM": 1 / 15,
        "LH": 1 / 12,
        "ML": 1 / 9,
        "MM": 1 / 6,
        "MH": 1 / 3,
    }
    exp = 0.0
    for infos in ratings:
        severity = infos["issue_severity"]
        if severity == "HIGH":
            return 0.0
        index = char(severity) + char(infos["issue_confidence"])
        exp += weight[index]
    return 6 * (2**-exp)
