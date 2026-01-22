from contextlib import ExitStack
from inspect import cleandoc
from pathlib import Path

import pytest
from yaml.parser import ParserError

from exasol.toolbox.tools.template import (
    _render_template,
    _templates,
)
from exasol.toolbox.tools.workflow import PKG

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
        uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - name: Setup Python & Poetry Environment
        uses: exasol/python-toolbox/.github/actions/python-environment@v4
        with:
          python-version: "3.10"
          poetry-version: "2.3.0"

      - name: Build Documentation
        run: |
          poetry run -- nox -s docs:multiversion
          rm -r .html-documentation/*/.doctrees

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: .html-documentation

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
    pkg = PKG
    template = "gh-pages"

    def test_works_as_expected(self):
        src = Path(_templates(self.pkg)[self.template])
        with ExitStack() as stack:
            rendered_str = _render_template(src=src, stack=stack)
        assert rendered_str == cleandoc(RENDERED_TEMPLATE) + "\n"

    @staticmethod
    def test_fails_when_yaml_malformed(tmp_path):
        file_path = tmp_path / "test.yaml"
        file_path.write_text(BAD_TEMPLATE)
        with pytest.raises(ParserError, match="while parsing a block collection"):
            with ExitStack() as stack:
                _render_template(src=file_path, stack=stack)
