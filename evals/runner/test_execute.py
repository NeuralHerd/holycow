"""End-to-end runs with a fake agent that speaks Codex's event format."""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from runner.agents import CodexAdapter, Trace
from runner.cases import Case, Step, load_case, skill_names
from runner.execute import arm_problem, run_case

FAKE_AGENT = r"""
import json, pathlib, sys, time
prompt, mode = sys.argv[1], sys.argv[2]
def emit(event):
    print(json.dumps(event), flush=True)
if mode == "sleep":
    time.sleep(30)
if mode == "crash":
    sys.exit(3)
if mode == "peek":
    emit({"type": "item.completed", "item": {"type": "command_execution", "command": "cat .agents/skills/hc-plan/SKILL.md"}})
readme = pathlib.Path("README.md")
readme.write_text(readme.read_text().replace("recieve", "receive"))
emit({"type": "item.completed", "item": {"type": "file_change", "changes": [{"path": "README.md", "kind": "update"}]}})
emit({"type": "item.completed", "item": {"type": "agent_message", "text": "Fixed: " + prompt}})
emit({"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 2}})
"""


class FakeAgent(CodexAdapter):
    name = "fake"

    def __init__(self, mode="fix"):
        self.mode = mode

    def command(self, workspace, prompt, model):
        return [sys.executable, "-c", FAKE_AGENT, prompt, self.mode], {}

    def version(self):
        return "fake 1.0"


class RunCaseTests(unittest.TestCase):
    def setUp(self):
        self.out = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.out, True)
        self.case = load_case("invocation/ordinary-request")

    def run_fake(self, mode="fix", arm="with", case=None):
        return run_case(case or self.case, FakeAgent(mode), arm, 1, self.out / arm)

    def test_passing_run_writes_its_result_and_removes_the_workspace(self):
        result = self.run_fake()
        self.assertEqual(result["verdict"], "pass", result["reason"])
        self.assertEqual(result["skills_installed"], skill_names())
        self.assertEqual(result["changed_files"], ["README.md"])
        self.assertEqual(result["agent_version"], "fake 1.0")
        self.assertEqual(result["skills_version"], (Path(__file__).resolve().parents[2] / "VERSION").read_text().strip())
        self.assertEqual(json.loads((self.out / "with" / "result.json").read_text())["verdict"], "pass")
        self.assertIn("+", (self.out / "with" / "diff.patch").read_text())
        self.assertIsNone(result["workspace"])

    def test_keep_workspace_leaves_it_for_inspection(self):
        result = run_case(self.case, FakeAgent(), "with", 1, self.out / "kept", keep_workspace=True)
        kept = Path(result["workspace"])
        self.addCleanup(shutil.rmtree, kept, True)
        self.assertIn("receive", (kept / "README.md").read_text())

    def test_without_arm_installs_nothing(self):
        result = self.run_fake(arm="without")
        self.assertEqual(result["skills_installed"], [])
        self.assertEqual(result["verdict"], "pass", result["reason"])

    def test_reading_a_skill_in_an_ordinary_request_fails(self):
        result = self.run_fake(mode="peek")
        self.assertEqual(result["verdict"], "fail")
        self.assertIn("hc-plan", result["reason"])

    def test_agent_crash_and_timeout_are_errors(self):
        self.assertEqual(self.run_fake(mode="crash")["verdict"], "error")
        quick = Case("invocation/ordinary-request", self.case.path, self.case.scenario,
                     (Step("Fix the typo in this README.", None),), self.case.graders, timeout_seconds=1)
        result = self.run_fake(mode="sleep", case=quick)
        self.assertEqual(result["verdict"], "error")
        self.assertIn("timed out", result["reason"])

    def test_invoked_steps_get_the_agent_invocation(self):
        explicit = Case(self.case.id, self.case.path, self.case.scenario,
                        (Step("Fix the typo in this README.", "hc-build"),), self.case.graders, 60)
        result = self.run_fake(case=explicit)
        self.assertEqual(result["steps"][0]["invocation"], "$hc-build")
        self.assertIn("Fixed: $hc-build Fix the typo", (self.out / "with" / "step-1.final.md").read_text())


class ArmProblemTests(unittest.TestCase):
    def test_reported_skills_must_match_the_arm(self):
        known = ["hc-build", "hc-review"]
        self.assertIsNone(arm_problem("with", known, [Trace(skills_available=known + ["other"])], known))
        self.assertIn("did not load", arm_problem("with", known, [Trace(skills_available=["hc-build"])], known))
        self.assertIn("visible", arm_problem("without", [], [Trace(skills_available=["hc-review"])], known))
        self.assertIsNone(arm_problem("without", [], [Trace()], known))
        self.assertIn("no skills", arm_problem("with", [], [Trace()], known))


if __name__ == "__main__":
    unittest.main()
