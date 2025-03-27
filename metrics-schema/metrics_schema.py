import json
import sys
from datetime import datetime
from pathlib import Path

from pydantic import (
    BaseModel,
    Field,
)

_TOOLBOX_PATH = Path(__file__).parent / ".."
sys.path.append(f"{_TOOLBOX_PATH}")

from exasol.toolbox.metrics import Rating


class Metrics(BaseModel):
    """This schema defines the structure and values for reporting Q/A metrics for projects."""

    project: str = Field(description=("Project Name Corresponding to the metrics."))
    commit: str = Field(
        description=(
            "Commit-Hash pointing to the state of the codebase used for generating the metrics."
        )
    )
    date: datetime = Field(
        description="The date and time when the metrics were recorded."
    )
    coverage: float = Field(
        description="Represents the percentage of the codebase that is covered by automated tests.",
        ge=0,
        le=100,
    )
    maintainability: Rating = Field(
        description="Rating of how easily the codebase can be understood, adapted, and extended.",
    )
    reliability: Rating = Field(
        description="Stability and dependability of the software. "
    )
    security: Rating = Field(
        description="Resilience against security threats and vulnerabilities."
    )
    technical_debt: Rating = Field(
        description="Amount of 'technical debt' in the project."
    )


if __name__ == "__main__":
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://schemas.exasol.com/project-metrics-0.2.0.json",
    }
    schema.update(Metrics.model_json_schema())
    print(json.dumps(schema, indent=2))
