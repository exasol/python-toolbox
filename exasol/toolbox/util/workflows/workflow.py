from pathlib import Path
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
)

from exasol.toolbox.util.workflows.process_template import WorkflowRenderer
from exasol.toolbox.util.workflows.render_yaml import (
    TemplateRenderingError,
    YamlOutputError,
    YamlParsingError,
)


class Workflow(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    content: str

    @classmethod
    def load_from_template(cls, file_path: Path, github_template_dict: dict[str, Any]):
        if not file_path.exists():
            raise FileNotFoundError(file_path)

        try:
            workflow_renderer = WorkflowRenderer(
                github_template_dict=github_template_dict,
                file_path=file_path,
            )
            workflow = workflow_renderer.render()
            return cls(content=workflow)
        except (TemplateRenderingError, YamlParsingError, YamlOutputError) as exc:
            raise exc
        except Exception as e:
            # Wrap all other "non-special" exceptions
            raise ValueError(f"Error rendering file: {file_path}") from e
