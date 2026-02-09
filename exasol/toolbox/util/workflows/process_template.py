from pathlib import Path

from exasol.toolbox.util.workflows.format_yaml import YamlRenderer


class TemplateRenderer(YamlRenderer):

    def render_to_workflow(self, file_path: Path) -> str:
        """
        Render the template to the contents of a valid GitHub workflow.
        """
        workflow_dict = self.get_yaml_dict(file_path)
        return self.get_as_string(workflow_dict)
