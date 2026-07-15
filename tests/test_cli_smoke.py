from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, "-m", "metricgov.cli", *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def prepare_booked_revenue_project(project: Path) -> subprocess.CompletedProcess[str]:
    result = run_cli("init", "revenue", cwd=project)
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    (project / "evidence" / "revenue.sql").write_text(
        "select sum(amount) as booked_revenue from sales.orders where close_date is not null",
        encoding="utf-8",
    )
    result = run_cli("prepare", cwd=project)
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result


def complete_booked_revenue_yaml(*, owner_confirmed: bool = True, status: str = "Proposed") -> str:
    return textwrap.dedent(
        f"""\
        decisions:
          - metric: Booked Revenue
            status: {status}
            owner: Sales Ops
            owner_confirmed: {str(owner_confirmed).lower()}
            source_of_truth: crm.opportunities
            definition: Value of closed-won opportunities.
            logic_formula: Sum opportunity amount where status is closed-won.
            grain: Opportunity by close month
            time_basis: Close date month
            approved_use: Sales bookings reporting
            not_approved_use: Recognised revenue reporting
            naming_decision: Rename Sales Revenue to Booked Revenue
            related_metrics: [Recognised Revenue]
            caveats: [Bookings are not recognised revenue.]
            review_cadence: Quarterly
        """
    )


