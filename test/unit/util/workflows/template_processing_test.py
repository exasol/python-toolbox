from inspect import cleandoc

from exasol.toolbox.util.workflows.template_processing import TemplateToWorkflow
from noxconfig import PROJECT_CONFIG


class TestTemplateToWorkflow:
    @staticmethod
    def test_works_for_general_case():
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

        template_to_workflow = TemplateToWorkflow(
            template_str=cleandoc(input_yaml),
            github_template_dict=PROJECT_CONFIG.github_template_dict,
        )
        assert template_to_workflow.render() == cleandoc(input_yaml)

    @staticmethod
    def test_fixes_extra_horizontal_whitespace():
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

        template_to_workflow = TemplateToWorkflow(
            template_str=cleandoc(input_yaml),
            github_template_dict=PROJECT_CONFIG.github_template_dict,
        )
        assert template_to_workflow.render() == cleandoc(expected_yaml)

    @staticmethod
    def test_keeps_comments():
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

        template_to_workflow = TemplateToWorkflow(
            template_str=cleandoc(input_yaml),
            github_template_dict=PROJECT_CONFIG.github_template_dict,
        )

        assert template_to_workflow.render() == cleandoc(expected_yaml)

    @staticmethod
    def test_keeps_quotes_for_variables_as_is():
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

        template_to_workflow = TemplateToWorkflow(
            template_str=cleandoc(input_yaml),
            github_template_dict=PROJECT_CONFIG.github_template_dict,
        )

        assert template_to_workflow.render() == cleandoc(expected_yaml)

    @staticmethod
    def test_updates_jinja_variables():
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

        template_to_workflow = TemplateToWorkflow(
            template_str=cleandoc(input_yaml),
            github_template_dict=PROJECT_CONFIG.github_template_dict,
        )

        assert template_to_workflow.render() == cleandoc(expected_yaml)

    @staticmethod
    def test_preserves_list_format():
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

        template_to_workflow = TemplateToWorkflow(
            template_str=cleandoc(input_yaml),
            github_template_dict=PROJECT_CONFIG.github_template_dict,
        )

        assert template_to_workflow.render() == cleandoc(input_yaml)
