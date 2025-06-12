import re

def _section(line):
    regex = re.compile(r"^\[(.*)\]$")
    match = regex.match(line)
    return match.group(1) if match else ""
