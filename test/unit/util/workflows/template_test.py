from inspect import cleandoc

from exasol.toolbox.util.workflows.template import TemplateToWorkflow
from noxconfig import PROJECT_CONFIG

TEMPLATE = """
name: Publish Documentation

on:
  workflow_call:
  workflow_dispatch:

# A multi-line comment
# because why not make it harder
jobs:
  build-documentation:
    # My second comment
    runs-on: "(( os_version ))"
    permissions:
      contents: read
    steps:
      - name: SCM Checkout # A comment inline
        uses: actions/checkout@v6
        with:
          fetch-depth: 0
      - name: Setup Python & Poetry Environment
        # My third comment
        uses: exasol/python-toolbox/.github/actions/python-environment@v5
        with:
          # My fourth comment
          python-version: "(( minimum_python_version ))"
          poetry-version: "(( dependency_manager_version ))"

      - name: Build Documentation
        run: |
          poetry run -- nox -s docs:multiversion
          mv .html-documentation html-documentation

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v4
        with:
          path: html-documentation

  deploy-documentation:
    needs: [ build-documentation ]
    permissions:
      contents: read
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: "(( os_version ))"
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

"""

WORKFLOW = """
name: Publish Documentation
on:
  workflow_call:
  workflow_dispatch:
# A multi-line comment
# because why not make it harder
jobs:
  build-documentation:
    # My second comment
    runs-on: "ubuntu-24.04"
    permissions:
      contents: read
    steps:
    - name: SCM Checkout
      uses: actions/checkout@v6
      with:
        fetch-depth: 0
    - name: Setup Python & Poetry Environment
      # My third comment
      uses: exasol/python-toolbox/.github/actions/python-environment@v5
      with:
        # My fourth comment
        python-version: "3.10"
        poetry-version: "2.3.0"
    - name: Build Documentation
      run: |
        poetry run -- nox -s docs:multiversion
        mv .html-documentation html-documentation
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v4
      with:
        path: html-documentation
  deploy-documentation:
    needs:
    - build-documentation
    permissions:
      contents: read
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: "${{ steps.deployment.outputs.page_url }}"
    runs-on: "ubuntu-24.04"
    steps:
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v4

"""


class TestTemplateToWorkflow:
    @staticmethod
    def test_works_as_expected():
        template_to_workflow = TemplateToWorkflow(
            template_str=TEMPLATE,
            github_template_dict=PROJECT_CONFIG.github_template_dict,
        )
        assert template_to_workflow.convert() == cleandoc(WORKFLOW)
