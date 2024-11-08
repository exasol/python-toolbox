import pytest
import rich.console

from exasol.toolbox.nox._dependencies_check import Dependencies, report_illegal


@pytest.mark.parametrize(
    "toml,expected",
    [
        (
            """
            """,
            {}
        ),
        (
            """
[tool.poetry.dependencies]
python = "^3.8"
example-url1 = {url = "https://example.com/my-package-0.1.0.tar.gz"}

[tool.poetry.dev.dependencies]
nox = ">=2022.8.7"
example-url2 = {url = "https://example.com/my-package-0.2.0.tar.gz"}

[tool.poetry.group.test.dependencies]
sphinx = ">=5.3,<8"
example-git = {git = "git@github.com:requests/requests.git"}

[tool.poetry.group.dev.dependencies]
pytest = ">=7.2.2,<9"
example-path1 = {path = "../my-package/dist/my-package-0.1.0.tar.gz"}
            """,
            {
                "tool.poetry.dependencies": ["example-url1 = {'url': 'https://example.com/my-package-0.1.0.tar.gz'}"],
                "tool.poetry.dev.dependencies": ["example-url2 = {'url': 'https://example.com/my-package-0.2.0.tar.gz'}"],
                "tool.poetry.group.test.dependencies": ["example-git = {'git': 'git@github.com:requests/requests.git'}"],
                "tool.poetry.group.dev.dependencies": ["example-path1 = {'path': '../my-package/dist/my-package-0.1.0.tar.gz'}"],
            }
        ),
        (
            """
[tool.poetry.dev.dependencies]
nox = ">=2022.8.7"
example-url2 = {url = "https://example.com/my-package-0.2.0.tar.gz"}

[tool.poetry.group.test.dependencies]
sphinx = ">=5.3,<8"
example-git = {git = "git@github.com:requests/requests.git"}

[tool.poetry.group.dev.dependencies]
pytest = ">=7.2.2,<9"
example-path1 = {path = "../my-package/dist/my-package-0.1.0.tar.gz"}
            """,
            {
                "tool.poetry.dev.dependencies": ["example-url2 = {'url': 'https://example.com/my-package-0.2.0.tar.gz'}"],
                "tool.poetry.group.test.dependencies": ["example-git = {'git': 'git@github.com:requests/requests.git'}"],
                "tool.poetry.group.dev.dependencies": ["example-path1 = {'path': '../my-package/dist/my-package-0.1.0.tar.gz'}"],
            }
        ),
        (
            """
[tool.poetry.dependencies]
python = "^3.8"
example-url1 = {url = "https://example.com/my-package-0.1.0.tar.gz"}

[tool.poetry.group.test.dependencies]
sphinx = ">=5.3,<8"
example-git = {git = "git@github.com:requests/requests.git"}

[tool.poetry.group.dev.dependencies]
pytest = ">=7.2.2,<9"
example-path1 = {path = "../my-package/dist/my-package-0.1.0.tar.gz"}
            """,
            {
                "tool.poetry.dependencies": ["example-url1 = {'url': 'https://example.com/my-package-0.1.0.tar.gz'}"],
                "tool.poetry.group.test.dependencies": ["example-git = {'git': 'git@github.com:requests/requests.git'}"],
                "tool.poetry.group.dev.dependencies": ["example-path1 = {'path': '../my-package/dist/my-package-0.1.0.tar.gz'}"],
            }
        ),
        (
            """
[tool.poetry.dependencies]
python = "^3.8"
example-url1 = {url = "https://example.com/my-package-0.1.0.tar.gz"}

[tool.poetry.dev.dependencies]
nox = ">=2022.8.7"
example-url2 = {url = "https://example.com/my-package-0.2.0.tar.gz"}
            """,
            {
                "tool.poetry.dependencies": ["example-url1 = {'url': 'https://example.com/my-package-0.1.0.tar.gz'}"],
                "tool.poetry.dev.dependencies": ["example-url2 = {'url': 'https://example.com/my-package-0.2.0.tar.gz'}"],
            }
        )
    ]
)
def test_dependency_check_parse(toml, expected):
    dependencies =  dependencies = Dependencies.parse(toml)
    assert dependencies.illegal == expected


@pytest.mark.parametrize(
    "toml,expected",
    [
        (
            """
[tool.poetry.dependencies]
python = "^3.8"
example-url1 = {url = "https://example.com/my-package-0.1.0.tar.gz"}

[tool.poetry.dev.dependencies]
nox = ">=2022.8.7"
example-url2 = {url = "https://example.com/my-package-0.2.0.tar.gz"}

[tool.poetry.group.test.dependencies]
sphinx = ">=5.3,<8"
example-git = {git = "git@github.com:requests/requests.git"}

[tool.poetry.group.dev.dependencies]
pytest = ">=7.2.2,<9"
example-path1 = {path = "../my-package/dist/my-package-0.1.0.tar.gz"}
example-path2 = {path = "../my-package/dist/my-package-0.2.0.tar.gz"}
            """,
            """5 illegal dependencies

[tool.poetry.dependencies]
example-url1 = {'url': 'https://example.com/my-package-0.1.0.tar.gz'}

[tool.poetry.dev.dependencies]
example-url2 = {'url': 'https://example.com/my-package-0.2.0.tar.gz'}

[tool.poetry.group.test.dependencies]
example-git = {'git': 'git@github.com:requests/requests.git'}

[tool.poetry.group.dev.dependencies]
example-path1 = {'path': '../my-package/dist/my-package-0.1.0.tar.gz'}
example-path2 = {'path': '../my-package/dist/my-package-0.2.0.tar.gz'}

"""
        ),
    ]
)
def test_dependencies_check_report(toml, expected, capsys):
    console = rich.console.Console()
    dependencies = Dependencies.parse(toml)
    report_illegal(dependencies.illegal, console)
    assert capsys.readouterr().out == expected
