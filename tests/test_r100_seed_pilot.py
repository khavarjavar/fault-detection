"""Check unattended stage handling with tiny processes, without training."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_r100_seed_pilot import execute_steps


class SeedPilotTests(unittest.TestCase):
    def test_success_records_all_stages(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            state = execute_steps(directory, [
                {"name": "first", "command": [sys.executable, "-c", "print('first')"]},
                {"name": "second", "command": [sys.executable, "-c", "print('second')"]},
            ], directory)
            self.assertEqual(state["status"], "steps_complete")
            self.assertEqual(state["completed_steps"], ["first", "second"])
            self.assertIsNone(state["active_child_pid"])
            self.assertFalse(state["test_files_opened"])

    def test_failure_does_not_launch_next_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            sentinel = directory / "must_not_exist"
            with self.assertRaisesRegex(RuntimeError, "exit code 7"):
                execute_steps(directory, [
                    {"name": "failed", "command": [sys.executable, "-c", "raise SystemExit(7)"]},
                    {"name": "forbidden", "command": [sys.executable, "-c",
                        "from pathlib import Path; import sys; Path(sys.argv[1]).touch()", str(sentinel)]},
                ], directory)
            self.assertFalse(sentinel.exists())
            self.assertFalse((directory / "pipeline_forbidden.log").exists())
            state = json.loads((directory / "pipeline_state.json").read_text())
            self.assertEqual(state["status"], "failed")
            self.assertEqual(state["completed_steps"], [])
            self.assertEqual(state["last_exit_code"], 7)


if __name__ == "__main__":
    unittest.main()
