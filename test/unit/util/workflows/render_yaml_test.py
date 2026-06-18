from inspect import cleandoc
from pathlib import Path

import pytest
from jinja2 import (
    TemplateSyntaxError,
    UndefinedError,
)
from ruamel.yaml.parser import ParserError
from ruamel.yaml.representer import RepresenterError

from exasol.toolbox.util.workflows.exceptions import (
    TemplateRenderingError,
    YamlOutputError,
    YamlParsingError,
)
from exasol.toolbox.util.workflows.render_yaml import (
    YamlRenderer,
)


@pytest.fixture
def test_yml(tmp_path: Path) -> Path:
    return tmp_path / "test.yml"


@pytest.fixture
def yaml_renderer(test_yml, project_config) -> YamlRenderer:
    return YamlRenderer(
        github_template_dict=project_config.github_template_dict, file_path=test_yml
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
        ) as ex:
            yaml_renderer.get_yaml_dict()

        assert isinstance(ex.value.__cause__, ParserError)
        assert "while parsing a block collection" in str(ex.value.__cause__)

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

        with pytest.raises(YamlOutputError, match="could not be output") as ex:
            yaml_renderer.get_as_string(yaml_dict)

        assert isinstance(ex.value.__cause__, RepresenterError)
        assert "cannot represent an object" in str(ex.value.__cause__)


class TestYamlRendererJinja:
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
    def test_omits_block_when_extension_is_missing(
        test_yml, yaml_renderer, project_config
    ):
        input_yaml = """
        jobs:
          run-unit-tests:
            name: Unit Tests (Python-${{ matrix.python-versions }})
            runs-on: "(( os_version ))"
            permissions:
              contents: read
            strategy:
              fail-fast: false
              matrix:
                python-versions: (( python_versions | tojson ))

            steps:
              - name: Check out Repository
                id: check-out-repository
                uses: actions/checkout@v6

        (% if workflow_extension.fast_tests %)
          fast-tests-extension:
            uses: ./.github/workflows/fast-tests-extension.yml
            permissions:
              contents: read
          (% endif %)

        """
        expected_yaml = """
        jobs:
        run-unit-tests:
          name: Unit Tests (Python-${{ matrix.python-versions }})
          runs-on: "ubuntu-24.04"
          permissions:
            contents: read
          strategy:
            fail-fast: false
            matrix:
              python-versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]

          steps:
            - name: Check out Repository
              id: check-out-repository
              uses: actions/checkout@v6

        """

        content = cleandoc(input_yaml)
        test_yml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

    @staticmethod
    def test_includes_if_block_when_extension_is_present(test_yml, project_config):
        input_yaml = """
        jobs:
          run-unit-tests:
            name: Unit Tests (Python-${{ matrix.python-versions }})
            runs-on: "(( os_version ))"
            permissions:
              contents: read
            strategy:
              fail-fast: false
              matrix:
                python-versions: (( python_versions | tojson ))

            steps:
              - name: Check out Repository
                id: check-out-repository
                uses: actions/checkout@v6

        (% if workflow_extension.fast_tests %)
          fast-tests-extension:
            uses: ./.github/workflows/fast-tests-extension.yml
            permissions:
              contents: read
          (% endif %)

        """
        expected_yaml = """
        jobs:
        run-unit-tests:
          name: Unit Tests (Python-${{ matrix.python-versions }})
          runs-on: "ubuntu-24.04"
          permissions:
            contents: read
          strategy:
            fail-fast: false
            matrix:
              python-versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]

          steps:
            - name: Check out Repository
              id: check-out-repository
              uses: actions/checkout@v6

        fast-tests-extension:
          uses: ./.github/workflows/fast-tests-extension.yml
          permissions:
            contents: read

        """
        workflow_directory = project_config.github_workflow_directory
        workflow_directory.mkdir(parents=True)
        (workflow_directory / "fast-tests-extension.yml").touch()

        content = cleandoc(input_yaml)
        test_yml.write_text(content)
        yaml_renderer = YamlRenderer(
            github_template_dict=project_config.github_template_dict,
            file_path=test_yml,
        )

        yaml_dict = yaml_renderer.get_yaml_dict()

        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

    @staticmethod
    def test_includes_extension_with_multiple_secrets(test_yml, project_config):
        input_yaml = """
        jobs:
          run-unit-tests:
            name: Unit Tests (Python-${{ matrix.python-versions }})
            runs-on: "(( os_version ))"
            permissions:
              contents: read
            strategy:
              fail-fast: false
              matrix:
                python-versions: (( python_versions | tojson ))

            steps:
              - name: Check out Repository
                id: check-out-repository
                uses: actions/checkout@v6

        (% if workflow_extension.merge_gate %)
          merge-gate-extension:
            uses: ./.github/workflows/merge-gate-extension.yml
            (% if secrets.merge_gate_extension %)
            secrets:
              (% for secret_name in secrets.merge_gate_extension %)
              (( secret_name )): ${{ secrets.(( secret_name )) }}
              (% endfor %)
            (% endif %)
            permissions:
              contents: read
          (% endif %)

        """
        expected_yaml = """
        jobs:
        run-unit-tests:
          name: Unit Tests (Python-${{ matrix.python-versions }})
          runs-on: "ubuntu-24.04"
          permissions:
            contents: read
          strategy:
            fail-fast: false
            matrix:
              python-versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]

          steps:
            - name: Check out Repository
              id: check-out-repository
              uses: actions/checkout@v6

        merge-gate-extension:
          uses: ./.github/workflows/merge-gate-extension.yml
          secrets:
            MERGE_GATE_SECRET: ${{ secrets.MERGE_GATE_SECRET }}
            ANOTHER_SECRET: ${{ secrets.ANOTHER_SECRET }}
          permissions:
            contents: read

        """
        workflow_directory = project_config.github_workflow_directory
        workflow_directory.mkdir(parents=True)
        (workflow_directory / "merge-gate-extension.yml").touch()

        custom_workflow_secrets = project_config.custom_workflow_secrets.model_copy(
            update={
                "merge_gate_extension": (
                    "MERGE_GATE_SECRET",
                    "ANOTHER_SECRET",
                )
            }
        )
        updated_project_config = project_config.model_copy(
            update={"custom_workflow_secrets": custom_workflow_secrets}
        )
        yaml_renderer = YamlRenderer(
            github_template_dict=updated_project_config.github_template_dict,
            file_path=test_yml,
        )

        content = cleandoc(input_yaml)
        test_yml.write_text(content)

        yaml_dict = yaml_renderer.get_yaml_dict()
        assert yaml_renderer.get_as_string(yaml_dict) == cleandoc(expected_yaml)

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
        ) as ex:
            yaml_renderer.get_yaml_dict()
        assert isinstance(ex.value.__cause__, UndefinedError)
        assert "'bad_jinja' is undefined" in str(ex.value.__cause__)

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
        ) as ex:
            yaml_renderer.get_yaml_dict()
        assert isinstance(ex.value.__cause__, TemplateSyntaxError)
        assert "unexpected ')'" in str(ex.value.__cause__)
