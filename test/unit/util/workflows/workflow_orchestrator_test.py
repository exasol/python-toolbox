from pathlib import Path
from unittest.mock import patch

import pytest
from pydantic import computed_field

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.util.workflows.exceptions import (
    InvalidWorkflowPatcherEntryError,
    YamlJobValueError,
)
from exasol.toolbox.util.workflows.templates import (
    DOCUMENTATION_ONLY_WORKFLOW_NAMES,
    NOT_MAINTAINED_WORKFLOW_NAMES,
    WORKFLOW_TEMPLATE_OPTIONS,
)
from exasol.toolbox.util.workflows.workflow import Workflow
from exasol.toolbox.util.workflows.workflow_orchestrator import WorkflowOrchestrator


def _remove_header(template_text: str) -> str:
    """
    Remove the Jinja header placeholder line from a workflow template.
    """
    return template_text.split("\n", 1)[1].strip()


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

    @staticmethod
    @pytest.mark.parametrize("workflow_name", DOCUMENTATION_ONLY_WORKFLOW_NAMES)
    def test_returns_ralse_for_documentation_only_workflow_when_docs_enabled(
        project_config, workflow_name
    ):

        result = WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config,
        )._skip_workflow(
            workflow_name=workflow_name,
            is_new_project=False,
        )

        assert result is False


    @staticmethod
    @pytest.mark.parametrize("workflow_name", DOCUMENTATION_ONLY_WORKFLOW_NAMES)
    def test_returns_true_for_documentation_only_workflow_when_docs_disabled(
        tmp_path, workflow_name
    ):
        class Config(BaseConfig):
            @computed_field  # type: ignore[misc]
            @property
            def has_documentation(self) -> bool:
                return False

        config = Config(root_path=tmp_path, project_name="test")

        result = WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=config,
        )._skip_workflow(
            workflow_name=workflow_name,
            is_new_project=False,
        )

        assert result is True


class TestIterWorkflows:
    @staticmethod
    def test_works_as_expected_without_patcher(project_config_without_patcher):
        workflow_name = "merge-gate"
        project_config_without_patcher.github_workflow_directory.mkdir(parents=True)
        input_text = WORKFLOW_TEMPLATE_OPTIONS[workflow_name].read_text()

        result = WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config_without_patcher,
        )._iter_workflows()

        result = list(result)
        assert len(result) == 1
        assert result[0].template_path == WORKFLOW_TEMPLATE_OPTIONS[workflow_name]
        assert result[0].output_path.name == f"{workflow_name}.yml"
        assert (
            Workflow._normalize_content(result[0].content)[:10]
            == _remove_header(input_text)[:10]
        )

    @staticmethod
    def test_works_as_expected_with_relevant_patcher(project_config, remove_job_yaml):
        workflow_name = "checks"
        project_config.github_workflow_directory.mkdir(parents=True)
        input_text = WORKFLOW_TEMPLATE_OPTIONS[workflow_name].read_text()
        removed_job_name = "build-documentation-and-check-links"
        assert removed_job_name in remove_job_yaml
        assert removed_job_name in input_text

        result = WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config,
        )._iter_workflows()

        result = list(result)
        assert len(result) == 1
        assert result[0].output_path.name == f"{workflow_name}.yml"
        assert (
            Workflow._normalize_content(result[0].content)[:10]
            == _remove_header(input_text)[:10]
        )
        assert removed_job_name not in result[0].content

    @staticmethod
    def test_works_as_expected_with_not_relevant_patcher(
        project_config, remove_job_yaml
    ):
        workflow_name = "merge-gate"
        project_config.github_workflow_directory.mkdir(parents=True)
        input_text = WORKFLOW_TEMPLATE_OPTIONS[workflow_name].read_text()

        result = WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config,
        )._iter_workflows()

        result = list(result)
        assert len(result) == 1
        assert result[0].output_path.name == f"{workflow_name}.yml"
        assert (
            Workflow._normalize_content(result[0].content)[:10]
            == _remove_header(input_text)[:10]
        )

    @staticmethod
    def test_not_maintained_workflows_added_to_new_project(
        project_config_without_patcher,
    ):
        directory = project_config_without_patcher.github_workflow_directory
        directory.mkdir(parents=True)

        result = WorkflowOrchestrator(
            workflow_choice="all",
            config=project_config_without_patcher,
        )._iter_workflows()

        assert {f"{name}.yml" for name in NOT_MAINTAINED_WORKFLOW_NAMES}.issubset(
            {workflow.output_path.name for workflow in result}
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

        result = WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config_without_patcher,
        )._iter_workflows()

        assert list(result) == []

    @staticmethod
    @pytest.mark.parametrize("workflow_name", NOT_MAINTAINED_WORKFLOW_NAMES)
    def test_not_maintained_workflows_not_added_to_old_project(
        project_config_without_patcher, workflow_name
    ):
        directory = project_config_without_patcher.github_workflow_directory
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "dummy.yml").touch()

        result = WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config_without_patcher,
        )._iter_workflows()

        assert list(result) == []

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
            for _ in WorkflowOrchestrator(
                workflow_choice="checks",
                config=project_config,
            )._iter_workflows():
                pass

        assert (
            f"In file '{project_config.github_workflow_patcher_yaml}', "
            "an entry '{'job_name': 'unknown-job'}' does not exist in"
        ) in str(ex.value)
        assert isinstance(ex.value.__cause__, YamlJobValueError)


