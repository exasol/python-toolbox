from inspect import cleandoc

from yaml import (
    dump,
    safe_load,
)

from exasol.toolbox.util.workflows.format_yaml import GitHubDumper


class TestEmptyRepresenter:
    documentation = cleandoc(
        """
    name: Merge-Gate
    on:
      workflow_call:
    """
    )

    def test_works_as_expected(self):
        data = safe_load(cleandoc(self.documentation))
        output = dump(
            data,
            Dumper=GitHubDumper,
        )
        assert output == self.documentation + "\n"

    def test_default_behavior_differs(self):
        expected = cleandoc(
            """
        name: Merge-Gate
        on:
          workflow_call: null
        """
        )

        data = safe_load(cleandoc(self.documentation))

        output = dump(data)
        assert output == expected + "\n"


class TestStrPresenter:
    @staticmethod
    def test_line_break_works_as_expected():
        pass
