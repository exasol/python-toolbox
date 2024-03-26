from pathlib import Path
from typing import List


def replace_version(template: Path, version: str) -> None:
    with open(template, encoding="utf-8") as file:
        input_lines = file.readlines()

    output_lines = _replace_version(
        input_lines, "exasol/python-toolbox/.github/", version
    )

    with open(template, "w", encoding="utf-8") as file:
        file.writelines(output_lines)


def _replace_version(input_lines, replace_filter, version) -> List[str]:
    filtered_lines = _filter_replace_lines(input_lines, replace_filter)
    replaced_filtered_lines = _replace_filtered_line(filtered_lines, version)
    return _replace_lines(input_lines, replaced_filtered_lines)


def _filter_replace_lines(
    input_lines: str, replace_filter: str
) -> List[tuple[int, str]]:
    filtered_lines = (
        (index, line)
        for index, line in enumerate(input_lines)
        if line.find(replace_filter) != -1
    )
    filtered_filtered_lines = [
        (index, line) for index, line in filtered_lines if line.find("@") != -1
    ]
    return filtered_filtered_lines


def _replace_filtered_line(
    filtered_lines: List[tuple[int, str]], version: str
) -> List[tuple[int, str]]:
    return [
        (index, line[0 : line.index("@") + 1] + version + "\n")
        for index, line in filtered_lines
    ]


def _replace_lines(lines: List[str], replace_lines: List[tuple[int, str]]):
    output = lines
    for index, line in replace_lines:
        output[index] = line
    return output


replace_version(Path("foo/ci.yml"), "9.9.9")
