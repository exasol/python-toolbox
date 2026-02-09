from inspect import cleandoc

import pytest

from exasol.toolbox.util.workflows.process_template import TemplateRenderer
from noxconfig import PROJECT_CONFIG


@pytest.fixture
def template_renderer() -> TemplateRenderer:
    return TemplateRenderer(github_template_dict=PROJECT_CONFIG.github_template_dict)


class TestTemplateRenderer:
    @staticmethod
    def test_works_for_general_case(tmp_path, template_renderer):
        input_yaml = """
        name: Build & Publish

        on:
          workflow_call:
            secrets:
              PYPI_TOKEN:
                required: true

        jobs:
          cd-job:
            name: Continuous Delivery
            permissions:
              contents: write
        """
        file_path = tmp_path / "dummy.yml"
        content = cleandoc(input_yaml)
        file_path.write_text(content)

        result = template_renderer.render_to_workflow(file_path=file_path)
        assert result == cleandoc(input_yaml)

    @staticmethod
    def test_fixes_extra_horizontal_whitespace(tmp_path, template_renderer):
        # required has 2 extra spaces
        input_yaml = """
        name: Build & Publish

        on:
          workflow_call:
            secrets:
              PYPI_TOKEN:
                  required: true
        """

        expected_yaml = """
        name: Build & Publish

        on:
          workflow_call:
            secrets:
              PYPI_TOKEN:
                required: true
        """

        file_path = tmp_path / "dummy.yml"
        content = cleandoc(input_yaml)
        file_path.write_text(content)

        result = template_renderer.render_to_workflow(file_path=file_path)
        assert result == cleandoc(expected_yaml)

    @staticmethod
    def test_keeps_comments(tmp_path, template_renderer):
        input_yaml = """
        steps:
          # Comment in nested area
          - name: SCM Checkout # Comment inline
            uses: actions/checkout@v6
            # Comment in step
        """

        expected_yaml = """
        steps:
        # Comment in nested area
        - name: SCM Checkout # Comment inline
          uses: actions/checkout@v6
          # Comment in step
        """

        file_path = tmp_path / "dummy.yml"
        content = cleandoc(input_yaml)
        file_path.write_text(content)

        result = template_renderer.render_to_workflow(file_path=file_path)
        assert result == cleandoc(expected_yaml)

    @staticmethod
    def test_keeps_quotes_for_variables_as_is(tmp_path, template_renderer):
        input_yaml = """
        - name: Build Artifacts
          run: poetry build
        - name: PyPi Release
          env:
            POETRY_HTTP_BASIC_PYPI_USERNAME: "__token__"
            POETRY_HTTP_BASIC_PYPI_PASSWORD: "${{ secrets.PYPI_TOKEN }}"
          run: poetry publish
        - name: GitHub Release
          env:
            GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          run: >
            gh release create ${GITHUB_REF_NAME}
            --title ${GITHUB_REF_NAME}
            --notes-file ./doc/changes/changes_${GITHUB_REF_NAME}.md
            dist/*
        """

        expected_yaml = """
        - name: Build Artifacts
          run: poetry build
        - name: PyPi Release
          env:
            POETRY_HTTP_BASIC_PYPI_USERNAME: "__token__"
            POETRY_HTTP_BASIC_PYPI_PASSWORD: "${{ secrets.PYPI_TOKEN }}"
          run: poetry publish
        - name: GitHub Release
          env:
            GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          run: >-
            gh release create ${GITHUB_REF_NAME}
            --title ${GITHUB_REF_NAME}
            --notes-file ./doc/changes/changes_${GITHUB_REF_NAME}.md
            dist/*
        """

        file_path = tmp_path / "dummy.yml"
        content = cleandoc(input_yaml)
        file_path.write_text(content)

        result = template_renderer.render_to_workflow(file_path=file_path)
        assert result == cleandoc(expected_yaml)

    @staticmethod
    def test_updates_jinja_variables(tmp_path, template_renderer):
        input_yaml = """
        - name: Setup Python & Poetry Environment
          uses: exasol/python-toolbox/.github/actions/python-environment@v5
          with:
            python-version: "(( minimum_python_version ))"
            poetry-version: "(( dependency_manager_version ))"
        """
        expected_yaml = """
        - name: Setup Python & Poetry Environment
        uses: exasol/python-toolbox/.github/actions/python-environment@v5
        with:
          python-version: "3.10"
          poetry-version: "2.3.0"
        """

        file_path = tmp_path / "dummy.yml"
        content = cleandoc(input_yaml)
        file_path.write_text(content)

        result = template_renderer.render_to_workflow(file_path=file_path)
        assert result == cleandoc(expected_yaml)

    @staticmethod
    def test_preserves_list_format(tmp_path, template_renderer):
        input_yaml = """
        on:
          pull_request:
            types: [opened, synchronize, reopened]

        Type-Check:
          name: Type Checking (Python-${{ matrix.python-versions }})
          runs-on: "ubuntu-24.04"
          permissions:
            contents: read
          strategy:
            fail-fast: false
            matrix:
              python-versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
        """

        file_path = tmp_path / "dummy.yml"
        content = cleandoc(input_yaml)
        file_path.write_text(content)

        result = template_renderer.render_to_workflow(file_path=file_path)
        assert result == cleandoc(input_yaml)
