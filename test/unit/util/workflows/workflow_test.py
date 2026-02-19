from inspect import cleandoc
from unittest.mock import patch

import pytest

from exasol.toolbox.util.workflows.exceptions import (
    InvalidWorkflowPatcherEntryError,
    TemplateRenderingError,
    YamlJobValueError,
    YamlOutputError,
    YamlParsingError,
)
from exasol.toolbox.util.workflows.process_template import WorkflowRenderer
from exasol.toolbox.util.workflows.templates import WORKFLOW_TEMPLATE_OPTIONS
from exasol.toolbox.util.workflows.workflow import (
    ALL,
    Workflow,
    _select_workflows,
    update_selected_workflow,
)


class TestWorkflow:
    @staticmethod
    def test_works_as_expected(tmp_path, project_config):
        input_yaml = """
        # This is a useful comment.
        - name: Setup Python & Poetry Environment
          uses: exasol/python-toolbox/.github/actions/python-environment@v5
          with:
            python-version: "(( minimum_python_version ))"
            poetry-version: "(( dependency_manager_version ))"
        """
        expected_yaml = """
        # This is a useful comment.
        - name: Setup Python & Poetry Environment
          uses: exasol/python-toolbox/.github/actions/python-environment@v5
          with:
            python-version: "3.10"
            poetry-version: "2.3.0"
        """
        input_file_path = tmp_path / "test.yml"
        content = cleandoc(input_yaml)
        input_file_path.write_text(content)

        workflow = Workflow.load_from_template(
            file_path=input_file_path,
            github_template_dict=project_config.github_template_dict,
        )
        output_file_path = tmp_path / f"{input_file_path.name}"
        workflow.write_to_file(file_path=output_file_path)

        assert output_file_path.read_text() == cleandoc(expected_yaml) + "\n"

    @staticmethod
    @pytest.mark.parametrize("template_path", WORKFLOW_TEMPLATE_OPTIONS.values())
    def test_works_for_all_templates(tmp_path, project_config, template_path):
        workflow = Workflow.load_from_template(
            file_path=template_path,
            github_template_dict=project_config.github_template_dict,
        )
        file_path = tmp_path / f"{template_path.name}"
        workflow.write_to_file(file_path=file_path)

        assert file_path.read_text() != ""

    @staticmethod
    def test_fails_when_yaml_does_not_exist(tmp_path, project_config):
        file_path = tmp_path / "test.yaml"
        with pytest.raises(FileNotFoundError, match="test.yaml"):
            Workflow.load_from_template(
                file_path=file_path,
                github_template_dict=project_config.github_template_dict,
            )

    @staticmethod
    @pytest.mark.parametrize(
        "raised_exc", [TemplateRenderingError, YamlParsingError, YamlOutputError]
    )
    def test_raises_custom_exceptions(tmp_path, project_config, raised_exc):
        file_path = tmp_path / "test.yaml"
        file_path.write_text("dummy content")

        with patch.object(
            WorkflowRenderer, "render", side_effect=raised_exc(file_path=file_path)
        ):
            with pytest.raises(raised_exc):
                Workflow.load_from_template(
                    file_path=file_path,
                    github_template_dict=project_config.github_template_dict,
                )

    @staticmethod
    def test_other_exceptions_raised_as_valuerror(tmp_path, project_config):
        file_path = tmp_path / "test.yaml"
        file_path.write_text("dummy content")

        with patch.object(
            WorkflowRenderer, "render", side_effect=AttributeError("unknown source")
        ):
            with pytest.raises(ValueError):
                Workflow.load_from_template(
                    file_path=file_path,
                    github_template_dict=project_config.github_template_dict,
                )


class TestSelectWorkflow:
    @staticmethod
    def test_for_all_works_as_expected():
        result = _select_workflows(ALL)
        assert result == WORKFLOW_TEMPLATE_OPTIONS

    @staticmethod
    @pytest.mark.parametrize("workflow_name", WORKFLOW_TEMPLATE_OPTIONS)
    def test_for_individual_workflows_works_as_expected(workflow_name):
        result = _select_workflows(workflow_name)
        assert result == {workflow_name: WORKFLOW_TEMPLATE_OPTIONS[workflow_name]}


class TestUpdateSelectedWorkflow:
    @staticmethod
    def test_works_as_expected_without_patcher(project_config_without_patcher):
        workflow_name = "merge-gate"
        # setup
        project_config_without_patcher.github_workflow_directory.mkdir(parents=True)
        input_text = WORKFLOW_TEMPLATE_OPTIONS[workflow_name].read_text()
        expected_file_path = (
            project_config_without_patcher.github_workflow_directory
            / f"{workflow_name}.yml"
        )

        update_selected_workflow(
            workflow_name=workflow_name, config=project_config_without_patcher
        )
        result = expected_file_path.read_text()

        # Currently, we check only a subselection as we must preserve formatting for tbx
        # endpoints, and there are 2 minor whitespace differences.
        assert result[:10] == input_text[:10]

    @staticmethod
    def test_works_as_expected_with_relevant_patcher(project_config, remove_job_yaml):
        # remove_job_yaml modifies "checks" and that's also the workflow being updated
        workflow_name = "checks"
        # setup
        project_config.github_workflow_directory.mkdir(parents=True)
        input_text = WORKFLOW_TEMPLATE_OPTIONS[workflow_name].read_text()
        expected_file_path = (
            project_config.github_workflow_directory / f"{workflow_name}.yml"
        )
        # setup checks
        removed_job_name = "build-documentation-and-check-links"
        assert removed_job_name in remove_job_yaml
        assert removed_job_name in input_text

        update_selected_workflow(workflow_name="checks", config=project_config)
        result = expected_file_path.read_text()

        # We compare only a subselection to verify that the files are roughly the
        # same, and we expect them to differ as the 'result' does not contain
        # the 'removed_job_name'
        assert result[:10] == input_text[:10]
        assert removed_job_name not in result

    @staticmethod
    def test_works_as_expected_with_not_relevant_patcher(
        project_config, remove_job_yaml
    ):
        # remove_job_yaml modifies "checks" and that's NOT the workflow being updated
        workflow_name = "merge-gate"
        # setup
        project_config.github_workflow_directory.mkdir(parents=True)
        input_text = WORKFLOW_TEMPLATE_OPTIONS[workflow_name].read_text()
        expected_file_path = (
            project_config.github_workflow_directory / f"{workflow_name}.yml"
        )

        update_selected_workflow(workflow_name=workflow_name, config=project_config)
        result = expected_file_path.read_text()

        # Currently, we check only a subselection as we must preserve formatting for tbx
        # endpoints, and there are 2 minor whitespace differences.
        assert result[:10] == input_text[:10]

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
            update_selected_workflow(workflow_name="checks", config=project_config)

        assert (
            f"In file '{project_config.github_workflow_patcher_yaml}', "
            "an entry '{'job_name': 'unknown-job'}' does not exist in"
        ) in str(ex.value)
        assert isinstance(ex.value.__cause__, YamlJobValueError)
