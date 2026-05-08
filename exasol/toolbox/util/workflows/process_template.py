import copy
from dataclasses import dataclass

from ruamel.yaml import CommentedMap

from exasol.toolbox.util.workflows import logger
from exasol.toolbox.util.workflows.exceptions import (
    YamlJobValueError,
    YamlStepIdValueError,
)
from exasol.toolbox.util.workflows.patch_workflow import (
    ActionType,
    WorkflowCommentedMap,
)
from exasol.toolbox.util.workflows.render_yaml import YamlRenderer


@dataclass(frozen=True)
class WorkflowRenderer(YamlRenderer):
    """
    The :class:`WorkflowRenderer` renders a workflow template provided by the PTB into
    a final workflow. It renders the final workflow by:
      - resolving Jinja variables.
      - standardizing formatting via ruamel.yaml for a consistent output.
    """

    patch_yaml: WorkflowCommentedMap | None

    def render(self) -> str:
        """
        Render the template to the contents of a valid GitHub workflow.
        """
        workflow_dict = self.get_yaml_dict()

        if self.patch_yaml:
            logger.debug("Customize workflow with `patch_yaml`")
            workflow_modifier = WorkflowModifier(
                workflow_dict=workflow_dict, patch_yaml=self.patch_yaml
            )
            workflow_dict = workflow_modifier.get_patched_workflow()

        return self.get_as_string(workflow_dict)


@dataclass
class WorkflowModifier:
    workflow_dict: CommentedMap
    patch_yaml: WorkflowCommentedMap

    def __post_init__(self):
        # Perform deepcopy to ensure this instance owns its data
        self.workflow_dict = copy.deepcopy(self.workflow_dict)

    @property
    def jobs_dict(self) -> CommentedMap:
        return self.workflow_dict["jobs"]

    def _get_step_list(self, job_name: str) -> CommentedMap:
        self._verify_job_exists(job_name=job_name)
        return self.jobs_dict[job_name]["steps"]

    def _customize_steps(self, step_customizations: CommentedMap) -> None:
        """
        Customize the steps of jobs specified in `step_customizations` in a workflow
        (`workflow_dict`). If a `step_id` or its parent `job` cannot be found, an
        exception is raised.
        """
        for patch in step_customizations:
            job_name = patch["job"]
            patch_id = patch["step_id"]
            idx = self._get_step_index(job_name=job_name, step_id=patch_id)

            step_list = self._get_step_list(job_name=job_name)
            if patch["action"] == ActionType.REPLACE.value:
                logger.debug(
                    f"Replace YAML at step_id '{patch_id}' in job '{job_name}'"
                )
                step_list[idx : idx + 1] = patch["content"]

            elif patch["action"] == ActionType.INSERT_AFTER.value:
                logger.debug(
                    f"Insert YAML after step_id '{patch_id}' in job '{job_name}'"
                )
                step_list[idx + 1 : idx + 1] = patch["content"]

    def _get_step_index(self, job_name: str, step_id: str) -> int:
        steps = self._get_step_list(job_name=job_name)
        for index, step in enumerate(steps):
            if step["id"] == step_id:
                return index
        raise YamlStepIdValueError(step_id=step_id, job_name=job_name)

    def _remove_jobs(self, remove_jobs: CommentedMap) -> None:
        """
        Remove the jobs specified in `remove_jobs` in a workflow yaml (`workflow_dict`).
        If a `job` cannot be found, an exception is raised.
        """
        for job_name in remove_jobs:
            self._verify_job_exists(job_name)
            logger.debug(f"Remove job '{job_name}'")
            self.jobs_dict.pop(job_name)
            self._remove_job_from_needs(job_name=job_name)

    def _remove_job_from_needs(self, job_name: str) -> None:
        """
        Remove the job from the needs of subsequent jobs.
        This does NOT handle cases where the needed job is used for subsequent
        operations in another job (e.g. when it is used to define the matrix).
        """
        for other_job_name, other_job in self.jobs_dict.items():
            needs = other_job.get("needs")
            if needs is None:
                continue

            logger.debug(
                f"Remove job '{job_name}' from needs of job '{other_job_name}'"
            )
            needs_without_removed_job = [need for need in needs if need != job_name]
            if len(needs_without_removed_job) == 0:
                other_job.pop("needs")
                return
            other_job["needs"] = needs_without_removed_job

    def _verify_job_exists(self, job_name: str) -> None:
        if job_name not in self.jobs_dict:
            raise YamlJobValueError(job_name=job_name)

    def get_patched_workflow(self):
        """
        Patch the `workflow_dict`. As dictionaries are mutable structures, we directly
        take advantage of this by having it modified in this class's internal methods
        without explicit returns.
        """

        if remove_jobs := self.patch_yaml.get("remove_jobs", {}):
            self._remove_jobs(remove_jobs=remove_jobs)

        if step_customizations := self.patch_yaml.get("step_customizations", {}):
            self._customize_steps(step_customizations=step_customizations)

        return self.workflow_dict
