from unittest.mock import patch

import pytest

from exasol.toolbox.util.workflows.process_template import WorkflowRenderer
from exasol.toolbox.util.workflows.render_yaml import (
    TemplateRenderingError,
    YamlOutputError,
    YamlParsingError,
)
from exasol.toolbox.util.workflows.workflow import Workflow
from noxconfig import PROJECT_CONFIG

TEMPLATE_DIR = PROJECT_CONFIG.source_code_path / "templates" / "github" / "workflows"


class TestWorkflow:
    @staticmethod
    @pytest.mark.parametrize("template_path", list(TEMPLATE_DIR.glob("*.yml")))
    def test_works_for_all_templates(template_path):
        Workflow.load_from_template(
            file_path=template_path,
            github_template_dict=PROJECT_CONFIG.github_template_dict,
        )

    @staticmethod
    def test_fails_when_yaml_does_not_exist(tmp_path):
        file_path = tmp_path / "test.yaml"
        with pytest.raises(FileNotFoundError, match="test.yaml"):
            Workflow.load_from_template(
                file_path=file_path,
                github_template_dict=PROJECT_CONFIG.github_template_dict,
            )

    @staticmethod
    @pytest.mark.parametrize(
        "raised_exc", [TemplateRenderingError, YamlParsingError, YamlOutputError]
    )
    def test_raises_custom_exceptions(tmp_path, raised_exc):
        file_path = tmp_path / "test.yaml"
        file_path.write_text("dummy content")

        with patch.object(
            WorkflowRenderer, "render", side_effect=raised_exc(file_path=file_path)
        ):
            with pytest.raises(raised_exc):
                Workflow.load_from_template(
                    file_path=file_path,
                    github_template_dict=PROJECT_CONFIG.github_template_dict,
                )

    @staticmethod
    def test_other_exceptions_raised_as_valuerror(tmp_path):
        file_path = tmp_path / "test.yaml"
        file_path.write_text("dummy content")

        with patch.object(
            WorkflowRenderer, "render", side_effect=AttributeError("unknown source")
        ):
            with pytest.raises(ValueError):
                Workflow.load_from_template(
                    file_path=file_path,
                    github_template_dict=PROJECT_CONFIG.github_template_dict,
                )
