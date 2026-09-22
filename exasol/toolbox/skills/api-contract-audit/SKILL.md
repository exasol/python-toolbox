---
name: api-contract-audit
description: Audit a Python library's public API for inconsistencies between type annotations, docstrings, user-facing documentation/examples, and actual runtime behavior. Use when reviewing API changes, checking whether public methods accept undocumented parameter shapes, or validating that docs and type hints match enforcement in code.
---

# API Contract Audit

Use this skill when the task is to review a Python package's public API contract rather than implement features.

Focus on externally visible behavior:
- public functions and methods
- exported classes
- user-facing docs and examples
- runtime validation and coercion

Do not assume the annotation is the source of truth. The goal is to find drift between multiple sources of truth.

## Inputs To Compare

For each relevant public API entrypoint, compare:
- signature and type annotations
- docstring parameter and return descriptions
- examples in docs, README, and example scripts
- runtime behavior in the implementation path

Treat these as separate claims. Report when they disagree.

## What To Look For

Prioritize these mismatch patterns:
- annotation says `str`, but implementation accepts or requires tuple-like schema-qualified identifiers
- annotation says one scalar type, but runtime hard-checks another with `isinstance(...)`
- docstring says a parameter or return type that does not match the signature
- docs/examples call the API with arguments that disagree with the annotation or actual signature
- implementation silently accepts more forms than the public docs mention
- wrappers expose narrower types than the lower-level public method they forward to
- runtime coercion like `int(val)` or `str(val)` that makes the public contract broader than the annotation suggests

Typical search signals:
- `isinstance(`
- `type(`
- `raise ValueError`
- identifier-formatting helpers
- tuple-specific branches
- wrapper methods that pass through parameters unchanged

## Workflow

1. Enumerate the public API surface relevant to the request.
2. Read the implementation of each public method and the immediate downstream code it calls.
3. Trace parameter handling until the real runtime constraint is clear.
4. Cross-check docstrings and user-facing docs/examples.
5. Report only concrete inconsistencies or clearly label residual uncertainty.

Prefer `rg` for discovery. Good starter patterns:

```bash
rg -n "^class |^    def " package_dir
rg -n "isinstance\\(|type\\(|raise ValueError|raise TypeError" package_dir
rg -n "function_name\\(" README.md doc examples test
```

## Output Format

Present findings first, ordered by severity.

For each finding include:
- severity: High, Medium, or Low
- affected API
- what the annotation/doc claims
- what the implementation really does
- file references for both sides of the mismatch

After findings, optionally include:
- open questions where intended behavior is unclear
- a short summary of recurring patterns

If no findings are discovered, say that explicitly and mention any coverage limits.

## Severity Guidance

- High: likely to mislead callers, break type-checked usage, or document the wrong accepted input shape
- Medium: accepted behavior is real but under-documented, or docs/examples contradict each other
- Low: naming, docstring argument labels, stale prose, or smaller clarity issues

## Boundaries

- Do not rewrite the API contract on your own. If code, docs, and examples disagree, report the disagreement.
- Do not stop at the first example. Check for the same pattern across sibling APIs.
- Do not treat private helper inconsistencies as findings unless they affect public behavior.