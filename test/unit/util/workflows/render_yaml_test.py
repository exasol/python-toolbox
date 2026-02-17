from inspect import cleandoc
from pathlib import Path

import pytest
from jinja2 import (
    TemplateSyntaxError,
    UndefinedError,
)
from ruamel.yaml.parser import ParserError
from ruamel.yaml.representer import RepresenterError
from toolbox.util.workflows.exceptions import (
    TemplateRenderingError,
    YamlOutputError,
    YamlParsingError,
)

from exasol.toolbox.util.workflows.render_yaml import (
    YamlRenderer,
)
from noxconfig import PROJECT_CONFIG


@pytest.fixture
def test_yml(tmp_path: Path) -> Path:
    return tmp_path / "test.yml"


@pytest.fixture
def yaml_renderer(test_yml) -> YamlRenderer:
    return YamlRenderer(
        github_template_dict=PROJECT_CONFIG.github_template_dict, file_path=test_yml
    )


class TestYamlRenderer:
    @staticmethod
    def test_works_for_general_case(test_yml, yaml_renderer):
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
        test_yml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(input_yaml)

    @staticmethod
    def test_fixes_extra_horizontal_whitespace(test_yml, yaml_renderer):
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
        test_yml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

    @staticmethod
    def test_keeps_comments(test_yml, yaml_renderer):
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
        test_yml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

    @staticmethod
    def test_keeps_quotes_for_variables_as_is(test_yml, yaml_renderer):
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
        test_yml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

    @staticmethod
    def test_updates_jinja_variables(test_yml, yaml_renderer):
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
        test_yml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

    @staticmethod
    def test_preserves_list_format(test_yml, yaml_renderer):
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
        test_yml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(input_yaml)

    @staticmethod
    def test_jinja_variable_unknown(test_yml, yaml_renderer):
        input_yaml = """
        - name: Setup Python & Poetry Environment
          uses: exasol/python-toolbox/.github/actions/python-environment@v5
          with:
            poetry-version: "(( bad_jinja ))"
        """

        content = cleandoc(input_yaml)
        test_yml.write_text(content)

        with pytest.raises(
            TemplateRenderingError, match="Check for Jinja-related errors."
        ) as exc:
            yaml_renderer.get_yaml_dict()
        assert isinstance(exc.value.__cause__, UndefinedError)
        assert "'bad_jinja' is undefined" in str(exc.value.__cause__)

    @staticmethod
    def test_jinja_variable_unclosed(test_yml, yaml_renderer):
        input_yaml = """
        - name: Setup Python & Poetry Environment
          uses: exasol/python-toolbox/.github/actions/python-environment@v5
          with:
            python-version: "(( minimum_python_version )"
        """
        content = cleandoc(input_yaml)
        test_yml.write_text(content)

        with pytest.raises(
            TemplateRenderingError, match="Check for Jinja-related errors."
        ) as exc:
            yaml_renderer.get_yaml_dict()
        assert isinstance(exc.value.__cause__, TemplateSyntaxError)
        assert "unexpected ')'" in str(exc.value.__cause__)

    @staticmethod
    def test_parsing_fails_when_yaml_malformed(test_yml, yaml_renderer):
        bad_template = """
        name: Publish Documentation

        on:
          workflow_call:
          workflow_dispatch:

        jobs:

          build-documentation:
            runs-on: "ubuntu-24.04"
            permissions:
              contents: read
            steps:
              - name: SCM Checkout
              uses: actions/checkout@v5
        """
        test_yml.write_text(cleandoc(bad_template))

        with pytest.raises(
            YamlParsingError, match="Check for invalid YAML syntax."
        ) as excinfo:
            yaml_renderer.get_yaml_dict()

        assert isinstance(excinfo.value.__cause__, ParserError)
        assert "while parsing a block collection" in str(excinfo.value.__cause__)

    @staticmethod
    def test_yaml_cannot_output_to_string(test_yml, yaml_renderer):
        input_yaml = """
        steps:
          # Comment in nested area
          - name: SCM Checkout # Comment inline
            uses: actions/checkout@v6
            # Comment in step
        """
        content = cleandoc(input_yaml)
        test_yml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        yaml_dict["steps"][0]["name"] = lambda x: x + 1

        with pytest.raises(YamlOutputError, match="could not be output") as excinfo:
            yaml_renderer.get_as_string(yaml_dict)

        assert isinstance(excinfo.value.__cause__, RepresenterError)
        assert "cannot represent an object" in str(excinfo.value.__cause__)
