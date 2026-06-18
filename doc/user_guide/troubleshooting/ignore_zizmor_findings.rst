.. _ignore_zizmor_findings:

Ignoring Zizmor Findings
========================

`zizmor <https://docs.zizmor.sh/>`__ can automatically fix some findings. The
``--fix`` flag accepts three modes:

* ``--fix=safe`` applies only safe fixes. This is the default.
* ``--fix=unsafe-only`` applies only unsafe fixes, meaning fixes that may be
  correct but require human review because they can affect semantics.
* ``--fix=all`` applies both safe and unsafe fixes.

When you are first enabling ``workflow:audit``, it can be practical to start with
a broader ``.zizmor.yml`` configuration and then tighten it over time.
However, once a finding is understood, prefer ignoring the specific line that
triggers it instead of adding a broader suppressing rule to ``.zizmor.yml``.
That keeps the exception local and visible during review.

A typical line-level ignore looks like this:

.. code-block:: yaml

   secrets: inherit # zizmor: ignore[secrets-inherit] - PTB cannot customize inherited secrets here yet.

Use configuration rules in ``.zizmor.yml`` only when the finding is genuinely
project-wide. If you add a temporary rule while working through a batch of
findings, remove it again once the repository is clean.
