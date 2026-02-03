import re

from yaml import SafeDumper
from yaml.resolver import Resolver

# Regex for common strings in YAML that lose quotes:
#   1. Version numbers (e.g., 2.3.0, 3.10)
#   2. OS/image names (e.g., ubuntu-24.04)
#   3. Numeric strings that look like octals or floats (e.g., 045, 1.2)
QUOTE_REGEX = re.compile(r"^(\d+\.\d+(\.\d+)?|[a-zA-Z]+-\d+\.\d+|0\d+)$")

# yaml uses a shorthand to identify "on" and "off" tags.
# for GitHub workflows, we do NOT want "on" replaced with "True".
for character in ["O", "o"]:
    Resolver.yaml_implicit_resolvers[character] = [
        x
        for x in Resolver.yaml_implicit_resolvers[character]
        if x[0] != "tag:yaml.org,2002:bool"
    ]


class GitHubDumper(SafeDumper):
    pass


def empty_representer(dumper: SafeDumper, data):
    """
    Leave empty fields like empty, instead of adding "null"

    Without using `empty_representer`
        on:
          workflow_call: null

    Using `empty_representer`
        on:
          workflow_call:
    """
    return dumper.represent_scalar("tag:yaml.org,2002:null", "")


def str_presenter(dumper: SafeDumper, data):
    """
    Present str in a custom format compatible with GitHub
    """
    # For line breaks in a multiline step, use pipe "|" instead of quotes "'"
    if "\n" in data:
        # Ensure it ends with \n so PyYAML doesn't add the '-' strip indicator
        if not data.endswith("\n"):
            data += "\n"
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")

    # For strings with versions, ensure that they are quoted '"' so that they
    # are not incorrectly parsed in the workflow, e.g. to an integer instead of a float.
    if QUOTE_REGEX.match(data):
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


GitHubDumper.add_representer(str, str_presenter)
GitHubDumper.add_representer(type(None), empty_representer)
