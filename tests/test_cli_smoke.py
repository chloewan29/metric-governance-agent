from __future__ import annotations

import os
import subprocess
import sys
import tempfile
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


class CliSmokeTest(unittest.TestCase):
    def test_help_lists_readme_commands(self) -> None:
        result = run_cli("--help", cwd=REPO_ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        commands = ("init", "scan", "classify", "workshop", "record", "publish", "check", "prepare", "finalize")
        for command in commands:
            self.assertIn(command, result.stdout)

    def test_prepare_outside_project_explains_next_steps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_cli("prepare", cwd=Path(directory))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("This command must be run inside a metric governance project.", result.stderr)
            self.assertIn("To try the worked example: cd examples/revenue", result.stderr)
            self.assertIn("To start a new project: metricgov init revenue", result.stderr)

    def test_revenue_prepare_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            result = run_cli("init", "revenue", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            (project / "evidence" / "revenue.sql").write_text(
                "select sum(amount) as booked_revenue from sales.orders where close_date is not null",
                encoding="utf-8",
            )
            result = run_cli("prepare", cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            outputs = (
                "artifacts/01_evidence_log.csv",
                "artifacts/02_metric_family_map.md",
                "artifacts/03_ambiguity_register.md",
                "artifacts/04_workshop_pack.md",
            )
            for output in outputs:
                self.assertTrue((project / output).is_file(), output)


if __name__ == "__main__":
    unittest.main()
