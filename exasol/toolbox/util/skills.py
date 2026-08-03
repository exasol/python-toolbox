from collections.abc import Mapping
from pathlib import Path
from typing import Final

import importlib_resources as resources

SKILLS_DIRECTORY: Final = "exasol.toolbox.skills"
PTB_SKILL_NAME: Final = "exasol-python-toolbox"


def get_skill_path(skill_name: str = PTB_SKILL_NAME) -> Path:
    """
    Return the path to a packaged skill.
    """
    return Path(str(resources.files(SKILLS_DIRECTORY) / skill_name))


def get_skill_files(skill_name: str = PTB_SKILL_NAME) -> Mapping[str, Path]:
    """
    Return packaged skill files.

    The keys are paths relative to the skill root.
    """
    skill_path = get_skill_path(skill_name)
    return {
        str(path.relative_to(skill_path)): path
        for path in skill_path.rglob("*")
        if path.is_file()
    }
