import argparse
import contextlib
import glob
import itertools
import json
import logging
import multiprocessing
import os
import pathlib
import re
import shutil
import string
import subprocess
import sys
import tempfile
from importlib import resources

from jinja2 import Template
from rich.console import Console
from rich.logging import RichHandler
from sphinx import config as sphinx_config
from sphinx import project as sphinx_project

from exasol.toolbox.sphinx.multiversion import (
    git,
    sphinx,
)

logging.basicConfig(
    level="INFO",
    datefmt="[%X]",
    handlers=[RichHandler(console=Console(stderr=True), show_time=False)],
)
logger = logging.getLogger(__name__)


@contextlib.contextmanager
def working_dir(path):
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def load_sphinx_config_worker(q, confpath, confoverrides, add_defaults):
    try:
        with working_dir(confpath):
            current_config = sphinx_config.Config.read(
                confpath,
                confoverrides,
            )

        if add_defaults:
            current_config.add(
                "smv_tag_whitelist", sphinx.DEFAULT_TAG_WHITELIST, "html", str
            )
            current_config.add(
                "smv_branch_whitelist",
                sphinx.DEFAULT_TAG_WHITELIST,
                "html",
                str,
            )
            current_config.add(
                "smv_remote_whitelist",
                sphinx.DEFAULT_REMOTE_WHITELIST,
                "html",
                str,
            )
            current_config.add(
                "smv_released_pattern",
                sphinx.DEFAULT_RELEASED_PATTERN,
                "html",
                str,
            )
            current_config.add(
                "smv_outputdir_format",
                sphinx.DEFAULT_OUTPUTDIR_FORMAT,
                "html",
                str,
            )
            current_config.add(
                "smv_build_targets",
                sphinx.DEFAULT_BUILD_TARGETS,
                "html",
                {str: {str: str}},
            )
            current_config.add("smv_prefer_remote_refs", False, "html", bool)
            current_config.add("smv_prebuild_command", "", "html", str)
            current_config.add("smv_prebuild_export_pattern", "", "html", str)
            current_config.add("smv_prebuild_export_destination", "", "html", str)
            current_config.add("smv_postbuild_command", "", "html", str)
            current_config.add("smv_postbuild_export_pattern", "", "html", str)
            current_config.add("smv_postbuild_export_destination", "", "html", str)
            current_config.add(
                "smv_clean_intermediate_files",
                sphinx.DEFAULT_CLEAN_INTERMEDIATE_FILES_FLAG,
                "html",
                bool,
            )
        current_config.pre_init_values()
        current_config.init_values()
    except Exception as err:
        q.put(err)
        return

    q.put(current_config)


def load_sphinx_config(confpath, confoverrides, add_defaults=False):
    q = multiprocessing.Queue()
    proc = multiprocessing.Process(
        target=load_sphinx_config_worker,
        args=(q, confpath, confoverrides, add_defaults),
    )
    proc.start()
    proc.join()
    result = q.get_nowait()
    if isinstance(result, Exception):
        raise result
    return result


def get_python_flags():
    if sys.flags.bytes_warning:
        yield "-b"
    if sys.flags.debug:
        yield "-d"
    if sys.flags.hash_randomization:
        yield "-R"
    if sys.flags.ignore_environment:
        yield "-E"
    if sys.flags.inspect:
        yield "-i"
    if sys.flags.isolated:
        yield "-I"
    if sys.flags.no_site:
        yield "-S"
    if sys.flags.no_user_site:
        yield "-s"
    if sys.flags.optimize:
        yield "-O"
    if sys.flags.quiet:
        yield "-q"
    if sys.flags.verbose:
        yield "-v"
    for option, value in sys._xoptions.items():
        if value is True:
            yield from ("-X", option)
        else:
            yield from ("-X", f"{option}={value}")


def find_matching_files_and_dirs(pattern: str, root_dir: str) -> set:
    logger = logging.getLogger(__name__)
    logger.debug(f"Export pattern: {pattern}")
    regex = re.compile(pattern)
    matches = set()
    for root, dirs, files in os.walk(root_dir):
        for directory in dirs:
            directory_result = regex.match(directory)
            if directory_result:
                matches.add(os.path.join(root, directory))
        for file in files:
            file_result = regex.match(file)
            if file_result:
                matches.add(os.path.join(root, file))
    logger.debug(f"Pattern matches: {matches}")

    return matches


