"""Check that failures and the time limit stop only the pilot child."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_paper_attention3d_pilot as supervisor

REAL_POPEN = subprocess.Popen
REAL_SLEEP = time.sleep


class SupervisorTests(unittest.TestCase):
    def execute_trial(self, program, expired):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            (run / "launch_plan.json").write_text(json.dumps({"source_sha256": {}}))
            children = []
            def launch(*args, **kwargs):
                process = REAL_POPEN([sys.executable, "-c", program], **kwargs)
                children.append(process)
                return process
            def now():
                now.calls += 1
                return 0 if now.calls == 1 else 14401
            now.calls = 0
            with patch.object(supervisor, "RUN", run), \
                 patch.object(supervisor, "seed_snapshot", return_value={"unchanged": True}), \
                 patch.object(supervisor.subprocess, "Popen", side_effect=launch), \
                 patch.object(supervisor.time, "sleep", side_effect=lambda seconds: REAL_SLEEP(0.01)):
                if expired:
                    with patch.object(supervisor.time, "monotonic", side_effect=now):
                        supervisor.main()
                else:
                    supervisor.main()
            state = json.loads((run / "supervisor_state.json").read_text())
            self.assertIsNotNone(children[0].poll())
            self.assertFalse((run / "report.md").exists())
            return state

    def test_hard_limit_terminates_child_and_preserves_unrelated_process(self):
        unrelated = REAL_POPEN([sys.executable, "-c", "import time; time.sleep(60)"])
        try:
            state = self.execute_trial("import time; time.sleep(60)", expired=True)
            self.assertEqual(state["status"], "hard_budget_stopped")
            self.assertNotEqual(state["returncode"], 0)
            self.assertIsNone(unrelated.poll())
        finally:
            unrelated.terminate()
            unrelated.wait(timeout=5)

    def test_failed_child_does_not_produce_completed_report(self):
        state = self.execute_trial("raise SystemExit(7)", expired=False)
        self.assertEqual(state["status"], "failed")
        self.assertEqual(state["returncode"], 7)


if __name__ == "__main__":
    unittest.main()
