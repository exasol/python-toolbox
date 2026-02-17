from inspect import cleandoc
from pathlib import Path

import pytest

from exasol.toolbox.util.workflows.render_yaml import YamlRenderer
from noxconfig import PROJECT_CONFIG


@pytest.fixture
def file_path(tmp_path: Path) -> Path:
    return tmp_path / "test.yml"


@pytest.fixture
def yaml_renderer(file_path) -> YamlRenderer:
    return YamlRenderer(
        github_template_dict=PROJECT_CONFIG.github_template_dict, file_path=file_path
    )


class TestTemplateRenderer:
    @staticmethod
    def test_works_for_general_case(file_path, yaml_renderer):
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
        content = cleandoc(input_yaml)
        file_path.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(input_yaml)

    @staticmethod
    def test_fixes_extra_horizontal_whitespace(file_path, yaml_renderer):
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

        content = cleandoc(input_yaml)
        file_path.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

    @staticmethod
    def test_keeps_comments(file_path, yaml_renderer):
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

        content = cleandoc(input_yaml)
        file_path.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

    @staticmethod
    def test_keeps_quotes_for_variables_as_is(file_path, yaml_renderer):
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

        content = cleandoc(input_yaml)
        file_path.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

    @staticmethod
    def test_updates_jinja_variables(file_path, yaml_renderer):
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

        content = cleandoc(input_yaml)
        file_path.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

    @staticmethod
    def test_preserves_list_format(file_path, yaml_renderer):
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

        content = cleandoc(input_yaml)
        file_path.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(input_yaml)
