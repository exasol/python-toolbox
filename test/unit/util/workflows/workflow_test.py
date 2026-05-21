from inspect import cleandoc
from pathlib import Path
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
from exasol.toolbox.util.workflows.templates import (
    NOT_MAINTAINED_WORKFLOW_NAMES,
    WORKFLOW_TEMPLATE_OPTIONS,
)
from exasol.toolbox.util.workflows.workflow import (
    ALL,
    Workflow,
    _select_workflow_template,
    update_workflow,
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
            template_path=input_file_path,
            github_template_dict=project_config.github_template_dict,
        )
        output_file_path = tmp_path / f"{input_file_path.name}"
        workflow.write_to_file(file_path=output_file_path)

        assert output_file_path.read_text() == cleandoc(expected_yaml) + "\n"

    @staticmethod
    def test_compare_to_file_accepts_matching_content(tmp_path):
        content = "line 1\nline 2"
        file_path = tmp_path / "workflow.yml"
        file_path.write_text(f"\n{content}\n")

        workflow = Workflow(content=f"\n{content}\n")

        assert workflow.compare_to_file(file_path=file_path) == ""

    @staticmethod
    def test_compare_to_file_reports_diff(tmp_path):
        workflow = Workflow(content="line 1\nline 2")
        file_path = tmp_path / "workflow.yml"
        file_path.write_text("line 1\nline 3\n")

        diff = workflow.compare_to_file(file_path=file_path)

        assert diff == (
            f"--- existing: {file_path.name}\n"
            "+++ generated\n"
            "@@ -1,2 +1,2 @@\n"
            " line 1\n"
            "-line 3\n"
            "+line 2"
        )

    @staticmethod
    def test_write_to_file_skips_up_to_date_file(tmp_path):
        file_path = tmp_path / "workflow.yml"
        file_path.write_text("line 1\nline 2\n")
        workflow = Workflow(content="line 1\nline 2")

        with patch.object(Path, "write_text") as write_text:
            workflow.write_to_file(file_path=file_path)

        write_text.assert_not_called()
        assert file_path.read_text() == "line 1\nline 2\n"

    @staticmethod
    @pytest.mark.parametrize("template_path", WORKFLOW_TEMPLATE_OPTIONS.values())
    def test_works_for_all_templates(tmp_path, project_config, template_path):
        workflow = Workflow.load_from_template(
            template_path=template_path,
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
                template_path=file_path,
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
                    template_path=file_path,
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
                    template_path=file_path,
                    github_template_dict=project_config.github_template_dict,
                )


class TestSelectWorkflowTemplate:
    @staticmethod
    def test_for_all_works_as_expected():
        result = _select_workflow_template(ALL)
        assert result == WORKFLOW_TEMPLATE_OPTIONS

    @staticmethod
    @pytest.mark.parametrize("workflow_name", WORKFLOW_TEMPLATE_OPTIONS)
    def test_for_individual_workflows_works_as_expected(workflow_name):
        result = _select_workflow_template(workflow_name)
        assert result == {workflow_name: WORKFLOW_TEMPLATE_OPTIONS[workflow_name]}


class TestUpdateWorkflow:
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

        update_workflow(
            workflow_choice=workflow_name, config=project_config_without_patcher
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

        update_workflow(workflow_choice="checks", config=project_config)
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

        update_workflow(workflow_choice=workflow_name, config=project_config)
        result = expected_file_path.read_text()

        # Currently, we check only a subselection as we must preserve formatting for tbx
        # endpoints, and there are 2 minor whitespace differences.
        assert result[:10] == input_text[:10]

    @staticmethod
    def test_not_maintained_workflows_added_to_new_project(
        project_config_without_patcher,
    ):
        directory = project_config_without_patcher.github_workflow_directory
        directory.mkdir(parents=True)

        update_workflow(workflow_choice="all", config=project_config_without_patcher)

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

        update_workflow(
            workflow_choice=workflow_name, config=project_config_without_patcher
        )

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

        update_workflow(
            workflow_choice=workflow_name, config=project_config_without_patcher
        )

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

        update_workflow(
            workflow_choice=workflow_name, config=project_config_without_patcher
        )

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
            update_workflow(workflow_choice="checks", config=project_config)

        assert (
            f"In file '{project_config.github_workflow_patcher_yaml}', "
            "an entry '{'job_name': 'unknown-job'}' does not exist in"
        ) in str(ex.value)
        assert isinstance(ex.value.__cause__, YamlJobValueError)
