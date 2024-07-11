from inspect import cleandoc

import pytest

from exasol.toolbox.metrics import (
    Rating,
    _static_code_analysis,
    _bandit_scoring,
)


@pytest.mark.parametrize(
    "rating,expected",
    [
        (Rating.A, "A"),
        (Rating.B, "B"),
        (Rating.C, "C"),
        (Rating.D, "D"),
        (Rating.E, "E"),
        (Rating.F, "F"),
        (Rating.NotAvailable, "N/A"),
    ],
)
def test_format_rating(rating, expected):
    actual = f"{rating:n}"
    assert actual == expected


@pytest.mark.parametrize(
    "score,expected",
    [
        (0.0, Rating.F),
        (0.9, Rating.F),
        (1.0, Rating.E),
        (2.9, Rating.E),
        (3.0, Rating.D),
        (3.9, Rating.D),
        (4.0, Rating.C),
        (5.9, Rating.C),
        (6.0, Rating.B),
        (7.9, Rating.B),
        (8.0, Rating.A),
        (10.0, Rating.A),
    ],
)
def test_rating_from_score(score, expected):
    actual = Rating.from_score(score)
    assert actual == expected


def test_rating_from_score_throws_exception_for_unknown_value():
    with pytest.raises(ValueError):
        _ = Rating.from_score(100)


@pytest.fixture
def named_temp_file(tmp_path):
    files = []

    def _factory(name, content):
        path = tmp_path / name
        mode = "w" if not isinstance(content, bytes) else "wb"
        with open(path, mode) as f:
            f.write(content)
            files.append(path)

        return path

    yield _factory

    for file in files:
        file.unlink()


@pytest.mark.parametrize(
    "content,expected",
    [
        (
            cleandoc(
                """
    ************* Module doc.user_guide.modules.sphinx.multiversion.conf
    doc/user_guide/modules/sphinx/multiversion/conf.py:8:0: W0622: Redefining built-in 'copyright' (redefined-builtin)
    doc/user_guide/modules/sphinx/multiversion/conf.py:4:0: C0103: Constant name "author" doesn't conform to UPPER_CASE naming style (invalid-name)
    doc/user_guide/modules/sphinx/multiversion/conf.py:5:0: C0103: Constant name "project" doesn't conform to UPPER_CASE naming style (invalid-name)
    doc/user_guide/modules/sphinx/multiversion/conf.py:6:0: C0103: Constant name "release" doesn't conform to UPPER_CASE naming style (invalid-name)
    doc/user_guide/modules/sphinx/multiversion/conf.py:7:0: C0103: Constant name "version" doesn't conform to UPPER_CASE naming style (invalid-name)
    doc/user_guide/modules/sphinx/multiversion/conf.py:8:12: C0209: Formatting a regular string which could be a f-string (consider-using-f-string)
    doc/user_guide/modules/sphinx/multiversion/conf.py:10:0: C0103: Constant name "html_theme" doesn't conform to UPPER_CASE naming style (invalid-name)
    doc/user_guide/modules/sphinx/multiversion/conf.py:19:0: C0103: Constant name "html_last_updated_fmt" doesn't conform to UPPER_CASE naming style (invalid-name)
    doc/user_guide/modules/sphinx/multiversion/conf.py:20:0: C0103: Constant name "master_doc" doesn't conform to UPPER_CASE naming style (invalid-name)
    doc/user_guide/modules/sphinx/multiversion/conf.py:21:0: C0103: Constant name "pygments_style" doesn't conform to UPPER_CASE naming style (invalid-name)
    doc/user_guide/modules/sphinx/multiversion/conf.py:41:0: C0103: Constant name "smv_remote_whitelist" doesn't conform to UPPER_CASE naming style (invalid-name)
    doc/user_guide/modules/sphinx/multiversion/conf.py:42:0: C0103: Constant name "smv_branch_whitelist" doesn't conform to UPPER_CASE naming style (invalid-name)
    doc/user_guide/modules/sphinx/multiversion/conf.py:43:0: C0103: Constant name "smv_tag_whitelist" doesn't conform to UPPER_CASE naming style (invalid-name)

    ------------------------------------------------------------------
    Your code has been rated at 7.80/10 (previous run: 7.86/10, -0.05)
    """
            ),
            Rating.B,
        ),
        (
            "",
            Rating.NotAvailable,
        ),
    ],
)
def test_static_code_analysis(
    named_temp_file, content, expected
):  # pylint: disable=redefined-outer-name
    coverage_report = named_temp_file(name=".lint.txt", content=content)
    actual = _static_code_analysis(coverage_report)
    assert actual == expected


@pytest.mark.parametrize(
    "rating, expected",
    [
        ([{"issue_severity": "HIGH", "issue_confidence": "HIGH"}], 0),
        ([{"issue_severity": "HIGH", "issue_confidence": "MEDIUM"}], 0),
        ([{"issue_severity": "HIGH", "issue_confidence": "LOW"}], 0),
        ([{"issue_severity": "MEDIUM", "issue_confidence": "HIGH"}], 1),
        ([{"issue_severity": "MEDIUM", "issue_confidence": "MEDIUM"}], 2),
        ([{"issue_severity": "MEDIUM", "issue_confidence": "LOW"}], 3),
        ([{"issue_severity": "LOW", "issue_confidence": "HIGH"}], 4),
        ([{"issue_severity": "LOW", "issue_confidence": "MEDIUM"}], 5),
        ([{"issue_severity": "LOW", "issue_confidence": "LOW"}], 6),
    ]
)
def test_bandit_scoring(rating, expected):
    actual = _bandit_scoring(rating)
    assert actual <= expected
