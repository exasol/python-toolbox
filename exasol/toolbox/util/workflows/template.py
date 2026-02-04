from dataclasses import dataclass
from inspect import cleandoc
from itertools import count
from re import (
    MULTILINE,
    sub,
)
from typing import Any

from jinja2 import Environment
from yaml import (
    dump,
    safe_load,
)

from exasol.toolbox.util.workflows.formatting import GitHubDumper

jinja_env = Environment(
    variable_start_string="((", variable_end_string="))", autoescape=True
)


@dataclass(frozen=True)
class TemplateToWorkflow:
    template_str: str
    github_template_dict: dict[str, Any]
    _comment_id: count = count(0)

    def _render_with_jinja(self, input_str: str) -> str:
        """
        Render the template with Jinja.
        """
        jinja_template = jinja_env.from_string(input_str)
        return jinja_template.render(self.github_template_dict)

    def _convert_comment_to_key_pair(self, input_str: str) -> str:
        """
        Convert a comment to a key-pair, which is parseable by PyYaml.

        Example:
            # Comment 1
            build-job:
            ....

            __com_1: "Comment 1"
            build-job:
            ....

        Case where it does not work:
          schedule:
            # At 00:00 on every 7th day-of-month from 1 through 31. (https://crontab.guru)
            - cron: "0 0 1/7 * *"

        Here the replacement comment would need to start with a - to be valid YAML.
        This is possible to do, but the code would be more complicated, as it is
        not guaranteed that the next line starts with a -.
        """

        def comment_to_key(match):
            indent = match.group(1)
            content = match.group(2)
            return f'{indent}__com_{next(self._comment_id)}: "{content}"'

        pattern = r"(^\s*)#\s*(.*)"
        return sub(pattern, comment_to_key, input_str, flags=MULTILINE)

    @staticmethod
    def _convert_key_pair_to_comment(input_str: str) -> str:
        """
        Convert a special key-pair back to a comment. This performs the reverse
        operation of :meth:`_convert_comment_to_tag`.
        """
        pattern = r"(^\s*)__com_\d+:\s*(.*)"
        return sub(pattern, r"\1# \2", input_str, flags=MULTILINE)

    def convert(self) -> str:
        """
        Convert a workflow template to a rendered workflow that works for GitHub.
        """

        workflow_string = self._render_with_jinja(self.template_str)
        workflow_string = self._convert_comment_to_key_pair(workflow_string)
        workflow_dict = safe_load(workflow_string)
        workflow_string = dump(
            workflow_dict,
            Dumper=GitHubDumper,
            width=200,  # To prevent longer lines from wrapping
            sort_keys=False,  # if True, then re-orders the jobs alphabetically
        )
        workflow_string = self._convert_key_pair_to_comment(workflow_string)
        return cleandoc(workflow_string)