class TestGenerateWorkflows:
    @staticmethod
    def test_writes_all_workflows_on_fresh_project(project_config_without_patcher):
        directory = project_config_without_patcher.github_workflow_directory
        directory.mkdir(parents=True)

        WorkflowOrchestrator(
            workflow_choice="all",
            config=project_config_without_patcher,
        ).generate_workflows()

        assert all(
            (directory / f"{name}.yml").exists() for name in WORKFLOW_TEMPLATE_OPTIONS
        )

    @staticmethod
    def test_does_not_write_when_all_workflows_are_up_to_date(
        project_config_without_patcher,
    ):
        directory = project_config_without_patcher.github_workflow_directory
        directory.mkdir(parents=True)

        WorkflowOrchestrator(
            workflow_choice="all",
            config=project_config_without_patcher,
        ).generate_workflows()

        with patch.object(Path, "write_text") as write_text:
            WorkflowOrchestrator(
                workflow_choice="all",
                config=project_config_without_patcher,
            ).generate_workflows()

        write_text.assert_not_called()

    @staticmethod
    def test_overwrites_existing_workflow_file(project_config_without_patcher):
        directory = project_config_without_patcher.github_workflow_directory
        directory.mkdir(parents=True)

        workflow_name = "merge-gate"
        workflow_path = directory / f"{workflow_name}.yml"
        original_content = "line 3\n"
        workflow_path.write_text(original_content)

        WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config_without_patcher,
        ).generate_workflows()
        assert workflow_path.read_text() != original_content


class TestFindDifferingWorkflows:
    @staticmethod
    def test_returns_empty_list_when_workflow_is_up_to_date(
        project_config_without_patcher, capsys
    ):
        directory = project_config_without_patcher.github_workflow_directory
        directory.mkdir(parents=True)

        workflow_name = "merge-gate"
        WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config_without_patcher,
        ).generate_workflows()
        capsys.readouterr()

        outdated_workflows = WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config_without_patcher,
        ).find_differing_workflows()

        assert outdated_workflows == []
        assert "--- existing:" not in capsys.readouterr().out

    @staticmethod
    def test_returns_workflow_name_and_prints_diff_when_workflow_differs(
        project_config_without_patcher, capsys
    ):
        directory = project_config_without_patcher.github_workflow_directory
        directory.mkdir(parents=True)

        workflow_name = "merge-gate"
        workflow_path = directory / f"{workflow_name}.yml"
        workflow_path.write_text("line 3\n")

        outdated_workflows = WorkflowOrchestrator(
            workflow_choice=workflow_name,
            config=project_config_without_patcher,
        ).find_differing_workflows()

        assert outdated_workflows == ["merge-gate"]
        assert "--- existing: merge-gate.yml" in capsys.readouterr().out
