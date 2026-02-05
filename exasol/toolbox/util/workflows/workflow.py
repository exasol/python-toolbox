from pathlib import Path
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
)

from exasol.toolbox.util.workflows.template import TemplateToWorkflow


class Workflow(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    content: str

    @classmethod
    def load_from_template(cls, file_path: Path, github_template_dict: dict[str, Any]):
        if not file_path.exists():
            raise FileNotFoundError(file_path)

        try:
            raw_content = file_path.read_text()
            template_to_workflow = TemplateToWorkflow(
                template_str=raw_content, github_template_dict=github_template_dict
            )
            workflow = template_to_workflow.convert()
            return cls(content=workflow)
        except Exception as e:
            raise ValueError(f"Error rendering file: {file_path}") from e
