import collections
import datetime
import logging
import os
import re
import subprocess  # nosec: B404 - risk of subprocess is accepted
import tarfile
import tempfile

GitRef = collections.namedtuple(
    "GitRef",
    [
        "name",
        "commit",
        "source",
        "is_remote",
        "refname",
        "creatordate",
    ],
)

logger = logging.getLogger(__name__)


def get_toplevel_path(cwd=None):
    output = subprocess.check_output(
        (
            "git",
            "rev-parse",
            "--show-toplevel",
        ),
        cwd=cwd,
    ).decode()  # nosec: B603 - allow fixed git command
    return output.rstrip("\n")


def get_all_refs(gitroot):
    output = subprocess.check_output(
        (
            "git",
            "for-each-ref",
            "--format",
            "%(objectname)\t%(refname)\t%(creatordate:iso)",
            "refs",
        ),
        cwd=gitroot,
    ).decode()  # nosec: B603 - allow fixed git command and fixed arguments
    for line in output.splitlines():
        is_remote = False
        fields = line.strip().split("\t")
        if len(fields) != 3:
            continue

        commit = fields[0]
        refname = fields[1]
        creatordate = datetime.datetime.strptime(fields[2], "%Y-%m-%d %H:%M:%S %z")

        # Parse refname
        matchobj = re.match(r"^refs/(heads|tags|remotes/[^/]+)/(\S+)$", refname)
        if not matchobj:
            continue
        source = matchobj.group(1)
        name = matchobj.group(2)

        if source.startswith("remotes/"):
            is_remote = True

        yield GitRef(name, commit, source, is_remote, refname, creatordate)


def get_refs(gitroot, tag_whitelist, branch_whitelist, remote_whitelist, files=()):
    for ref in get_all_refs(gitroot):
        if ref.source == "tags":
            if tag_whitelist is None or not re.match(tag_whitelist, ref.name):
                logger.debug(
                    "Skipping '%s' because tag '%s' doesn't match the "
                    "whitelist pattern",
                    ref.refname,
                    ref.name,
                )
                continue
        elif ref.source == "heads":
            if branch_whitelist is None or not re.match(branch_whitelist, ref.name):
                logger.debug(
                    "Skipping '%s' because branch '%s' doesn't match the "
                    "whitelist pattern",
                    ref.refname,
                    ref.name,
                )
                continue
        elif ref.is_remote and remote_whitelist is not None:
            remote_name = ref.source.partition("/")[2]
            if not re.match(remote_whitelist, remote_name):
                logger.debug(
                    "Skipping '%s' because remote '%s' doesn't match the "
                    "whitelist pattern",
                    ref.refname,
                    remote_name,
                )
                continue
            if branch_whitelist is None or not re.match(branch_whitelist, ref.name):
                logger.debug(
                    "Skipping '%s' because branch '%s' doesn't match the "
                    "whitelist pattern",
                    ref.refname,
                    ref.name,
                )
                continue
        else:
            logger.debug("Skipping '%s' because its not a branch or tag", ref.refname)
            continue

        missing_files = [
            filename
            for filename in files
            if filename != "." and not file_exists(gitroot, ref.refname, filename)
        ]
        if missing_files:
            logger.debug(
                "Skipping '%s' because it lacks required files: %r",
                ref.refname,
                missing_files,
            )
            continue

        yield ref


def file_exists(gitroot, refname, filename):
    if os.sep != "/":
        # Git requires / path sep, make sure we use that
        filename = filename.replace(os.sep, "/")

    proc = subprocess.run(
        (
            "git",
            "cat-file",
            "-e",
            f"{refname}:{filename}",
        ),
        cwd=gitroot,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )  # nosec: B603 - allow fixed git command and internally defined arguments
    return proc.returncode == 0


def copy_tree(gitroot, dst, reference, sourcepath="."):
    with tempfile.SpooledTemporaryFile() as fp:
        subprocess.check_call(
            (
                "git",
                "archive",
                "--format",
                "tar",
                reference.commit,
                "--",
                sourcepath,
            ),
            cwd=gitroot,
            stdout=fp,
        )  # nosec: B603 - allow fixed git command and internally defined arguments
        fp.seek(0)
        with tarfile.TarFile(fileobj=fp) as tarfp:
            tarfp.extractall(dst)
