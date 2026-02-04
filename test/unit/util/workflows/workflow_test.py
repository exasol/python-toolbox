import pytest

from exasol.toolbox.util.workflows.workflow import Workflow
from noxconfig import PROJECT_CONFIG

BAD_TEMPLATE = """
name: Publish Documentation

on:
  workflow_call:
  workflow_dispatch:

jobs:

  build-documentation:
    runs-on: "ubuntu-24.04"
    permissions:
      contents: read
    steps:
      - name: SCM Checkout
      uses: actions/checkout@v5
"""

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
    def test_fails_when_yaml_malformed(tmp_path):
        file_path = tmp_path / "test.yaml"
        file_path.write_text(BAD_TEMPLATE)
        with pytest.raises(ValueError, match="while parsing a block collection"):
            Workflow.load_from_template(
                file_path=file_path,
                github_template_dict=PROJECT_CONFIG.github_template_dict,
            )
