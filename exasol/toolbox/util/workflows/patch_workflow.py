from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
)
from ruamel.yaml import CommentedMap

from exasol.toolbox.util.workflows.render_yaml import YamlRenderer


class InvalidWorkflowPatcherYamlError(Exception):
    def __init__(self, file_path: Path):
        super().__init__(
            f"File '{file_path}' is malformed; it failed Pydantic validation."
        )


class ActionType(str, Enum):
    INSERT_AFTER = "INSERT_AFTER"
    REPLACE = "REPLACE"


class StepContent(BaseModel):
    """
    The :class:`StepContent` is used to lightly validate the content which
    would be used to REPLACE or INSERT_AFTER the specified step in the GitHub workflow.

    With the value `ConfigDict(extra="allow")`, this model allows for further fields
    (e.g. `dummy`) to be specified without any validation. This design choice was
    intentional, as GitHub already allows additional fields and may specify more fields
    than what has been specified in this model.

    As the validation here is light, it is left to GitHub to validate the content.
    For further information on what is allowed & expected for the fields, refer to
    `GitHub's documentation on jobs.<job_id>.steps <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idsteps>`__.
    """

    model_config = ConfigDict(extra="allow")  # This allows extra fields

    name: str
    id: str
    uses: str | None = None
    run: str | None = None
    with_: dict[str, Any] | None = Field(None, alias="with")
    env: dict[str, str] | None = None


class StepCustomization(BaseModel):
    """
    The :class:`StepCustomization` is used to specify the desired modification:
      * REPLACE - means that the contents of the specified `step_id` should be replaced
        with whatever `content` is provided.
      * INSERT_AFTER - means that the specified `content` should be inserted after
        the specified `step_id`.
    For a given step
    """

    action: ActionType
    job: str
    step_id: str
    content: list[StepContent]


class Workflow(BaseModel):
    """
    The :class:`Workflow` is used to specify which workflow should be modified.
    This is determined by the workflow `name`. A workflow can be modified by specifying:
       * `remove_jobs` - job names in this list will be removed from the workflow.
       * `step_customization` - items in this list indicate which job's step
          should be modified.
    """

    name: str
    remove_jobs: list[str] = Field(default_factory=list)
    step_customizations: list[StepCustomization] = Field(default_factory=list)


class WorkflowPatcherConfig(BaseModel):
    """
    The :class:`WorkflowPatcherConfig` is used to validate the expected format for
    the `.workflow-patcher.yml`, which is used to modify the workflow templates provided
    by the PTB.
    """

    workflows: list[Workflow]


@dataclass(frozen=True)
class WorkflowPatcher(YamlRenderer):
    """
    The :class:`WorkflowPatcher` enables users to define a YAML file
    to customize PTB-provided workflows by removing or modifying jobs in the file.
    A job can be modified by replacing or inserting steps.
    The provided YAML file must meet the conditions of :class:`WorkflowPatcherConfig`.
    """

    @cached_property
    def content(self) -> CommentedMap:
        """
        The loaded YAML content. It loads on first access and
        stays cached even though the class is frozen.
        """
        loaded_yaml = self.get_yaml_dict()
        try:
            WorkflowPatcherConfig.model_validate(loaded_yaml)
            return loaded_yaml
        except ValidationError as exc:
            raise InvalidWorkflowPatcherYamlError(file_path=self.file_path) from exc
