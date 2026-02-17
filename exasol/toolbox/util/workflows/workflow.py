from pathlib import Path
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
)
from structlog.contextvars import (
    bind_contextvars,
    clear_contextvars,
)

from exasol.toolbox.util.workflows import logger
from exasol.toolbox.util.workflows.exceptions import YamlError
from exasol.toolbox.util.workflows.process_template import WorkflowRenderer


class Workflow(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    content: str

    @classmethod
    def load_from_template(cls, file_path: Path, github_template_dict: dict[str, Any]):
        bind_contextvars(template_file_name=file_path.name)
        logger.info("Load workflow from template")

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        try:
            workflow_renderer = WorkflowRenderer(
                github_template_dict=github_template_dict,
                file_path=file_path,
            )
            workflow = workflow_renderer.render()
            return cls(content=workflow)
        except YamlError as ex:
            raise ex
        except Exception as ex:
            # Wrap all other "non-special" exceptions
            raise ValueError(f"Error rendering file: {file_path}") from ex
        finally:
            clear_contextvars()
