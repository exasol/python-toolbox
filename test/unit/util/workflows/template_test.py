from inspect import cleandoc

from exasol.toolbox.util.workflows.template import TemplateToWorkflow
from noxconfig import PROJECT_CONFIG

TEMPLATE = """
name: Build & Publish

on:
  workflow_call:
    secrets:
      PYPI_TOKEN:
          required: true

jobs:
  cd-job:
    name: Continuous Delivery
    runs-on: "(( os_version ))"
    permissions:
      contents: write
    steps:
      # Comment in nested area
      - name: SCM Checkout # Comment inline
        uses: actions/checkout@v6
        # Comment in step
      - name: Setup Python & Poetry Environment
        uses: exasol/python-toolbox/.github/actions/python-environment@v5
        with:
          python-version: "(( minimum_python_version ))"
          poetry-version: "(( dependency_manager_version ))"
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

WORKFLOW = """
name: Build & Publish

on:
  workflow_call:
    secrets:
      PYPI_TOKEN:
        required: true

jobs:
  cd-job:
    name: Continuous Delivery
    runs-on: "ubuntu-24.04"
    permissions:
      contents: write
    steps:
      # Comment in nested area
      - name: SCM Checkout # Comment inline
        uses: actions/checkout@v6
        # Comment in step
      - name: Setup Python & Poetry Environment
        uses: exasol/python-toolbox/.github/actions/python-environment@v5
        with:
          python-version: "3.10"
          poetry-version: "2.3.0"
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


class TestTemplateToWorkflow:
    @staticmethod
    def test_works_as_expected():
        template_to_workflow = TemplateToWorkflow(
            template_str=TEMPLATE,
            github_template_dict=PROJECT_CONFIG.github_template_dict,
        )
        assert template_to_workflow.convert() == cleandoc(WORKFLOW)
