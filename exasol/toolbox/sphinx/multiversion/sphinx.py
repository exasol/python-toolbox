import collections
import datetime
import json
import logging
import os
import posixpath

from sphinx import config as sphinx_config
from sphinx.locale import _
from sphinx.util import i18n as sphinx_i18n

from exasol.toolbox.util.version import Version as ExasolVersion
from exasol.toolbox.version import VERSION as PLUGIN_VERSION

logger = logging.getLogger(__name__)

DATE_FMT = "%Y-%m-%d %H:%M:%S %z"
DEFAULT_TAG_WHITELIST = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$"
DEFAULT_BRANCH_WHITELIST = r"^(master|main)"
DEFAULT_REMOTE_WHITELIST = None
DEFAULT_RELEASED_PATTERN = r"^tags/.*$"
DEFAULT_OUTPUTDIR_FORMAT = r"{ref.name}"
DEFAULT_BUILD_TARGETS = {
    "HTML": {
        "builder": "html",
        "downloadable": False,
        "download_format": "",
    },
}
DEFAULT_CLEAN_INTERMEDIATE_FILES_FLAG = True
ARCHIVE_TYPES = ["zip", "tar", "gztar", "bztar", "xztar"]

Version = collections.namedtuple(
    "Version",
    [
        "name",
        "url",
        "version",
        "release",
        "is_released",
        "artefacts",
    ],
)


class VersionInfo:
    def __init__(self, app, context, metadata, current_version_name):
        self.app = app
        self.context = context
        self.metadata = metadata
        self.current_version_name = current_version_name

    def _dict_to_versionobj(self, v):
        return Version(
            name=v["name"],
            url=self.vpathto(v["name"]),
            version=v["version"],
            release=v["release"],
            is_released=v["is_released"],
            artefacts=[
                {"name": name, "url": self.apathto(name, target)}
                for name, target in v["build_targets"].items()
                if self.apathto(name, target) is not None
            ],
        )

    @property
    def tags(self):
        return [
            self._dict_to_versionobj(v)
            for v in self.metadata.values()
            if v["source"] == "tags"
        ]

    @property
    def branches(self):
        return [
            self._dict_to_versionobj(v)
            for v in self.metadata.values()
            if v["source"] != "tags"
        ]

    @property
    def releases(self):
        return [
            self._dict_to_versionobj(v)
            for v in self.metadata.values()
            if v["is_released"]
        ]

    @property
    def in_development(self):
        return [
            self._dict_to_versionobj(v)
            for v in self.metadata.values()
            if not v["is_released"]
        ]

    def __iter__(self):
        yield from self.branches
        yield from sorted(
            self.tags, key=lambda t: ExasolVersion.from_string(t.name), reverse=True
        )

    def __getitem__(self, name):
        v = self.metadata.get(name)
        if v:
            return self._dict_to_versionobj(v)

    def vhasdoc(self, other_version_name):
        if self.current_version_name == other_version_name:
            return True

        other_version = self.metadata[other_version_name]
        return self.context["pagename"] in other_version["docnames"]

    def vpathto(self, other_version_name):
        if self.current_version_name == other_version_name:
            return "{}.html".format(posixpath.split(self.context["pagename"])[-1])

        # Find relative outputdir paths from common output root
        current_version = self.metadata[self.current_version_name]
        other_version = self.metadata[other_version_name]

        current_outputroot = os.path.abspath(current_version["outputdir"])
        other_outputroot = os.path.abspath(other_version["outputdir"])
        outputroot = os.path.commonpath((current_outputroot, other_outputroot))

        current_outputroot = os.path.relpath(current_outputroot, start=outputroot)
        other_outputroot = os.path.relpath(other_outputroot, start=outputroot)

        # Ensure that we use POSIX separators in the path (for the HTML code)
        if os.sep != posixpath.sep:
            current_outputroot = posixpath.join(*os.path.split(current_outputroot))
            other_outputroot = posixpath.join(*os.path.split(other_outputroot))

        # Find relative path to root of other_version's outputdir
        current_outputdir = posixpath.dirname(
            posixpath.join(current_outputroot, self.context["pagename"])
        )
        other_outputdir = posixpath.relpath(other_outputroot, start=current_outputdir)

        if not self.vhasdoc(other_version_name):
            return posixpath.join(other_outputdir, "index.html")

        return posixpath.join(
            other_outputdir, "{}.html".format(self.context["pagename"])
        )

    def apathto(self, build_target_name, build_target):
        """Find the path to the artefact identified by build_target_name
        and build_target.
        """
        current_version = self.metadata[self.current_version_name]
        current_outputroot = os.path.abspath(current_version["outputdir"])
        artefact_dir = posixpath.join(current_outputroot, "artefacts")
        current_outputdir = posixpath.dirname(
            posixpath.join(current_outputroot, self.context["pagename"])
        )

        filename = "{project}_docs-{version}".format(
            project=self.app.config.project.replace(" ", ""),
            version=self.current_version_name.replace("/", "-"),
        )

        if build_target["download_format"] in ARCHIVE_TYPES:
            filename = "{f}-{build_name}.{extension}".format(
                f=filename,
                build_name=build_target_name,
                extension=build_target["download_format"],
            )
        else:
            filename = "{f}.{extension}".format(
                f=filename,
                extension=build_target["download_format"],
            )
        artefact_path = posixpath.relpath(
            posixpath.join(artefact_dir, filename), start=current_outputdir
        )
        return artefact_path


