from unittest.mock import (
    MagicMock,
    patch,
)

import pytest

from exasol.toolbox.nox._documentation import _check_failed_links


@pytest.mark.parametrize(
    "results, expected",
    [
        ([""], ([""], [])),
        (
            [
                '{"filename": "ftest.rst", "lineno": 1, "status": "broken", "code": 0, "uri": "https://ftest", "info": ""}',
                '{"filename": "ttest.rst", "lineno": 1, "status": "working", "code": 0, "uri": "https://ttest", "info": ""}',
                '{"filename": "rtest.rst", "lineno": 1, "status": "redirected", "code": 0, "uri": "https://rtest", "info": ""}',
            ],
            (
                [
                    '{"filename": "ftest.rst", "lineno": 1, "status": "broken", "code": 0, "uri": "https://ftest", "info": ""}',
                    '{"filename": "ttest.rst", "lineno": 1, "status": "working", "code": 0, "uri": "https://ttest", "info": ""}',
                    '{"filename": "rtest.rst", "lineno": 1, "status": "redirected", "code": 0, "uri": "https://rtest", "info": ""}',
                ],
                [
                    '{"filename": "ftest.rst", "lineno": 1, "status": "broken", "code": 0, '
                    '"uri": "https://ftest", "info": ""}'
                ],
            ),
        ),
    ],
)
def test_failed_links(results, expected):
    frequest = MagicMock()
    frequest.status_code = 404
    trequest = MagicMock()
    trequest.status_code = 200
    history1 = MagicMock()
    history1.url = "https://rtest"
    history2 = MagicMock()
    history2.url = "https://rtest.next"
    rrequest = MagicMock()
    rrequest.history = [history1, history2]
    rrequest.url = "https://rtest.end"
    with patch(
        "exasol.toolbox.nox._documentation.requests.get",
        side_effect=[frequest, rrequest],
    ):
        actual = _check_failed_links(results)
    assert actual == expected
