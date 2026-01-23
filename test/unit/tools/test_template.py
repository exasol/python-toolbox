from contextlib import ExitStack
from inspect import cleandoc

import pytest
from yaml.parser import ParserError

from exasol.toolbox.tools.template import (
    _render_template,
)

TEMPLATE = """
name: Publish Documentation

on:
  workflow_call:
  workflow_dispatch:

jobs:

  build-documentation:
    runs-on: "(( os_version ))"
    permissions:
      contents: read
    steps:
      - name: SCM Checkout
        uses: actions/checkout@v6
        with:
          fetch-depth: 0

      - name: Setup Python & Poetry Environment
        uses: exasol/python-toolbox/.github/actions/python-environment@v5
        with:
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

RENDERED_TEMPLATE = """
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
        uses: actions/checkout@v6
        with:
          fetch-depth: 0

      - name: Setup Python & Poetry Environment
        uses: exasol/python-toolbox/.github/actions/python-environment@v5
        with:
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
    needs: [ build-documentation ]
    permissions:
      contents: read
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: "ubuntu-24.04"
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

"""

BAD_TEMPLATE = """
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


class TestRenderTemplate:
    @staticmethod
    def test_works_as_expected(tmp_path):
        file_path = tmp_path / "test.yml"
        file_path.write_text(TEMPLATE)
        with ExitStack() as stack:
            rendered_str = _render_template(src=file_path, stack=stack)
        assert rendered_str == cleandoc(RENDERED_TEMPLATE) + "\n"

    @staticmethod
    def test_fails_when_yaml_malformed(tmp_path):
        file_path = tmp_path / "test.yaml"
        file_path.write_text(BAD_TEMPLATE)
        with pytest.raises(ParserError, match="while parsing a block collection"):
            with ExitStack() as stack:
                _render_template(src=file_path, stack=stack)
