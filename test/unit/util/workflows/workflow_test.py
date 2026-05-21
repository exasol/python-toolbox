from inspect import cleandoc
from pathlib import Path
from unittest.mock import patch

import pytest

from exasol.toolbox.util.workflows.exceptions import (
    TemplateRenderingError,
    YamlOutputError,
    YamlParsingError,
)
from exasol.toolbox.util.workflows.process_template import WorkflowRenderer
from exasol.toolbox.util.workflows.templates import (
    WORKFLOW_TEMPLATE_OPTIONS,
)
from exasol.toolbox.util.workflows.workflow import Workflow


@pytest.fixture
def workflow_template_path(tmp_path):
    template_directory = tmp_path / "templates"
    template_directory.mkdir()
    template_path = template_directory / "workflow.yml"

    content = """
    jobs:
    check-release-tag:
      name: Check Release Tag
      uses: ./.github/workflows/check-release-tag.yml
      permissions:
        contents: read
    """

    template_path.write_text(cleandoc(content))
    return template_path


@pytest.fixture
def workflow_output_directory(tmp_path):
    output_directory = tmp_path / "output"
    output_directory.mkdir()
    return output_directory


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
            output_directory=tmp_path,
            github_template_dict=project_config.github_template_dict,
        )
        output_file_path = tmp_path / f"{input_file_path.name}"
        assert workflow.template_path == input_file_path
        assert workflow.output_path == output_file_path
        workflow.write_to_file()

        assert output_file_path.read_text() == cleandoc(expected_yaml) + "\n"

    @staticmethod
    def test_compare_to_file_has_identical_content(
        project_config, workflow_template_path, workflow_output_directory
    ):
        content = workflow_template_path.read_text()
        output_path = workflow_output_directory / workflow_template_path.name
        output_path.write_text(content)

        workflow = Workflow.load_from_template(
            template_path=workflow_template_path,
            output_directory=workflow_output_directory,
            github_template_dict=project_config.github_template_dict,
        )

        assert workflow.compare_to_file() == ""

    @staticmethod
    def test_compare_to_file_lacks_existing_content(
        project_config, workflow_template_path, workflow_output_directory
    ):
        workflow = Workflow.load_from_template(
            template_path=workflow_template_path,
            output_directory=workflow_output_directory,
            github_template_dict=project_config.github_template_dict,
        )

        assert workflow.compare_to_file() == (
            f"--- existing: {workflow.output_path.name}\n"
            "+++ generated\n"
            "@@ -0,0 +1,6 @@\n"
            "+jobs:\n"
            "+check-release-tag:\n"
            "+  name: Check Release Tag\n"
            "+  uses: ./.github/workflows/check-release-tag.yml\n"
            "+  permissions:\n"
            "+    contents: read"
        )

    @staticmethod
    def test_compare_to_file_reports_diff(
        project_config, workflow_template_path, workflow_output_directory
    ):
        output_path = workflow_output_directory / workflow_template_path.name
        output_path.write_text("line 3\n")

        workflow = Workflow.load_from_template(
            template_path=workflow_template_path,
            output_directory=workflow_output_directory,
            github_template_dict=project_config.github_template_dict,
        )

        assert workflow.compare_to_file() == (
            f"--- existing: {workflow.output_path.name}\n"
            "+++ generated\n"
            "@@ -1 +1,6 @@\n"
            "-line 3\n"
            "+jobs:\n"
            "+check-release-tag:\n"
            "+  name: Check Release Tag\n"
            "+  uses: ./.github/workflows/check-release-tag.yml\n"
            "+  permissions:\n"
            "+    contents: read"
        )

    @staticmethod
    def test_write_to_file_skips_up_to_date_file(
        project_config, workflow_template_path, workflow_output_directory
    ):
        content = workflow_template_path.read_text()
        output_path = workflow_output_directory / workflow_template_path.name
        output_path.write_text(content)

        workflow = Workflow.load_from_template(
            template_path=workflow_template_path,
            output_directory=workflow_output_directory,
            github_template_dict=project_config.github_template_dict,
        )

        with patch.object(Path, "write_text") as write_text:
            workflow.write_to_file()

        write_text.assert_not_called()

    @staticmethod
    @pytest.mark.parametrize("template_path", WORKFLOW_TEMPLATE_OPTIONS.values())
    def test_write_to_file_works_for_all_templates(
        tmp_path, project_config, template_path
    ):
        workflow = Workflow.load_from_template(
            template_path=template_path,
            output_directory=tmp_path,
            github_template_dict=project_config.github_template_dict,
        )
        file_path = tmp_path / f"{template_path.name}"
        workflow.write_to_file()

        assert file_path.read_text() != ""

    @staticmethod
    def test_load_from_template_fails_when_yaml_does_not_exist(
        tmp_path, project_config
    ):
        file_path = tmp_path / "test.yaml"
        with pytest.raises(FileNotFoundError, match="test.yaml"):
            Workflow.load_from_template(
                template_path=file_path,
                output_directory=tmp_path,
                github_template_dict=project_config.github_template_dict,
            )

    @staticmethod
    @pytest.mark.parametrize(
        "raised_exc", [TemplateRenderingError, YamlParsingError, YamlOutputError]
    )
    def test_load_from_template_raises_custom_exceptions(
        tmp_path, project_config, raised_exc
    ):
        file_path = tmp_path / "test.yaml"
        file_path.write_text("dummy content")

        with patch.object(
            WorkflowRenderer, "render", side_effect=raised_exc(file_path=file_path)
        ):
            with pytest.raises(raised_exc):
                Workflow.load_from_template(
                    template_path=file_path,
                    output_directory=tmp_path,
                    github_template_dict=project_config.github_template_dict,
                )

    @staticmethod
    def test_load_from_template_reraises_other_exceptions_raised_as_valuerror(
        tmp_path, project_config
    ):
        file_path = tmp_path / "test.yaml"
        file_path.write_text("dummy content")

        with patch.object(
            WorkflowRenderer, "render", side_effect=AttributeError("unknown source")
        ):
            with pytest.raises(ValueError):
                Workflow.load_from_template(
                    template_path=file_path,
                    output_directory=tmp_path,
                    github_template_dict=project_config.github_template_dict,
                )
