import pytest

from exasol.toolbox.metrics import (
    Rating,
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


def _level(char):
    levels = {"H": "HIGH", "M": "MEDIUM", "L": "LOW"}
    return levels[char]


def _ratings(cases):
    output = []
    for rating in cases:
        output.append(
            {
                "issue_severity": _level(rating[0]),
                "issue_confidence": _level(rating[1]),
            }
        )
    return output