class CliSmokeTest(unittest.TestCase):
    def test_help_lists_readme_commands(self) -> None:
        result = run_cli("--help", cwd=REPO_ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        commands = ("demo", "init", "scan", "classify", "workshop", "record", "publish", "change-plan", "check", "prepare", "finalize")
        for command in commands:
            self.assertIn(command, result.stdout)

    def test_prepare_outside_project_explains_next_steps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_cli("prepare", cwd=Path(directory))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("This command must be run inside a metric governance project.", result.stderr)
            self.assertIn("To try the worked example: cd examples/revenue", result.stderr)
            self.assertIn("To start a new project: metricgov init revenue", result.stderr)

    def test_init_prints_guidance_and_preserves_decision_template(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            result = run_cli("init", "revenue", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Add evidence to evidence/.", result.stdout)
            self.assertIn("Next command: metricgov prepare", result.stdout)
            decisions = project / "feedback" / "workshop_decisions.yaml"
            self.assertTrue(decisions.is_file())
            self.assertIn("# decisions:", decisions.read_text(encoding="utf-8"))
            decisions.write_text("# keep this file\n", encoding="utf-8")
            result = run_cli("init", "revenue", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(decisions.read_text(encoding="utf-8"), "# keep this file\n")

    def test_revenue_prepare_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            result = prepare_booked_revenue_project(project)
            self.assertIn("Review artifacts/03_ambiguity_register.md.", result.stdout)
            self.assertIn("Use artifacts/04_workshop_pack.md", result.stdout)
            self.assertIn("Next command: metricgov finalize --from feedback/workshop_decisions.yaml", result.stdout)
            outputs = (
                "artifacts/01_evidence_log.csv",
                "artifacts/02_metric_family_map.md",
                "artifacts/03_ambiguity_register.md",
                "artifacts/04_workshop_pack.md",
            )
            for output in outputs:
                self.assertTrue((project / output).is_file(), output)

    def test_free_text_record_behavior_stays_draft(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            prepare_booked_revenue_project(project)
            notes = project / "feedback" / "workshop_notes.md"
            notes.write_text("Sales Ops discussed the booked revenue definition.", encoding="utf-8")
            result = run_cli("record", "--from", str(notes), cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            mdr = (project / "decisions" / "MDR-001-booked-revenue.md").read_text(encoding="utf-8")
            self.assertIn("TBD — requires owner confirmation.", mdr)
            self.assertIn("Sales Ops discussed the booked revenue definition.", mdr)

    def test_yaml_decision_populates_mdr_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            prepare_booked_revenue_project(project)
            decisions = project / "feedback" / "workshop_decisions.yaml"
            decisions.write_text(complete_booked_revenue_yaml(), encoding="utf-8")
            result = run_cli("record", "--from", str(decisions), cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            mdr = (project / "decisions" / "MDR-001-booked-revenue.md").read_text(encoding="utf-8")
            self.assertIn("## Owner Confirmed\ntrue", mdr)
            self.assertIn("Value of closed-won opportunities.", mdr)
            self.assertIn("Sales bookings reporting", mdr)
            self.assertIn("Rename Sales Revenue to Booked Revenue", mdr)
            result = run_cli("publish", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            catalog = (project / "catalog" / "business_metric_catalog.csv").read_text(encoding="utf-8")
            self.assertIn("Value of closed-won opportunities.", catalog)

    def test_complete_yaml_reduces_governance_failures(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            prepare_booked_revenue_project(project)
            result = run_cli("record", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            before = run_cli("check", cwd=project)
            self.assertIn("Failures: 1", before.stdout)

            decisions = project / "feedback" / "workshop_decisions.yaml"
            decisions.write_text(complete_booked_revenue_yaml(), encoding="utf-8")
            result = run_cli("record", "--from", str(decisions), cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            after = run_cli("check", cwd=project)
            self.assertIn("Failures: 0", after.stdout)

    def test_certification_requires_owner_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            prepare_booked_revenue_project(project)
            decisions = project / "feedback" / "workshop_decisions.yaml"
            decisions.write_text(
                textwrap.dedent("""\
                    decisions:
                      - metric: Booked Revenue
                        status:
                          value: Certified
                          proposed: true
                        owner_confirmed: false
                """),
                encoding="utf-8",
            )
            result = run_cli("record", "--from", str(decisions), cwd=project)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Cannot certify", result.stderr)

    def test_change_plan_creates_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            prepare_booked_revenue_project(project)
            result = run_cli("record", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = run_cli("change-plan", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((project / "artifacts" / "07_dashboard_change_plan.md").is_file())

    def test_confirmed_naming_decision_is_ready_to_rename(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            result = run_cli("init", "revenue", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            (project / "evidence" / "marketing_pipeline.sql").write_text(
                "select sum(amount) as pipeline_revenue from mart.marketing_pipeline",
                encoding="utf-8",
            )
            result = run_cli("prepare", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            decisions = project / "feedback" / "workshop_decisions.yaml"
            decisions.write_text(
                textwrap.dedent("""\
                    decisions:
                      - metric: Pipeline Value
                        status: Proposed
                        owner: Marketing
                        owner_confirmed: true
                        naming_decision: Rename "Pipeline Revenue" to "Pipeline Value"
                """),
                encoding="utf-8",
            )
            result = run_cli("finalize", "--from", str(decisions), cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            plan = (project / "artifacts" / "07_dashboard_change_plan.md").read_text(encoding="utf-8")
            self.assertIn("| Pipeline Revenue | Pipeline Value | marketing_pipeline.sql | sql |", plan)
            self.assertIn("Owner-confirmed naming decision", plan)
            self.assertIn("Ready to rename", plan)

    def test_no_naming_decision_creates_no_action_plan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            prepare_booked_revenue_project(project)
            result = run_cli("record", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = run_cli("change-plan", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("No naming decisions were found", result.stdout)
            plan = (project / "artifacts" / "07_dashboard_change_plan.md").read_text(encoding="utf-8")
            self.assertIn("Naming decisions found: 0", plan)
            self.assertIn("No naming decisions found.", plan)
            self.assertIn("No action", plan)

    def test_demo_revenue_succeeds_from_repo_root(self) -> None:
        result = run_cli("demo", "revenue", cwd=REPO_ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Demo complete", result.stdout)
        self.assertIn("Workflow steps ran: prepare, finalize, change-plan, check", result.stdout)

    def test_demo_unknown_name_has_helpful_error(self) -> None:
        result = run_cli("demo", "churn", cwd=REPO_ROOT)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown demo: churn. Available demos: revenue.", result.stderr)

    def test_demo_outside_repo_root_has_helpful_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_cli("demo", "revenue", cwd=Path(directory))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "Could not find examples/revenue. Run this command from the repository root.",
                result.stderr,
            )

    def test_demo_output_lists_artifacts_and_expected_failures(self) -> None:
        result = run_cli("demo", "revenue", cwd=REPO_ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        expected_paths = (
            "examples/revenue/artifacts/03_ambiguity_register.md",
            "examples/revenue/artifacts/04_workshop_pack.md",
            "examples/revenue/decisions/",
            "examples/revenue/catalog/business_metric_dictionary.md",
            "examples/revenue/artifacts/07_dashboard_change_plan.md",
            "examples/revenue/artifacts/06_governance_check.md",
        )
        for path in expected_paths:
            self.assertIn(path, result.stdout)
        self.assertIn("Governance check failures are expected", result.stdout)
        self.assertIn("one Ready to rename change is owner-confirmed", result.stdout)


if __name__ == "__main__":
    unittest.main()
