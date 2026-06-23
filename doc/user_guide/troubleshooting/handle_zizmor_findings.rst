.. _handle_zizmor_findings:

Handling Zizmor Findings
========================

Fixing the Issues
-----------------

`zizmor <https://docs.zizmor.sh/>`__ can automatically fix some findings. The
``--fix`` flag accepts three modes:

* ``--fix=safe`` applies only safe fixes. This is the default.
* ``--fix=unsafe-only`` applies only unsafe fixes, meaning fixes that may be
  correct but require human review because they can affect semantics.
* ``--fix=all`` applies both safe and unsafe fixes.

If a finding does not have a known auto-fix, check the relevant audit
documentation in the `zizmor documentation <https://docs.zizmor.sh/>`__.
That usually makes it clearer whether the issue needs a code change, a
configuration change, or an accepted exception.

Ignoring Accepted Issues
------------------------

When you are first enabling ``workflow:audit``, it can be practical to start with
a broader ``.zizmor.yml`` configuration and then tighten it over time.
However, once a finding is understood, prefer ignoring the specific line that
triggers it instead of adding a broader suppressing rule to ``.zizmor.yml``.
That keeps the exception local and visible during review.

A typical line-level ignore looks like this:

.. code-block:: yaml

    - name: Set up Poetry (${{ inputs.poetry-version }})
      shell: bash
      run: | # zizmor: ignore[github-env] - This shared action is used by many workflows, and downstream steps need `poetry` on PATH; we do not have a safer replacement yet.
        POETRY_VERSION="${INPUTS_POETRY_VERSION}" "$PYTHON_BINARY" "${{ github.action_path }}/ext/get_poetry.py"
        echo "$HOME/.local/bin" >> $GITHUB_PATH

Use configuration rules in ``.zizmor.yml`` only when the finding is genuinely
project-wide. If you add a temporary rule while working through a batch of
findings, remove it again once the repository is clean.
