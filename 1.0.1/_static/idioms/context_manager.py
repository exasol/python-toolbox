# With Context Manager
import os
from contextlib import contextmanager


@contextmanager
def chdir(path):
    old_dir = os.getcwd()
    os.chdir(path)
    yield path
    os.chdir(old_dir)


def initialize(directory):
    with chdir(directory) as _working_dir:
        with open("some-file.txt", "w") as f:
            f.write("Some content")


# With Python 3.11
from contextlib import chdir


def initialize(directory):
    with chdir(directory) as _working_dir:
        with open("some-file.txt", "w") as f:
            f.write("Some content")


# Naive Approach
import os


def initialize(directory):
    old_dir = os.getcwd()
    os.chdir(directory)
    os.chdir(old_dir)
    with open("some-file.txt", "w") as f:
        f.write("Some content")
    os.chdir(old_dir)
