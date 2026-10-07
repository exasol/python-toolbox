"""Models for validating packaged agent-skill evaluation cases."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


NonBlankString = Annotated[str, Field(pattern=r"\S")]


class ExpectedResponse(BaseModel):
    """Required and forbidden content for one evaluation response."""

    model_config = ConfigDict(extra="forbid")

    must_include: list[NonBlankString] = Field(min_length=1)
    must_not_include: list[NonBlankString] = Field(min_length=1)


class EvalCase(BaseModel):
    """One prompt and its expected response constraints."""

    model_config = ConfigDict(extra="forbid")

    id: NonBlankString
    category: NonBlankString
    prompt: NonBlankString
    expected: ExpectedResponse


class PackagedSkillEvalCases(BaseModel):
    """Schema for a packaged skill's ``eval_cases.yml`` file."""

    model_config = ConfigDict(extra="forbid")

    version: Literal[1]
    skill: NonBlankString
    cases: list[EvalCase] = Field(min_length=1)
