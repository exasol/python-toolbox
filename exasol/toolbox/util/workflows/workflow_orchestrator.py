from __future__ import annotations

from collections.abc import Mapping
from functools import cached_property
from pathlib import Path
from typing import (
    Annotated,
    Final,
)

from pydantic import BaseModel

from exasol.toolbox.util.workflows.templates import WORKFLOW_TEMPLATE_OPTIONS

ALL: Final[str] = "all"
WorkflowChoice = Annotated[
    str, f"Should be a value from {[ALL, *WORKFLOW_TEMPLATE_OPTIONS.keys()]}"
]
WORKFLOW_CHOICES: Final[list[str]] = [ALL, *WORKFLOW_TEMPLATE_OPTIONS.keys()]


class WorkflowOrchestrator(BaseModel):
    """Orchestrate workflow rendering, comparison, and writing."""

    workflow_choice: WorkflowChoice

    @cached_property
    def templates(self) -> Mapping[str, Path]:
        """
        A mapping of workflow templates names to paths. This can be a single
        item or all workflow templates.
        """
        if self.workflow_choice == ALL:
            return WORKFLOW_TEMPLATE_OPTIONS
        return {self.workflow_choice: WORKFLOW_TEMPLATE_OPTIONS[self.workflow_choice]}
