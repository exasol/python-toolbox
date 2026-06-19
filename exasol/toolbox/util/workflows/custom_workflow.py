from __future__ import annotations

from pathlib import Path

from pydantic import (
    BaseModel,
    ConfigDict,
)
from ruamel.yaml import (
    CommentedMap,
)

from exasol.toolbox.util.workflows.render_yaml import parse_yaml_text


class CustomWorkflow(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    file_path: Path
    yaml_content: CommentedMap

    @classmethod
    def load_from_file(cls, file_path: Path) -> CustomWorkflow:
        workflow_string = file_path.read_text()
        yaml = parse_yaml_text(origin_path=file_path, workflow_string=workflow_string)
        return cls(file_path=file_path, yaml_content=yaml)

    def extract_secrets(self) -> tuple[str, ...]:
        """Return the secret names declared for ``workflow_call``.

        The reusable workflow must declare them near the top level of the file
        like this:

        .. code-block:: yaml

           on:
             workflow_call:
               secrets:
                 PYPI_TOKEN:
                   required: true
                 SONAR_TOKEN:
                   required: true
        """
        workflow_call = self.yaml_content.get("on", {}).get("workflow_call")
        if isinstance(workflow_call, dict):
            if secrets := workflow_call.get("secrets", {}):
                return tuple(secrets.keys())
        return ()