def export_to_destination(items: set, destination: str) -> None:
    logger = logging.getLogger(__name__)
    os.makedirs(destination, exist_ok=True)
    for item in items:
        # Copy file to desination
        if os.path.isfile(item):
            logger.debug(
                "Copying {} to {}".format(
                    item, os.path.join(destination, os.path.basename(item))
                )
            )
            shutil.copy(item, os.path.join(destination, os.path.basename(item)))

        # Copy directory to desination
        elif os.path.isdir(item):
            logger.debug(f"Copying {item} to {destination}")
            shutil.copytree(item, destination, dirs_exist_ok=True)


def _create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("sourcedir", help="path to documentation source files")
    parser.add_argument("outputdir", help="path to output directory")
    parser.add_argument(
        "filenames",
        nargs="*",
        help="a list of specific files to rebuild. Ignored if -a is specified",
    )
    parser.add_argument(
        "-c",
        metavar="PATH",
        dest="confdir",
        help=(
            "path where configuration file (conf.py) is located "
            "(default: same as SOURCEDIR)"
        ),
    )
    parser.add_argument(
        "-C",
        action="store_true",
        dest="noconfig",
        help="use no config file at all, only -D options",
    )
    parser.add_argument(
        "-D",
        metavar="setting=value",
        action="append",
        dest="define",
        default=[],
        help="override a setting in configuration file",
    )
    parser.add_argument(
        "--dump-metadata",
        action="store_true",
        help="dump generated metadata and exit",
    )
    return parser


def main(argv=None):
    parser = _create_parser()
    if not argv:
        argv = sys.argv[1:]
    args, argv = parser.parse_known_args(argv)

    try:
        if args.noconfig:
            sys.exit(1)
        sys.exit(_main(args, argv))
    except Exception as ex:
        logger.exception(ex)
        sys.exit(1)