def html_page_context(app, pagename, templatename, context, doctree):
    versioninfo = VersionInfo(
        app, context, app.config.smv_metadata, app.config.smv_current_version
    )
    context["versions"] = versioninfo
    context["vhasdoc"] = versioninfo.vhasdoc
    context["vpathto"] = versioninfo.vpathto

    current = versioninfo[app.config.smv_current_version]
    context["current_version"] = current.name
    context["latest_version"] = versioninfo[app.config.smv_latest_version]
    context["html_theme"] = app.config.html_theme


def config_inited(app, config):
    """Update the Sphinx builder.
    :param sphinx.application.Sphinx app: Sphinx application object.
    """

    if not config.smv_metadata:
        if not config.smv_metadata_path:
            return

        with open(config.smv_metadata_path, encoding="utf-8") as f:
            metadata = json.load(f)

        config.smv_metadata = metadata

    if not config.smv_current_version:
        return

    try:
        data = app.config.smv_metadata[config.smv_current_version]
    except KeyError:
        return

    app.connect("html-page-context", html_page_context)

    # Restore config values
    old_config = sphinx_config.Config.read(data["confdir"])
    old_config.pre_init_values()
    old_config.init_values()
    config.version = data["version"]
    config.release = data["release"]
    config.rst_prolog = data["rst_prolog"]
    config.today = old_config.today
    if not config.today:
        config.today = sphinx_i18n.format_date(
            format=config.today_fmt or _("%b %d, %Y"),
            date=datetime.datetime.strptime(data["creatordate"], DATE_FMT),
            language=config.language,
        )


def setup(app):
    app.add_config_value("smv_metadata", {}, "html")
    app.add_config_value("smv_metadata_path", "", "html")
    app.add_config_value("smv_current_version", "", "html")
    app.add_config_value("smv_latest_version", "main", "html")
    app.add_config_value("smv_tag_whitelist", DEFAULT_TAG_WHITELIST, "html")
    app.add_config_value("smv_branch_whitelist", DEFAULT_BRANCH_WHITELIST, "html")
    app.add_config_value("smv_remote_whitelist", DEFAULT_REMOTE_WHITELIST, "html")
    app.add_config_value("smv_released_pattern", DEFAULT_RELEASED_PATTERN, "html")
    app.add_config_value("smv_outputdir_format", DEFAULT_OUTPUTDIR_FORMAT, "html")
    app.add_config_value("smv_build_targets", DEFAULT_BUILD_TARGETS, "html")
    app.add_config_value(
        "smv_clean_intermediate_files",
        DEFAULT_CLEAN_INTERMEDIATE_FILES_FLAG,
        "html",
    )
    app.connect("config-inited", config_inited)

    return {
        "version": PLUGIN_VERSION,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
