import subprocess  # nosec
from functools import wraps
from pathlib import Path


def run_command(func):
    @wraps(func)
    def wrapper(*args, **kwargs) -> str:
        command_list = func(*args, **kwargs)
        output = subprocess.run(
            command_list, capture_output=True, text=True, check=True
        )  # nosec
        return output.stdout.strip()

    return wrapper


class Git:
    @staticmethod
    @run_command
    def get_latest_tag():
        """
        Get the latest tag from the git repository.
        """
        return ["git", "describe", "--tags", "--abbrev=0"]

    @staticmethod
    @run_command
    def read_file_from_tag(tag: str, path: Path | str):
        """
        Read the contents of the specified file `path` at the point in
        time specified by git tag `tag`.
        """
        return ["git", "cat-file", "blob", f"{tag}:{path}"]

    @staticmethod
    def checkout(tag: str, source: Path, dest: Path) -> None:
        """
        Copy the specified file `source` at the point in time specified by
        git tag `tag` to file `dest` within the local filesystem.
        """
        contents = Git.read_file_from_tag(tag=tag, path=source)
        dest.write_text(contents)

    @staticmethod
    @run_command
    def create_and_switch_to_branch(branch_name: str):
        return ["git", "switch", "-c", branch_name]

    @staticmethod
    @run_command
    def toplevel():
        return ["git", "rev-parse", "--show-toplevel"]
