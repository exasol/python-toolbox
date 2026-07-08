from inspect import cleandoc

import pytest

from exasol.toolbox.util.workflows.custom_workflow_extractor import (
    CustomWorkflowEntry,
    CustomWorkflowExtractor,
)


@pytest.fixture
def workflow_directory(tmp_path):
    workflow_directory = tmp_path / ".github" / "workflows"
    workflow_directory.mkdir(parents=True)
    return workflow_directory


@pytest.fixture
def custom_workflow_extractor(workflow_directory):
    return CustomWorkflowExtractor(
        github_workflow_directory=workflow_directory,
        sonar_token_name="SONAR_TOKEN",
    )


class TestCustomWorkflowEntry:
    @staticmethod
    def test_secrets_are_normalized_on_creation():
        custom_workflow_entry = CustomWorkflowEntry(
            exists=True,
            secrets=("ZETA_SECRET", "ALPHA_SECRET", "ALPHA_SECRET"),
        )

        assert custom_workflow_entry == CustomWorkflowEntry(
            exists=True,
            secrets=("ALPHA_SECRET", "ZETA_SECRET"),
        )


class TestBuildCustomWorkflowEntry:
    @staticmethod
    def test_file_does_not_exist(custom_workflow_extractor):
        custom_workflow_entry = custom_workflow_extractor._build_custom_workflow_entry(
            workflow="slow-checks"
        )

        assert custom_workflow_entry == CustomWorkflowEntry(
            exists=False,
            secrets=(),
        )

    @staticmethod
    def test_file_does_not_contain_secrets(
        custom_workflow_extractor, workflow_directory
    ):
        workflow = "slow-checks"
        workflow_path = workflow_directory / f"{workflow}.yml"
        workflow_path.write_text(cleandoc("""
            name: Slow-Checks

            on:
              workflow_call:
        """))

        custom_workflow_entry = custom_workflow_extractor._build_custom_workflow_entry(
            workflow=workflow
        )

        assert custom_workflow_entry == CustomWorkflowEntry(
            exists=True,
            secrets=(),
        )

    @staticmethod
    def test_file_contains_secret(custom_workflow_extractor, workflow_directory):
        workflow = "slow-checks"
        workflow_path = workflow_directory / f"{workflow}.yml"
        workflow_path.write_text(cleandoc("""
                name: Slow-Checks

                on:
                  workflow_call:
                    secrets:
                      SLOW_CHECK_SECRET:
                        required: true
                """))

        custom_workflow_entry = custom_workflow_extractor._build_custom_workflow_entry(
            workflow=workflow
        )

        assert custom_workflow_entry == CustomWorkflowEntry(
            exists=True,
            secrets=("SLOW_CHECK_SECRET",),
        )


class TestBuildMergeGateEntry:
    @staticmethod
    def test_build_merge_gate_entry(custom_workflow_extractor):
        custom_workflows_dict = {
            "merge-gate-extension": CustomWorkflowEntry(
                exists=True,
                secrets=("EXT_SECRET",),
            ),
            "slow-checks": CustomWorkflowEntry(
                exists=True,
                secrets=("SLOW_SECRET",),
            ),
        }

        merge_gate_entry = custom_workflow_extractor._build_merge_gate_entry(
            custom_workflows_dict
        )

        assert merge_gate_entry == CustomWorkflowEntry(
            exists=True,
            secrets=("EXT_SECRET", "SLOW_SECRET", "SONAR_TOKEN"),
        )


class TestBuildCustomWorkflowDict:
    default_custom_workflow_dict = {
        "cd-extension": CustomWorkflowEntry(exists=False, secrets=()),
        "fast-tests-extension": CustomWorkflowEntry(exists=False, secrets=()),
        "merge-gate-extension": CustomWorkflowEntry(exists=False, secrets=()),
        "slow-checks": CustomWorkflowEntry(exists=False, secrets=()),
        "merge-gate": CustomWorkflowEntry(exists=True, secrets=("SONAR_TOKEN",)),
    }

    def test_no_custom_workflows_exist(self, custom_workflow_extractor):
        custom_workflow_dict = custom_workflow_extractor.build_custom_workflow_dict()

        assert custom_workflow_dict == self.default_custom_workflow_dict

    @pytest.mark.parametrize(
        "workflow",
        (
            "cd-extension",
            "fast-tests-extension",
            "merge-gate-extension",
            "slow-checks",
        ),
    )
    def test_custom_workflow_written_to(
        self,
        custom_workflow_extractor,
        workflow_directory,
        workflow,
    ):
        secret = f"{workflow.upper()}_SECRET"
        workflow_path = workflow_directory / f"{workflow}.yml"
        workflow_path.write_text(cleandoc(f"""
                name: {workflow}

                on:
                  workflow_call:
                    secrets:
                      {secret}:
                        required: true
                """))

        custom_workflow_dict = custom_workflow_extractor.build_custom_workflow_dict()

        expected_custom_workflow_dict = self.default_custom_workflow_dict.copy()
        expected_custom_workflow_dict[workflow] = CustomWorkflowEntry(
            exists=True,
            secrets=(secret,),
        )
        if workflow in ("merge-gate-extension", "slow-checks"):
            expected_custom_workflow_dict["merge-gate"] = CustomWorkflowEntry(
                exists=True,
                secrets=(
                    secret,
                    "SONAR_TOKEN",
                ),
            )

        assert custom_workflow_dict == expected_custom_workflow_dict
