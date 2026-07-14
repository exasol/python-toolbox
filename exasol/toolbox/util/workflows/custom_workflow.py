from __future__ import annotations

from pathlib import Path
from typing import (
    Literal,
    TypeAlias,
)

from pydantic import (
    BaseModel,
    ConfigDict,
)
from ruamel.yaml import (
    CommentedMap,
)

from exasol.toolbox.util.workflows.render_yaml import parse_yaml_text

PermissionLevel: TypeAlias = Literal["none", "read", "write"]
PERMISSION_RANK: dict[PermissionLevel, int] = {"none": 0, "read": 1, "write": 2}
Permissions: TypeAlias = dict[str, PermissionLevel]


def merge_permissions(permission_maps: list[Permissions]) -> Permissions:
    """Merge permission maps to keep the greater permission."""
    merged_permissions: Permissions = {}
    for permission_map in permission_maps:
        for permission_name, requested_level in permission_map.items():
            current_level = merged_permissions.get(permission_name, "none")
            if PERMISSION_RANK[requested_level] > PERMISSION_RANK[current_level]:
                merged_permissions[permission_name] = requested_level
    return merged_permissions


class CustomWorkflow(BaseModel):
    """A project-owned workflow used for seeded workflows and extensions.

    These workflows are seeded by the PTB or extend PTB-provided workflows, but
    they are maintained by the project itself rather than the PTB. See
    `Custom Workflows <https://exasol.github.io/python-toolbox/main/user_guide/features/github_workflows/index.html#custom-workflows>`__.
    """

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

    def extract_permissions(self) -> dict[str, str]:
        """Return the effective job permissions required by the workflow.

        The extractor scans all jobs and merges their ``permissions`` blocks into a
        single mapping. When the same permission appears multiple times, the more
        permissive level wins while preserving the first-seen order of the keys.

        For example, a custom workflow can declare permissions like this:

        .. code-block:: yaml

           name: Slow-Checks

           on:
             workflow_call:

           jobs:
             run-integration-tests:
               permissions:
                 contents: read
        """
        jobs = self.yaml_content.get("jobs", {})
        permission_maps = [job.get("permissions", {}) for job in jobs.values()]
        return merge_permissions(permission_maps)
