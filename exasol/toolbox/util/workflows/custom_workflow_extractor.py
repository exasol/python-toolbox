from __future__ import annotations

from pathlib import Path

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)

from exasol.toolbox.util.workflows.custom_workflow import (
    CustomWorkflow,
    Permissions,
    merge_permissions,
)

MINIMUM_GITHUB_PERMISSIONS: Permissions = {"contents": "read"}


class CustomWorkflowEntry(BaseModel):
    model_config = ConfigDict(frozen=True)

    exists: bool
    secrets: tuple[str, ...]
    permissions: Permissions

    @field_validator("secrets", mode="before")
    @classmethod
    def _normalize_secrets(cls, secrets: tuple[str, ...]) -> list[str]:
        """Return unique secret names in alphabetical order."""
        return sorted(set(secrets))

    @field_validator("permissions", mode="before")
    @classmethod
    def _normalize_permissions(cls, permissions: list[Permissions]) -> Permissions:
        """Merge permission maps while preserving first-seen order."""
        return merge_permissions(permissions)


class CustomWorkflowExtractor(BaseModel):
    model_config = ConfigDict(frozen=True)

    github_workflow_directory: Path
    sonar_token_name: str
    custom_workflows: tuple[str, ...] = (
        "cd-extension",
        "fast-tests-extension",
        "merge-gate-extension",
        "slow-checks",
    )

    def _build_custom_workflow_entry(
        self,
        workflow: str,
    ) -> CustomWorkflowEntry:
        file_path = self.github_workflow_directory / f"{workflow}.yml"

        secrets: tuple[str, ...] = ()
        permissions: list[Permissions] = []
        if file_path.is_file():
            custom_workflow = CustomWorkflow.load_from_file(file_path=file_path)
            secrets = custom_workflow.extract_secrets()
            permissions = [
                MINIMUM_GITHUB_PERMISSIONS,
                custom_workflow.extract_permissions(),
            ]
        return CustomWorkflowEntry(
            exists=file_path.exists(),
            secrets=secrets,
            permissions=permissions,
        )

    def _build_merge_gate_entry(
        self, custom_workflows_dict: dict[str, CustomWorkflowEntry]
    ) -> CustomWorkflowEntry:
        return CustomWorkflowEntry(
            exists=True,
            secrets=custom_workflows_dict["merge-gate-extension"].secrets
            + custom_workflows_dict["slow-checks"].secrets
            # from the `report.yml`
            + (self.sonar_token_name,),
            permissions=[
                MINIMUM_GITHUB_PERMISSIONS,
                custom_workflows_dict["merge-gate-extension"].permissions,
                custom_workflows_dict["slow-checks"].permissions,
            ],
        )

    def build_custom_workflow_dict(
        self,
    ) -> dict[str, CustomWorkflowEntry]:
        """
        Build the template metadata used to specify whether a custom workflow is
        present and which secrets its caller must pass through.

        The secret names are extracted from the reusable workflow itself via
        :meth:`CustomWorkflow.extract_secrets`.
        """

        custom_workflows_dict = {}
        for workflow in self.custom_workflows:
            custom_workflows_dict[workflow] = self._build_custom_workflow_entry(
                workflow=workflow,
            )

        custom_workflows_dict["merge-gate"] = self._build_merge_gate_entry(
            custom_workflows_dict
        )
        return custom_workflows_dict
