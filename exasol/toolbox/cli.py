from argparse import ArgumentTypeError

from exasol.toolbox.release import Version


def version(arg: str) -> Version:
    try:
        return Version.from_string(arg)
    except Exception as ex:
        msg = f"Expected format: <number>.<number>.<number>, e.g. 1.2.3, actual: {arg}"
        raise ArgumentTypeError(msg) from ex
