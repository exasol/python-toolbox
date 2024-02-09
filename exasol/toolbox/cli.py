from argparse import ArgumentTypeError

from exasol.toolbox.release import Version


def version(arg):
    try:
        return Version.from_string(arg)
    except Exception as ex:
        raise ArgumentTypeError() from ex
