from inspect import cleandoc

from yaml import (
    dump,
    safe_load,
)

from exasol.toolbox.util.workflows.formatting import GitHubDumper


class TestEmptyRepresenter:
    documentation = """
    name: Merge-Gate
    on:
      workflow_call:
    """

    def test_works_as_expected(self):
        data = safe_load(cleandoc(self.documentation))
        output = dump(
            data,
            Dumper=GitHubDumper,
        )
        assert output == cleandoc(self.documentation) + "\n"

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
    doc_with_line_break = """
    steps:
    - name: Generate GitHub Summary
      run: |
        echo -e "# Summary" >> $GITHUB_STEP_SUMMARY
        poetry run -- nox -s project:report -- --format markdown >> $GITHUB_STEP_SUMMARY
    """
    doc_with_version = """
    steps:
    - name: Setup Python & Poetry Environment
      uses: exasol/python-toolbox/.github/actions/python-environment@v5
      with:
        python-version: "3.10"
        poetry-version: "2.3.0"
    """
    doc_with_github_secrets = """
    steps:
    - name: PyPi Release
      env:
        POETRY_HTTP_BASIC_PYPI_USERNAME: "__token__"
        POETRY_HTTP_BASIC_PYPI_PASSWORD: "${{ secrets.PYPI_TOKEN }}"
      run: poetry publish
    """

    def test_line_break_works_as_expected(self):
        data = safe_load(cleandoc(self.doc_with_line_break))
        output = dump(
            data,
            Dumper=GitHubDumper,
        )
        assert output == cleandoc(self.doc_with_line_break) + "\n"

    def test_line_break_with_default_differs(self):
        data = safe_load(cleandoc(self.doc_with_line_break))
        output = dump(data)
        assert output == (
            "steps:\n"
            "- name: Generate GitHub Summary\n"
            '  run: \'echo -e "# Summary" >> $GITHUB_STEP_SUMMARY\n'
            "\n"
            "    poetry run -- nox -s project:report -- --format markdown >> "
            "$GITHUB_STEP_SUMMARY'\n"
        )

    def test_quote_regex_works_as_expected(self):
        data = safe_load(cleandoc(self.doc_with_version))
        output = dump(
            data,
            Dumper=GitHubDumper,
            sort_keys=False,  # if True, then re-orders the jobs alphabetically
        )
        assert output == cleandoc(self.doc_with_version) + "\n"

    def test_quote_regex_with_default_differs(self):
        data = safe_load(cleandoc(self.doc_with_version))
        output = dump(
            data,
            sort_keys=False,  # if True, then re-orders the jobs alphabetically
        )
        assert output == (
            "steps:\n"
            "- name: Setup Python & Poetry Environment\n"
            "  uses: exasol/python-toolbox/.github/actions/python-environment@v5\n"
            "  with:\n"
            "    python-version: '3.10'\n"
            "    poetry-version: 2.3.0\n"
        )

    def test_quote_github_secrets_works_as_expected(self):
        data = safe_load(cleandoc(self.doc_with_github_secrets))
        output = dump(
            data,
            Dumper=GitHubDumper,
            sort_keys=False,  # if True, then re-orders the jobs alphabetically
        )
        assert output == cleandoc(self.doc_with_github_secrets) + "\n"

    def test_quote_github_secrets_with_default_differs(self):
        data = safe_load(cleandoc(self.doc_with_github_secrets))
        output = dump(
            data,
            sort_keys=False,  # if True, then re-orders the jobs alphabetically
        )
        assert output == (
            "steps:\n"
            "- name: PyPi Release\n"
            "  env:\n"
            "    POETRY_HTTP_BASIC_PYPI_USERNAME: __token__\n"
            "    POETRY_HTTP_BASIC_PYPI_PASSWORD: ${{ secrets.PYPI_TOKEN }}\n"
            "  run: poetry publish\n"
        )
