from dataclasses import dataclass

import pytest


@dataclass(frozen=True)
class ExamplePatcherYaml:
    remove_jobs = """
        workflows:
        - name: "checks.yml"
          remove_jobs:
            - build-documentation-and-check-links
        """
    step_customization = """
        workflows:
        - name: "checks.yml"
          step_customizations:
            - action: {action}
              job: run-unit-tests
              step_id: check-out-repository
              content:
                - name: SCM Checkout
                  id: checkout-repo
                  uses: actions/checkout@v6
                  with:
                    fetch-depth: 0
        """


@pytest.fixture(scope="session")
def example_patcher_yaml():
    return ExamplePatcherYaml