def _main(args, argv):
    sourcedir_absolute = os.path.abspath(args.sourcedir)
    confdir_absolute = (
        os.path.abspath(args.confdir)
        if args.confdir is not None
        else sourcedir_absolute
    )

    # Conf-overrides
    confoverrides = {}
    for d in args.define:
        key, _, value = d.partition("=")
        confoverrides[key] = value

    # Parse config
    config = load_sphinx_config(confdir_absolute, confoverrides, add_defaults=True)

    # Get relative paths to root of git repository
    gitroot = pathlib.Path(git.get_toplevel_path(cwd=sourcedir_absolute)).resolve()
    cwd_absolute = os.path.abspath("")
    cwd_relative = os.path.relpath(cwd_absolute, str(gitroot))

    logger.debug("Git toplevel path: %s", str(gitroot))
    sourcedir = os.path.relpath(sourcedir_absolute, str(gitroot))
    logger.debug("Source dir (relative to git toplevel path): %s", str(sourcedir))
    if args.confdir:
        confdir = os.path.relpath(confdir_absolute, str(gitroot))
    else:
        confdir = sourcedir
    logger.debug("Conf dir (relative to git toplevel path): %s", str(confdir))
    conffile = os.path.join(confdir, "conf.py")

    # Get git references
    gitrefs = git.get_refs(
        str(gitroot),
        config.smv_tag_whitelist,
        config.smv_branch_whitelist,
        config.smv_remote_whitelist,
        files=(sourcedir, conffile),
    )

    # Order git refs
    if config.smv_prefer_remote_refs:
        gitrefs = sorted(gitrefs, key=lambda x: (not x.is_remote, *x))
    else:
        gitrefs = sorted(gitrefs, key=lambda x: (x.is_remote, *x))

    with tempfile.TemporaryDirectory() as tmp:
        # Generate Metadata
        metadata = {}
        outputdirs = set()
        for gitref in gitrefs:
            # Clone Git repo
            repopath = os.path.join(tmp, gitref.commit)
            try:
                git.copy_tree(str(gitroot), gitroot.as_uri(), repopath, gitref)
            except (OSError, subprocess.CalledProcessError):
                logger.error(
                    "Failed to copy git tree for %s to %s",
                    gitref.refname,
                    repopath,
                )
                continue

            # Find config
            confpath = os.path.join(repopath, confdir)
            try:
                current_config = load_sphinx_config(confpath, confoverrides)
            except (OSError, sphinx_config.ConfigError):
                logger.error(
                    "Failed load config for %s from %s",
                    gitref.refname,
                    confpath,
                )
                continue

            # Ensure that there are not duplicate output dirs
            outputdir = config.smv_outputdir_format.format(
                ref=gitref,
                config=current_config,
            )
            if outputdir in outputdirs:
                logger.warning(
                    "outputdir '%s' for %s conflicts with other versions",
                    outputdir,
                    gitref.refname,
                )
                continue
            outputdirs.add(outputdir)

            # Get List of files
            source_suffixes = current_config.source_suffix
            if isinstance(source_suffixes, str):
                source_suffixes = [current_config.source_suffix]

            current_sourcedir = os.path.join(repopath, sourcedir)
            project = sphinx_project.Project(current_sourcedir, source_suffixes)
            metadata[gitref.name] = {
                "name": gitref.name,
                "project": current_config.project,
                "version": current_config.version,
                "release": current_config.release,
                "rst_prolog": current_config.rst_prolog,
                "is_released": bool(
                    re.match(config.smv_released_pattern, gitref.refname)
                ),
                "source": gitref.source,
                "creatordate": gitref.creatordate.strftime(sphinx.DATE_FMT),
                "basedir": repopath,
                "sourcedir": current_sourcedir,
                "outputdir": os.path.join(os.path.abspath(args.outputdir), outputdir),
                "confdir": confpath,
                "docnames": list(project.discover()),
                "build_targets": config.smv_build_targets,
            }

        if args.dump_metadata:
            print(json.dumps(metadata, indent=2))
            return 0

        if not metadata:
            logger.error("No matching refs found!")
            return 2

        # Write Metadata
        metadata_path = os.path.abspath(os.path.join(tmp, "versions.json"))
        with open(metadata_path, mode="w", encoding="utf-8") as fp:
            json.dump(metadata, fp, indent=2)

        # Run Sphinx
        argv.extend(["-D", f"smv_metadata_path={metadata_path}"])
        for version_name, data in metadata.items():
            os.makedirs(data["outputdir"], exist_ok=True)

            defines = itertools.chain(
                *(("-D", string.Template(d).safe_substitute(data)) for d in args.define)
            )

            current_argv = argv.copy()
            current_argv.extend(
                [
                    *defines,
                    "-D",
                    f"smv_current_version={version_name}",
                    "-c",
                    confdir_absolute,
                    *args.filenames,
                ]
            )
            current_cwd = os.path.join(data["basedir"], cwd_relative)
            if config.smv_prebuild_command != "":
                logger.debug(
                    "Running prebuild command: %r", config.smv_prebuild_command
                )
                subprocess.check_call(
                    config.smv_prebuild_command, cwd=current_cwd, shell=True
                )

                if config.smv_prebuild_export_pattern != "":
                    matches = find_matching_files_and_dirs(
                        config.smv_prebuild_export_pattern, current_cwd
                    )
                    export_dst = os.path.join(
                        data["outputdir"],
                        config.smv_prebuild_export_destination,
                    )
                    export_to_destination(matches, export_dst)

            for build_target_name, build_target in data["build_targets"].items():
                builder = build_target.get("builder", None)
                if not builder:
                    raise AttributeError(
                        "Builder for build target {} not defined".format(
                            build_target_name
                        )
                    )

                downloadable = build_target.get("downloadable", False)
                download_format = build_target.get("download_format", "")

                if downloadable and download_format == "":
                    raise ValueError(
                        (
                            "Download format for build target {} not defined "
                            "but downloadable is True"
                        ).format(build_target_name)
                    )

                flag = "-b"
                builder_modifier = builder
                if builder == "latexpdf" or builder == "info":
                    flag = "-M"

                build_args = [flag, builder]
                target_build_dir = "{}/{}".format(data["outputdir"], builder_modifier)
                logger.debug(
                    "Running sphinx-build with args: %r",
                    build_args + current_argv,
                )
                # Create sphinx-build command
                cmd = (
                    sys.executable,
                    *get_python_flags(),
                    "-m",
                    "sphinx",
                    *build_args,
                    data["sourcedir"],
                    target_build_dir,
                    *current_argv,
                )
                current_cwd = os.path.join(data["basedir"], cwd_relative)
                env = os.environ.copy()
                env.update(
                    {
                        "SPHINX_MULTIVERSION_NAME": data["name"],
                        "SPHINX_MULTIVERSION_VERSION": data["version"],
                        "SPHINX_MULTIVERSION_RELEASE": data["release"],
                        "SPHINX_MULTIVERSION_SOURCEDIR": data["sourcedir"],
                        "SPHINX_MULTIVERSION_OUTPUTDIR": data["outputdir"],
                        "SPHINX_MULTIVERSION_CONFDIR": data["confdir"],
                    }
                )
                # Run sphinx-build
                subprocess.check_call(cmd, cwd=current_cwd, env=env)

                # Create artefacts if this build target should be downloadable
                if downloadable:
                    artefact_dir = "{}/artefacts".format(data["outputdir"])
                    os.makedirs(artefact_dir, exist_ok=True)
                    filename = "{project}_docs-{version}".format(
                        project=config.project.replace(" ", ""),
                        version=version_name.replace("/", "-"),
                    )

                    # Make an archive out of the build targets build directory
                    # Archive types supported by shutil.make_archive
                    if download_format in sphinx.ARCHIVE_TYPES:
                        shutil.make_archive(
                            "{}/{}-{}".format(
                                artefact_dir, filename, build_target_name
                            ),
                            download_format,
                            target_build_dir,
                        )
                    else:
                        # Find files matching project-name.extension, e.g.
                        # example.pdf in the target build directory
                        candidate_files = glob.glob(
                            "{build_dir}/**/*.{extension}".format(
                                build_dir=target_build_dir,
                                extension=download_format,
                            ),
                            recursive=True,
                        )
                        if len(candidate_files) > 1:
                            build_file_pattern = "{project}.{extension}".format(
                                project=config.project.replace(" ", ""),
                                extension=download_format,
                            )
                            build_artefacts = [
                                x
                                for x in candidate_files
                                if pathlib.Path(x.lower()).name
                                == build_file_pattern.lower()
                            ]
                        else:
                            build_artefacts = candidate_files
                        if len(build_artefacts) == 0:
                            logger.warning(
                                ("Build artefact {project}" "not found.").format(
                                    project=build_file_pattern.lower(),
                                )
                            )
                        elif len(build_artefacts) > 1:
                            logger.warning(
                                (
                                    "Ambiguous build artefact results: {}. "
                                    "Files not moved to artefact directory."
                                ).format(build_artefacts)
                            )
                        else:
                            # Found a single file with appropriate extension
                            shutil.copy(
                                build_artefacts[0],
                                os.path.join(
                                    artefact_dir,
                                    f"{filename}.{download_format}",
                                ),
                            )

                # Clean up build directory
                # Move html target to root of outputdir, if it exists.
                if build_target_name == "HTML":
                    shutil.copytree(
                        os.path.join(target_build_dir),
                        os.path.join(data["outputdir"]),
                        dirs_exist_ok=True,
                    )
                # Remove build directories
                if config.smv_clean_intermediate_files:
                    shutil.rmtree(target_build_dir)

            if config.smv_postbuild_command != "":
                logger.debug(
                    "Running postbuild command: %r",
                    config.smv_postbuild_command,
                )
                subprocess.check_call(
                    config.smv_postbuild_command, cwd=current_cwd, shell=True
                )
                if config.smv_postbuild_export_pattern != "":
                    matches = find_matching_files_and_dirs(
                        config.smv_postbuild_export_pattern, current_cwd
                    )
                    export_dst = os.path.join(
                        data["outputdir"],
                        config.smv_postbuild_export_destination,
                    )
                    export_to_destination(matches, export_dst)

        with resources.path(
            "exasol.sphinx_extensions.multiversion.templates", "multiversion-index.html"
        ) as p:
            with open(p, encoding="utf-8") as f:
                template = Template(f.read())
            with open(
                os.path.join(args.outputdir, "index.html"), "w", encoding="utf-8"
            ) as f:
                ref = gitrefs[-1]
                f.write(template.render(version=ref.name))

    return 0
