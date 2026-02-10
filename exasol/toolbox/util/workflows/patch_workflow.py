from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)
from ruamel.yaml import CommentedMap

from exasol.toolbox.util.workflows.render_yaml import YamlRenderer


class ActionType(str, Enum):
    INSERT_AFTER = "INSERT_AFTER"
    REPLACE = "REPLACE"


class StepContent(BaseModel):
    model_config = ConfigDict(extra="allow")  # This allows extra fields

    name: str
    id: str
    uses: str | None = None
    run: str | None = None
    with_: dict[str, Any] | None = Field(None, alias="with")
    env: dict[str, str] | None = None


class StepCustomization(BaseModel):
    action: ActionType
    job: str
    step_id: str
    content: StepContent


class Workflow(BaseModel):
    name: str
    remove_jobs: list[str] = Field(default_factory=list)
    step_customizations: list[StepCustomization] = Field(default_factory=list)


class WorkflowPatcherConfig(BaseModel):
    workflows: list[Workflow]


class WorkflowPatcher(YamlRenderer):
    """
    The :class:`WorkflowPatcher` enables users to define a YAML file
    to customize PTB-provided workflows by removing or modifying jobs in the file.
    A job can be modified by replacing or inserting steps.
    The provided YAML file must meet the conditions of :class:`WorkflowPatcherConfig`.
    """

    def get_yaml_dict(self, file_path: Path) -> CommentedMap:
        loaded_yaml = super().get_yaml_dict(file_path)
        WorkflowPatcherConfig.model_validate(loaded_yaml)
        return loaded_yaml
