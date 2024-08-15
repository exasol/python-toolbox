from tomlkit import loads
import pytest
from exasol.toolbox.tools.dependencies_check import _source_filter

@pytest.mark.parametrize(
    "filter,source,expected",
    [
        (
            ['url', 'git', 'path'],
            """example-url = {url = "https://example.com/my-package-0.1.0.tar.gz"}""",
            True),
        (
            ['url', 'git', 'path'],
            """example-git = {git = "git@github.com:requests/requests.git"}""",
            True),
        (
            ['url', 'git', 'path'],
            """example-path = {path = "../my-package/dist/my-package-0.1.0.tar.gz"}""",
            True),
        (
            ['url', 'git', 'path'],
            """example-url = {platform = "darwin", url = "https://example.com/my-package-0.1.0.tar.gz"}""",
            True),
        (
            ['url', 'git', 'path'],
            """example = "^2.31.0.6" """,
            False),
        (
            ['url', 'git', 'path'],
            """python = ">=3.8.0,<4.0" """,
            False
        )
    ]
)
def test_dependencies_check(filter, source, expected):
    for _, version in loads(source).items():
        assert _source_filter(version, filter) == expected
