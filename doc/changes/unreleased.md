# Unreleased

## Summary

This major version introduces `matrix.yml` as the new nox session `matrix:generate`.

Projects can extend `BaseConfig` with additional matrix values when they need to expose
more entries to the workflows.

```python
class Config(BaseConfig):
    extra_matrix_value: str = "extra"

    @computed_field  # type: ignore[misc]
    @property
    def computed_matrix_value(self) -> str:
        # This can be requested when generating the matrix. If it is a singular value,
        # like is shown here, then the code will automatically wrap it in an array.
        return f"{self.project_name}-computed"
```

The corresponding nox sessions (`matrix:all`, `matrix:exasol`, and `matrix:python`) will
remain available until September 15, 2026, to provide a transition period for existing projects.

At the same time, the workflows `matrix-all.yml`, `matrix-exasol.yml`, and `matrix-python.yml` 
are deprecated and are no longer maintained by the exasol-toolbox. You can still use 
these workflows in your project until you can transition fully to using `matrix.yml`.

## Feature

* #730: Added support to extend GitHub workflow `cd.yml`
* #864: Modified PTB workflow templates to not persist credentials and to use pinned SHAs
* #654: Added and used general matrix `matrix.yml` for PTB-provided workflows
