import re

from yaml import SafeDumper
from yaml.resolver import Resolver

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


def empty_representer(dumper, data):
    """
    Leave empty fields without 'null'

    on:
        workflow_call:
    """
    return dumper.represent_scalar("tag:yaml.org,2002:null", "")


# Regex for common strings that lose quotes:
# 1. Version numbers (e.g., 2.3.0, 3.10)
# 2. OS/image names (e.g., ubuntu-24.04)
# 3. Numeric strings that look like octals or floats (e.g., 045, 1.2)
QUOTE_REGEX = re.compile(r"^(\d+\.\d+(\.\d+)?|[a-zA-Z]+-\d+\.\d+|0\d+)$")


def str_presenter(dumper, data):
    # Use literal style '|' for strings with newlines
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    if QUOTE_REGEX.match(data):
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


# Register it to the dumper
GitHubDumper.add_representer(str, str_presenter)
GitHubDumper.add_representer(type(None), empty_representer)
