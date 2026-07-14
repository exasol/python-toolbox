from inspect import cleandoc
from pathlib import Path
from types import SimpleNamespace

import pytest

from exasol.toolbox.util.workflows.render_yaml import YamlRenderer


@pytest.fixture
def macro_template(tmp_path: Path) -> Path:
    template_path = tmp_path / "dummy.yml"
    template_path.write_text(cleandoc("""
            (% from "_workflow_macros.j2" import workflow_permissions with context %)
            jobs:
              macro-job:
                uses: ./.github/workflows/dummy.yml
                (( workflow_permissions("dummy-extension") ))
            """))
    return template_path


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
