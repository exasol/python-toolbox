.. _developer_agent_skills:

Testing Agent Skills
====================

Packaged Skills
---------------

The ``skills:check`` Nox session validates common structure and content rules
for every packaged skill.

The PTB pytest suite verifies skill packaging and installation with:

* ``test/unit/skills_test.py``: packaging, installation, required files, and
  ``eval_cases.yml`` validation.
* ``test/unit/util/skill_test.py``: lower-level validation and
  installation behavior.
* ``test/integration/project-template/nox_test.py``: verifies that
  ``skills:check`` and ``skills:install`` operate in a newly created project.
* ``test/unit/nox/_skills_test.py``: tests Nox session behavior and failure
  reporting.

When adding a skill to the PTB:

* Add its ``eval_cases.yml`` with representative prompts and expected response
  characteristics.
* Add assertions for any files beyond ``SKILL.md`` that the skill must package
  and install.
* Add deterministic, skill-specific assertions where the shared checks are
  insufficient.

These evaluation files and tests are PTB development resources; they are not
required by downstream projects using the packaged skills.

Writing ``eval_cases.yml``
--------------------------

An evaluation case should describe one distinct user goal. Keep the prompt
specific enough that a good response can be recognized from observable
evidence, and avoid requirements that merely repeat the skill's name or ask
for generic quality.

Use ``must_include`` for concrete evidence that should appear in a correct
response, such as:

* the names of the APIs or files that were inspected;
* the tools or checks that must be used, when they are part of the skill's
  intended behavior; and
* the reported mismatch, affected API, severity, or other required result.

Use ``must_not_include`` for concrete behavior the skill must avoid, such as
inventing findings, treating one source as authoritative without comparison,
or proposing implementation changes when the task asks only for an audit.
The prohibited text should describe an actual failure mode, not a broad word
that could legitimately occur in a response.

For example, a signature and docstring audit can name specific existing
functions in its prompt and require evidence from
``inspect.signature()``, ``inspect.get_annotations()``,
``typing.get_type_hints()``, and ``inspect.getdoc()``. Its ``must_include``
values can then require the inspected function names, the introspection tools,
and the concrete mismatch. This makes the case test the skill's intended
audit behavior instead of only testing whether the response is generally
relevant.

Each case should have a unique ``id``, a meaningful ``category``, a focused
``prompt``, and non-empty ``must_include`` and ``must_not_include`` lists.
Cases should cover different behaviors rather than restating the same prompt
with minor wording changes.
