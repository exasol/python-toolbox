from pathlib import Path

from exasol.toolbox.util.workflows.render_yaml import YamlRenderer


class WorkflowRenderer(YamlRenderer):
    """
    The :class:`WorkflowRenderer` renders a workflow template provided by the PTB into
    a final workflow. It renders the final workflow template by:
      - resolving Jinja variables.
      - standardizing formatting via ruamel.yaml for a consistent output.
    """

    def render_to_workflow(self, file_path: Path) -> str:
        """
        Render the template to the contents of a valid GitHub workflow.
        """
        workflow_dict = self.get_yaml_dict(file_path)
        return self.get_as_string(workflow_dict)
