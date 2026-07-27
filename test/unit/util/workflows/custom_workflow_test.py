from inspect import cleandoc
from pathlib import Path

import pytest

from exasol.toolbox.util.workflows.custom_workflow import merge_permissions
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

    yaml_with_permissions = cleandoc("""
    name: Build & Publish

    on:
      workflow_call:

    jobs:
      build:
        permissions:
          contents: read
          packages: read
      publish:
        permissions:
          contents: write
          id-token: write
    """)

    yaml_without_secrets = cleandoc("""
    name: Build & Publish

    on:
      workflow_call:
    """)

    yaml_with_job_without_permissions = cleandoc("""
    name: Build & Publish

    on:
      workflow_call:

    jobs:
      build:
        runs-on: ubuntu-latest
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

    def test_extract_permissions_when_present(self, test_yml):
        test_yml.write_text(self.yaml_with_permissions)

        custom_workflow = CustomWorkflow.load_from_file(file_path=test_yml)
        permissions = custom_workflow.extract_permissions()

        assert list(permissions.items()) == [
            ("contents", "write"),
            ("packages", "read"),
            ("id-token", "write"),
        ]

    def test_extract_permissions_when_no_jobs_present(self, test_yml):
        test_yml.write_text(self.yaml_without_secrets)

        custom_workflow = CustomWorkflow.load_from_file(file_path=test_yml)
        permissions = custom_workflow.extract_permissions()

        assert permissions == {}

    def test_extract_permissions_when_job_has_no_permissions(self, test_yml):
        test_yml.write_text(self.yaml_with_job_without_permissions)

        custom_workflow = CustomWorkflow.load_from_file(file_path=test_yml)
        permissions = custom_workflow.extract_permissions()

        assert permissions == {}

    def test_merge_permissions_keeps_most_permissive_level(self):
        permissions = merge_permissions(
            [
                {"contents": "read", "packages": "read"},
                {"contents": "write", "issues": "read"},
                {"packages": "read", "issues": "write"},
            ]
        )

        assert list(permissions.items()) == [
            ("contents", "write"),
            ("packages", "read"),
            ("issues", "write"),
        ]
