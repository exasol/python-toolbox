from inspect import cleandoc
from pathlib import Path

import pytest

from exasol.toolbox.util.workflows.custom_workflow_extractor import CustomWorkflow


@pytest.fixture
def test_yml(tmp_path: Path) -> Path:
    return tmp_path / "test.yml"


class TestCustomWorkflow:
    yaml_with_secrets = cleandoc("""
    name: Build & Publish

    on:
      workflow_call:
        secrets:
          PYPI_TOKEN:
            required: true
          SONAR_TOKEN:
            required: true
    """)

    yaml_without_secrets = cleandoc("""
    name: Build & Publish

    on:
      workflow_call:
    """)

    def test_load_from_file(self, test_yml):
        test_yml.write_text(self.yaml_with_secrets)

        custom_workflow = CustomWorkflow.load_from_file(file_path=test_yml)

        assert custom_workflow.yaml_content

    def test_extract_secrets_when_present(self, test_yml):
        test_yml.write_text(self.yaml_with_secrets)

        custom_workflow = CustomWorkflow.load_from_file(file_path=test_yml)
        secrets = custom_workflow.extract_secrets()

        assert secrets == ("PYPI_TOKEN", "SONAR_TOKEN")

    def test_extract_secrets_when_no_secrets_present(self, test_yml):
        test_yml.write_text(self.yaml_without_secrets)

        custom_workflow = CustomWorkflow.load_from_file(file_path=test_yml)
        secrets = custom_workflow.extract_secrets()

        assert secrets == ()
