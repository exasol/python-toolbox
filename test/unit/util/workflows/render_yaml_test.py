from inspect import cleandoc

import pytest
from jinja2 import (
    TemplateSyntaxError,
    UndefinedError,
)

from exasol.toolbox.util.workflows.render_yaml import (
    TemplateRenderingError,
    YamlRenderer,
)
from noxconfig import PROJECT_CONFIG


@pytest.fixture
def dummy_yaml(tmp_path):
    return tmp_path / "dummy.yml"


@pytest.fixture
def yaml_renderer(dummy_yaml) -> YamlRenderer:
    return YamlRenderer(
        github_template_dict=PROJECT_CONFIG.github_template_dict, file_path=dummy_yaml
    )


class TestYamlRenderer:
    @staticmethod
    def test_works_for_general_case(dummy_yaml, yaml_renderer):
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
        dummy_yaml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(input_yaml)

    @staticmethod
    def test_fixes_extra_horizontal_whitespace(dummy_yaml, yaml_renderer):
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
        dummy_yaml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

    @staticmethod
    def test_keeps_comments(dummy_yaml, yaml_renderer):
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
        dummy_yaml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

    @staticmethod
    def test_keeps_quotes_for_variables_as_is(dummy_yaml, yaml_renderer):
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
        dummy_yaml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

    @staticmethod
    def test_updates_jinja_variables(dummy_yaml, yaml_renderer):
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
        dummy_yaml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

    @staticmethod
    def test_preserves_list_format(dummy_yaml, yaml_renderer):
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
        dummy_yaml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(input_yaml)

    @staticmethod
    def test_jinja_variable_unknown(dummy_yaml, yaml_renderer):
        input_yaml = """
        - name: Setup Python & Poetry Environment
          uses: exasol/python-toolbox/.github/actions/python-environment@v5
          with:
            poetry-version: "(( bad_jinja ))"
        """

        content = cleandoc(input_yaml)
        dummy_yaml.write_text(content)

        with pytest.raises(
            TemplateRenderingError, match="Check Jinja2-related errors."
        ) as exc:
            yaml_renderer.get_yaml_dict()
        assert isinstance(exc.value.__cause__, UndefinedError)
        assert "'bad_jinja' is undefined" in str(exc.value.__cause__)

    @staticmethod
    def test_jinja_variable_unclosed(dummy_yaml, yaml_renderer):
        input_yaml = """
        - name: Setup Python & Poetry Environment
          uses: exasol/python-toolbox/.github/actions/python-environment@v5
          with:
            python-version: "(( minimum_python_version )"
        """

        content = cleandoc(input_yaml)
        dummy_yaml.write_text(content)

        with pytest.raises(
            TemplateRenderingError, match="Check Jinja2-related errors."
        ) as exc:
            yaml_renderer.get_yaml_dict()
        assert isinstance(exc.value.__cause__, TemplateSyntaxError)
        assert "unexpected ')'" in str(exc.value.__cause__)
