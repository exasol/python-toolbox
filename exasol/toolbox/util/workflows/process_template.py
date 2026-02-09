from pathlib import Path

from exasol.toolbox.util.workflows.render_yaml import YamlRenderer


class TemplateRenderer(YamlRenderer):
    """
    The :class:`TemplateRenderer` is used to process the
    `PTB-provided GitHub workflow templates <https://exasol.github.io/python-toolbox/main/user_guide/features/github_workflows/index.html>__`
     by:
      - resolving Jinja variables.
      - standardising formatting via ruamel.yaml for consistent output.
    """

    def render_to_workflow(self, file_path: Path) -> str:
        """
        Render the template to the contents of a valid GitHub workflow.
        """
        workflow_dict = self.get_yaml_dict(file_path)
        return self.get_as_string(workflow_dict)
