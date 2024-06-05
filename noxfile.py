"""defines nox tasks/targets for this project"""
import nox

# imports all nox task provided by the toolbox
from exasol.toolbox.nox.tasks import *  # pylint: disable=wildcard-import disable=unused-wildcard-import

# default actions to be run if nothing is explicitly specified with the -s option
nox.options.sessions = ["fix"]

# entry point for debugging
def main() -> None:
    """
    This excerpt was taken from nox.__main__.py. Generally, users should invoke Nox using the CLI provided by the Nox package.
    However, when using Nox directly, it spawns a process and therefore, debugging isn't straightforward.
    To cope with this issue, this entry point was added to enable a straightforward way to debug Nox tasks.
    """
    import sys
    from typing import Any

    from nox import (
        _options,
        tasks,
        workflow,
    )
    from nox._version import get_nox_version
    from nox.logger import setup_logging

    def execute_workflow(args: Any) -> int:
        """
        Execute the appropriate tasks.
        """
        return workflow.execute(
            global_config=args,
            workflow=(
                tasks.load_nox_module,
                tasks.merge_noxfile_options,
                tasks.discover_manifest,
                tasks.filter_manifest,
                tasks.honor_list_request,
                tasks.run_manifest,
                tasks.print_summary,
                tasks.create_report,
                tasks.final_reduce,
            ),
        )

    args = _options.options.parse_args()

    if args.help:
        _options.options.print_help()
        return

    if args.version:
        print(get_nox_version(), file=sys.stderr)
        return

    setup_logging(
        color=args.color, verbose=args.verbose, add_timestamp=args.add_timestamp
    )
    exit_code = execute_workflow(args)
    sys.exit(exit_code)


if __name__ == "__main__":  # pragma: no cover
    main()
