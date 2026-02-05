from pathlib import Path
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
)

from exasol.toolbox.util.workflows.template_processing import TemplateRenderer


class Workflow(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    content: str

    @classmethod
    def load_from_template(cls, file_path: Path, github_template_dict: dict[str, Any]):
        if not file_path.exists():
            raise FileNotFoundError(file_path)

        try:
            raw_content = file_path.read_text()
            template_renderer = TemplateRenderer(
                template_str=raw_content, github_template_dict=github_template_dict
            )
            workflow = template_renderer.render_to_workflow()
            return cls(content=workflow)
        except Exception as e:
            raise ValueError(f"Error rendering file: {file_path}") from e
