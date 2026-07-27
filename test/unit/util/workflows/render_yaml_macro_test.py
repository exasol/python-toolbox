from inspect import cleandoc
from pathlib import Path
from types import SimpleNamespace

import pytest

from exasol.toolbox.util.workflows.render_yaml import YamlRenderer


@pytest.fixture
def macro_template(tmp_path: Path, macro_input: str) -> Path:
    template_path = tmp_path / "dummy.yml"
    template_path.write_text(cleandoc("""
            (% from "_workflow_macros.j2" import workflow_passed_secrets, workflow_permissions with context %)
            jobs:
              macro-job:
                uses: ./.github/workflows/dummy.yml
            {macro_input}
            """).format(macro_input=macro_input))
    return template_path


@pytest.mark.parametrize(
    "macro_input", ['(( workflow_permissions("dummy-extension") ))']
)
class TestWorkflowPermissions:
    @staticmethod
    def test_when_permissions_empty(macro_template):
        yaml_renderer = YamlRenderer(
            github_template_dict={
                "custom_workflows": {
                    "dummy-extension": SimpleNamespace(permissions={}),
                }
            },
            file_path=macro_template,
        )

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert "permissions" not in yaml_dict["jobs"]["macro-job"]

    @staticmethod
    def test_permissions_are_set(macro_template):
        yaml_renderer = YamlRenderer(
            github_template_dict={
                "custom_workflows": {
                    "dummy-extension": SimpleNamespace(
                        permissions={
                            "contents": "write",
                            "packages": "read",
                        }
                    ),
                }
            },
            file_path=macro_template,
        )

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_dict["jobs"]["macro-job"]["permissions"] == {
            "contents": "write",
            "packages": "read",
        }


@pytest.mark.parametrize(
    "macro_input", ['(( workflow_passed_secrets("dummy-extension") -))']
)
class TestWorkflowPassedSecrets:
    @staticmethod
    def test_when_secrets_empty(macro_template):
        yaml_renderer = YamlRenderer(
            github_template_dict={
                "custom_workflows": {
                    "dummy-extension": SimpleNamespace(secrets=()),
                }
            },
            file_path=macro_template,
        )

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert "secrets" not in yaml_dict["jobs"]["macro-job"]

    @staticmethod
    def test_when_secrets_are_set(macro_template):
        yaml_renderer = YamlRenderer(
            github_template_dict={
                "custom_workflows": {
                    "dummy-extension": SimpleNamespace(
                        secrets=("SECRET_A", "SECRET_B"),
                    ),
                }
            },
            file_path=macro_template,
        )

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_dict["jobs"]["macro-job"]["secrets"] == {
            "SECRET_A": "${{ secrets.SECRET_A }}",
            "SECRET_B": "${{ secrets.SECRET_B }}",
        }
