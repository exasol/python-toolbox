# Metrics Schema

This project contains a small script to generate the JSON schema for Exasol metrics.
It has been intentionally separated and should not be used as a dependency.
Its sole purpose is to generate the schema for the metrics statistics.

## How to Generate a Schema

**Note:** Ensure that the script is run from the directory where this README is located.

### 1. Create a new poetry shell

```shell
poetry shell
```

### 2. Install all necessary dependencies

```shell
poetry install
```

### 3. Generate the schema

**Note:** Please make sure to replace `MAJOR`, `MINOR` and `PATCH` with the appropriate version numbers.

```shell
python metrics_schema.py > metrics-MAJOR-MINOR-PATCH.json
```
