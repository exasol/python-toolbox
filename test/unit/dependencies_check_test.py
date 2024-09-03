from tomlkit import loads
import pytest
from exasol.toolbox.nox._dependencies_check import (
    _source_filter,
    _dependencies_check
)


@pytest.mark.parametrize(
    "filters,source,expected",
    [
        (
                ['url', 'git', 'path'],
                """example-url = {url = "https://example.com/my-package-0.1.0.tar.gz"}""",
                'url'),
        (
                ['url', 'git', 'path'],
                """example-git = {git = "git@github.com:requests/requests.git"}""",
                'git'),
        (
                ['url', 'git', 'path'],
                """example-path = {path = "../my-package/dist/my-package-0.1.0.tar.gz"}""",
                'path'),
        (
                ['url', 'git', 'path'],
                """example-url = {platform = "darwin", url = "https://example.com/my-package-0.1.0.tar.gz"}""",
                'url'),
        (
                ['url', 'git', 'path'],
                """example = "^2.31.0.6" """,
                None),
        (
                ['url', 'git', 'path'],
                """python = ">=3.8.0,<4.0" """,
                None
        )
    ]
)
def test_dependencies_check(filters, source, expected):
    for _, version in loads(source).items():
        assert _source_filter(version, filter) == expected


@pytest.mark.parametrize(
    "toml, expected",
    [
        (
                """[tool.poetry.dependencies]
python = "^3.8"
example-url = {url = "https://example.com/my-package-0.1.0.tar.gz"}

[tool.poetry.dev.dependencies]
nox = ">=2022.8.7"

[tool.poetry.group.test.dependencies]
sphinx = ">=5.3,<8"
example-git = {git = "git@github.com:requests/requests.git"}

[tool.poetry.group.dev.dependencies]
pytest = ">=7.2.2,<9"
example-path1 = {path = "../my-package/dist/my-package-0.1.0.tar.gz"}
example-path2 = {path = "../my-package/dist/my-package-0.2.0.tar.gz"}
""",
                """4 illegal dependencies:

[tool.poetry.dependencies]
example-url = {'url': 'https://example.com/my-package-0.1.0.tar.gz'}

[tool.poetry.group.test.dependencies]
example-git = {'git': 'git@github.com:requests/requests.git'}

[tool.poetry.group.dev.dependencies]
example-path1 = {'path': '../my-package/dist/my-package-0.1.0.tar.gz'}
example-path2 = {'path': '../my-package/dist/my-package-0.2.0.tar.gz'}
"""
        ),
    ]
)
def test_dependencies_check(toml, expected):
    assert _dependencies_check(toml) == expected
