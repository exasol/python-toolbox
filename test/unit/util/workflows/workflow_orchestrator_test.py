import pytest

from exasol.toolbox.util.workflows.exceptions import (
    InvalidWorkflowPatcherEntryError,
    YamlJobValueError,
)
from exasol.toolbox.util.workflows.templates import (
    NOT_MAINTAINED_WORKFLOW_NAMES,
    WORKFLOW_TEMPLATE_OPTIONS,
)
from exasol.toolbox.util.workflows.workflow_orchestrator import WorkflowOrchestrator


class TestTemplates:
    @staticmethod
    def test_all_works_as_expected(project_config):
        result = WorkflowOrchestrator(
            workflow_choice="all", config=project_config
        ).templates
        assert result == WORKFLOW_TEMPLATE_OPTIONS

    @staticmethod
    @pytest.mark.parametrize("workflow_name", WORKFLOW_TEMPLATE_OPTIONS)
    def test_individual_workflows_works_as_expected(workflow_name, project_config):
        result = WorkflowOrchestrator(
            workflow_choice=workflow_name, config=project_config
        ).templates
        assert result == {workflow_name: WORKFLOW_TEMPLATE_OPTIONS[workflow_name]}


class TestIsNewProject:
    @staticmethod
    def test_returns_true_when_no_yml_files_exist(project_config):
        project_config.github_workflow_directory.mkdir(parents=True)

        result = WorkflowOrchestrator(
            workflow_choice="all",
            config=project_config,
        )._is_new_project()

        assert result is True

    @staticmethod
    def test_returns_false_when_yml_files_exist(project_config):
        workflow_directory = project_config.github_workflow_directory
        workflow_directory.mkdir(parents=True)
        (workflow_directory / "existing.yml").touch()

        result = WorkflowOrchestrator(
            workflow_choice="all",
            config=project_config,
        )._is_new_project()

        assert result is False


class TestSkipWorkflow:
    @staticmethod
    def test_returns_true_for_not_maintained_workflow_in_existing_project(
        project_config,
    ):
        workflow_directory = project_config.github_workflow_directory
        workflow_directory.mkdir(parents=True)
        (workflow_directory / "existing.yml").touch()

        result = WorkflowOrchestrator(
            workflow_choice=NOT_MAINTAINED_WORKFLOW_NAMES[0],
            config=project_config,
        )._skip_workflow(
            workflow_name=NOT_MAINTAINED_WORKFLOW_NAMES[0],
            is_new_project=False,
        )

        assert result is True

    @staticmethod
    def test_returns_false_for_maintained_workflow(project_config):
        result = WorkflowOrchestrator(
            workflow_choice="checks",
            config=project_config,
        )._skip_workflow(workflow_name="checks", is_new_project=False)

        assert result is False


class TestWriteWorkflows:
    @staticmethod
    def test_works_as_expected_without_patcher(project_config_without_patcher):
        workflow_name = "merge-gate"
        project_config_without_patcher.github_workflow_directory.mkdir(parents=True)
        input_text = WORKFLOW_TEMPLATE_OPTIONS[workflow_name].read_text()
        expected_file_path = (
            project_config_without_patcher.github_workflow_directory
            / f"{workflow_name}.yml"
        )

        WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config_without_patcher,
        ).write_workflows()
        result = expected_file_path.read_text()

        assert result[:10] == input_text[:10]

    @staticmethod
    def test_works_as_expected_with_relevant_patcher(project_config, remove_job_yaml):
        workflow_name = "checks"
        project_config.github_workflow_directory.mkdir(parents=True)
        input_text = WORKFLOW_TEMPLATE_OPTIONS[workflow_name].read_text()
        expected_file_path = (
            project_config.github_workflow_directory / f"{workflow_name}.yml"
        )
        removed_job_name = "build-documentation-and-check-links"
        assert removed_job_name in remove_job_yaml
        assert removed_job_name in input_text

        WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config,
        ).write_workflows()
        result = expected_file_path.read_text()

        assert result[:10] == input_text[:10]
        assert removed_job_name not in result

    @staticmethod
    def test_works_as_expected_with_not_relevant_patcher(
        project_config, remove_job_yaml
    ):
        workflow_name = "merge-gate"
        project_config.github_workflow_directory.mkdir(parents=True)
        input_text = WORKFLOW_TEMPLATE_OPTIONS[workflow_name].read_text()
        expected_file_path = (
            project_config.github_workflow_directory / f"{workflow_name}.yml"
        )

        WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config,
        ).write_workflows()
        result = expected_file_path.read_text()

        assert result[:10] == input_text[:10]

    @staticmethod
    def test_not_maintained_workflows_added_to_new_project(
        project_config_without_patcher,
    ):
        directory = project_config_without_patcher.github_workflow_directory
        directory.mkdir(parents=True)

        WorkflowOrchestrator(
            workflow_choice="all",
            config=project_config_without_patcher,
        ).write_workflows()

        assert all(
            (directory / f"{name}.yml").exists()
            for name in NOT_MAINTAINED_WORKFLOW_NAMES
        )

    @staticmethod
    @pytest.mark.parametrize("workflow_name", NOT_MAINTAINED_WORKFLOW_NAMES)
    def test_not_maintained_workflows_not_modified_in_old_project(
        project_config_without_patcher, workflow_name
    ):
        directory = project_config_without_patcher.github_workflow_directory
        directory.mkdir(parents=True, exist_ok=True)
        workflow = "slow-checks.yml"
        (directory / workflow).touch()

        WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config_without_patcher,
        ).write_workflows()

        assert {file_path.name for file_path in directory.iterdir()} == {workflow}
        assert (directory / workflow).read_text() == ""

    @staticmethod
    @pytest.mark.parametrize("workflow_name", NOT_MAINTAINED_WORKFLOW_NAMES)
    def test_not_maintained_workflows_not_added_to_old_project(
        project_config_without_patcher, workflow_name
    ):
        directory = project_config_without_patcher.github_workflow_directory
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "dummy.yml").touch()

        WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config_without_patcher,
        ).write_workflows()

        assert {file_path.name for file_path in directory.iterdir()} == {"dummy.yml"}

    @staticmethod
    @pytest.mark.parametrize("workflow_name", NOT_MAINTAINED_WORKFLOW_NAMES)
    def test_not_maintained_workflows_not_modified_in_old_project(
        project_config_without_patcher, workflow_name
    ):
        directory = project_config_without_patcher.github_workflow_directory
        directory.mkdir(parents=True, exist_ok=True)
        workflow = "slow-checks.yml"
        (directory / workflow).touch()

        WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config_without_patcher,
        ).write_workflows()

        assert {file_path.name for file_path in directory.iterdir()} == {workflow}
        assert (directory / workflow).read_text() == ""

    @staticmethod
    def test_raises_invalidworkflowpatcherentryerror(project_config):
        patcher_yml = """
        workflows:
        - name: "checks"
          remove_jobs:
            - unknown-job
        """
        project_config.github_workflow_patcher_yaml.write_text(patcher_yml)

        with pytest.raises(InvalidWorkflowPatcherEntryError) as ex:
            WorkflowOrchestrator(
                workflow_choice="checks",
                config=project_config,
            ).write_workflows()

        assert (
            f"In file '{project_config.github_workflow_patcher_yaml}', "
            "an entry '{'job_name': 'unknown-job'}' does not exist in"
        ) in str(ex.value)
        assert isinstance(ex.value.__cause__, YamlJobValueError)
