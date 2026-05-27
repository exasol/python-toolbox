import difflib
import re
from pathlib import Path
from typing import (
    Any,
)

from pydantic import (
    BaseModel,
    ConfigDict,
)
from structlog.contextvars import (
    bound_contextvars,
)

from exasol.toolbox.config import WORKFLOW_HEADER_PATTERN
from exasol.toolbox.util.workflows import logger
from exasol.toolbox.util.workflows.exceptions import (
    YamlError,
    YamlKeyError,
)
from exasol.toolbox.util.workflows.patch_workflow import (
    WorkflowCommentedMap,
)
from exasol.toolbox.util.workflows.process_template import WorkflowRenderer


class Workflow(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    template_path: Path
    output_path: Path
    content: str

    @staticmethod
    def _normalize_content(content: str, strip_header: bool = True) -> str:
        """
        Normalize workflow content for comparison.
        """
        normalized_content = content.strip()
        if strip_header:
            normalized_content = re.sub(
                pattern=WORKFLOW_HEADER_PATTERN,
                repl="",
                string=normalized_content,
            ).strip()
        return normalized_content

    @classmethod
    def load_from_template(
        cls,
        template_path: Path,
        output_directory: Path,
        github_template_dict: dict[str, Any],
        patch_yaml: WorkflowCommentedMap | None = None,
    ):
        with bound_contextvars(template_file_name=template_path.name):
            logger.debug("Load workflow template: %s", template_path.name)

            if not template_path.exists():
                raise FileNotFoundError(template_path)

            try:
                workflow_renderer = WorkflowRenderer(
                    github_template_dict=github_template_dict,
                    file_path=template_path,
                    patch_yaml=patch_yaml,
                )
                return cls(
                    template_path=template_path,
                    output_path=output_directory / template_path.name,
                    content=workflow_renderer.render(),
                )
            except (YamlError, YamlKeyError) as ex:
                raise ex
            except Exception as ex:
                # Wrap all other "non-special" exceptions
                raise ValueError(f"Error rendering file: {template_path}") from ex

    def compare_to_file(self, strip_header: bool = True) -> str:
        existing_content = ""
        if self.output_path.is_file():
            existing_content = self.output_path.read_text()

        existing_content = self._normalize_content(
            existing_content, strip_header=strip_header
        )
        generated_content = self._normalize_content(
            self.content, strip_header=strip_header
        )

        diff = difflib.unified_diff(
            existing_content.splitlines(),
            generated_content.splitlines(),
            fromfile=f"existing: {self.output_path.name}",
            tofile="generated",
            lineterm="",
        )
        return "\n".join(diff)

    def write_to_file(self) -> None:
        if self.compare_to_file(strip_header=False) == "":
            logger.debug("Skip up-to-date workflow file %s", self.output_path.name)
            return
        logger.info("Write workflow file %s", self.output_path.name)
        self.output_path.write_text(self.content + "\n")
