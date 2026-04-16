from enum import (
    Enum,
)


class Rating(Enum):
    """
    A = Excellent
    B = Good
    C = Satisfactory (Ok, could be better though)
    D = Poor (Improvement necessary)
    E = Bad (Need for action)
    F = Broken (Get it fixed!)
    N/A = Rating is not available
    """

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    NotAvailable = "N/A"

    def __format__(self, format_spec: str) -> str:
        if format_spec == "n":
            return f"{self.value}"
        return str(self)

    @staticmethod
    def from_score(score: float) -> "Rating":
        if 0 <= score < 1:
            return Rating.F
        elif 1 <= score < 3:
            return Rating.E
        elif 3 <= score < 4:
            return Rating.D
        elif 4 <= score < 6:
            return Rating.C
        elif 6 <= score < 8:
            return Rating.B
        elif 8 <= score <= 10:
            return Rating.A
        else:
            raise ValueError(
                "Uncategorized score, score should be in the following interval [0,10]."
            )

    @staticmethod
    def bandit_rating(score: float) -> "Rating":
        score = round(score, 3)
        if score <= 0.2:
            return Rating.F
        elif 0.2 < score <= 1.6:
            return Rating.E
        elif 1.6 < score <= 3:
            return Rating.D
        elif 3 < score <= 4.4:
            return Rating.C
        elif 4.4 < score <= 5.8:
            return Rating.B
        elif 5.8 < score <= 6:
            return Rating.A
        else:
            raise ValueError(
                "Uncategorized score, score should be in the following interval [0,6]."
            )
