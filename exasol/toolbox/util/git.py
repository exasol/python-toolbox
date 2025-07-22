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
    def read_file_from_tag(tag: str, remote_file: str):
        """
        Read the contents of the specified file `remote_file` at the point in time
        specified by git tag `tag`.
        """
        return ["git", "cat-file", "blob", f"{tag}:{remote_file}"]

    @staticmethod
    def copy_remote_file_locally(
        tag: str, remote_file: str, destination_directory: Path
    ) -> None:
        """
        Copy the contents of the specified file `remote_file` at the point in time
        specified by git tag `tag` and copy it into the local `destination_directory/remote_file`.
        """
        contents = Git.read_file_from_tag(tag=tag, remote_file=remote_file)
        (destination_directory / remote_file).write_text(contents)

    @staticmethod
    @run_command
    def create_and_switch_to_branch(branch_name: str):
        return ["git", "switch", "-c", branch_name]
