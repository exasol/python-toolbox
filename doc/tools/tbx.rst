tbx
===
The :code:`tbx` is the main entry point for all of the toolbox specific tooling.

.. code-block:: shell

     $ tbx --help

     Usage: tbx [OPTIONS] COMMAND [ARGS]...

    ╭─ Options ───────────────────────────────────────────────────────────────────────────╮
    │ --install-completion          Install completion for the current shell.             │
    │ --show-completion             Show completion for the current shell, to copy it or  │
    │                               customize the installation.                           │
    │ --help                        Show this message and exit.                           │
    ╰─────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ──────────────────────────────────────────────────────────────────────────╮
    │ workflow                                                                            │
    ╰─────────────────────────────────────────────────────────────────────────────────────╯

workflow
--------
The workflow command helps to install and maintain GitHub workflows provided by the toolbox.

.. code-block:: shell

     $ tbx workflow --help

     Usage: tbx workflow [OPTIONS] COMMAND [ARGS]...

    ╭─ Options ───────────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                         │
    ╰─────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ──────────────────────────────────────────────────────────────────────────╮
    │ diff      Diff a specific workflow against the installed one.                       │
    │ install   Installs the requested workflow into the target directory.                │
    │ list      List all available workflows.                                             │
    │ show      Shows a specific workflow.                                                │
    │ update    Similar to install but checks for existing workflows and shows diff       │
    ╰─────────────────────────────────────────────────────────────────────────────────────╯
