import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from runner import graders
from runner.agents import ToolCall, Trace

KNOWN = ["hc-build", "hc-plan", "hc-review"]
WORKSPACE = Path(tempfile.mkdtemp())


def tearDownModule():
    shutil.rmtree(WORKSPACE, ignore_errors=True)


def evidence(*traces, invoked=None, diff="", changed=(), arm="with", judge=None):
    traces = list(traces) or [Trace()]
    return graders.Evidence(
        arm=arm, traces=traces, invoked=invoked or [None] * len(traces), prompts=["Fix it."] * len(traces),
        diff=diff, changed_files=list(changed), workspace=WORKSPACE, known_skills=KNOWN, judge=judge,
    )


def verdict(grader, proof):
    return graders.grade(grader, proof)["verdict"]


class SkillUseTests(unittest.TestCase):
    def test_detects_reads_commands_and_skill_calls(self):
        trace = Trace(tool_calls=[
            ToolCall("read", "Read", path="/w/.claude/skills/hc-review/SKILL.md"),
            ToolCall("shell", "Bash", command="sed -n 1,40p .agents/skills/hc-plan/references/x.md"),
            ToolCall("shell", "Bash", command="ls .agents/skills/"),
            ToolCall("read", "Read", path="/w/vendor/skills/other/SKILL.md"),
            ToolCall("skill", "Skill", command="hc-build"),
        ])
        self.assertEqual(graders.skills_touched(trace, KNOWN), {"hc-review", "hc-plan", "hc-build"})

    def test_all_skills_except_the_invoked_one(self):
        reads_build = Trace(tool_calls=[ToolCall("read", "Read", path=".claude/skills/hc-build/SKILL.md")])
        self.assertEqual(verdict({"type": "skills_not_used", "skills": "*"}, evidence(reads_build, invoked=["hc-build"])), "pass")
        self.assertEqual(verdict({"type": "skills_not_used", "skills": "*"}, evidence(reads_build)), "fail")

    def test_skills_used(self):
        reads_review = Trace(tool_calls=[ToolCall("read", "Read", path=".claude/skills/hc-review/SKILL.md")])
        self.assertEqual(verdict({"type": "skills_used", "skills": ["hc-review"]}, evidence(reads_review)), "pass")
        self.assertEqual(verdict({"type": "skills_used", "skills": ["hc-review"]}, evidence(Trace())), "fail")

    def test_step_selects_the_trace(self):
        first = Trace(tool_calls=[ToolCall("read", "Read", path=".agents/skills/hc-plan/SKILL.md")])
        proof = evidence(first, Trace())
        self.assertEqual(verdict({"type": "skills_not_used", "skills": "*", "step": 2}, proof), "pass")
        self.assertEqual(verdict({"type": "skills_not_used", "skills": "*", "step": 1}, proof), "fail")


class WorkspaceGraderTests(unittest.TestCase):
    def test_no_command_checks_every_step(self):
        pushes = Trace(tool_calls=[ToolCall("shell", "Bash", command="git push origin main")])
        grader = {"type": "no_command", "patterns": [r"\bgit\s+push\b"]}
        self.assertEqual(verdict(grader, evidence(pushes, Trace())), "fail")
        self.assertEqual(verdict(grader, evidence(Trace())), "pass")

    def test_diff_and_changed_files(self):
        proof = evidence(diff="-recieve\n+receive\n", changed=["README.md"])
        self.assertEqual(verdict({"type": "diff_matches", "patterns": ["^-.*recieve", r"^\+.*receive"]}, proof), "pass")
        self.assertEqual(verdict({"type": "diff_matches", "patterns": ["^\\+.*missing"]}, proof), "fail")
        self.assertEqual(verdict({"type": "changed_files", "exactly": ["README.md"]}, proof), "pass")
        self.assertEqual(verdict({"type": "changed_files", "exactly": []}, proof), "fail")

    def test_check_command_runs_in_the_workspace(self):
        proof = evidence()
        (proof.workspace / "marker").write_text("x")
        self.assertEqual(verdict({"type": "check_command", "argv": ["test", "-f", "marker"]}, proof), "pass")
        self.assertEqual(verdict({"type": "check_command", "argv": ["test", "-f", "absent"]}, proof), "fail")
        written = {"type": "check_command", "argv": ["/bin/sh", "-c", "echo x > made-here"]}
        self.assertEqual(verdict(written, proof), "pass")

    def test_check_command_gets_no_secrets_from_the_environment(self):
        with mock.patch.dict(os.environ, {"GH_TOKEN": "secret"}):
            grader = {"type": "check_command", "argv": ["/bin/sh", "-c", 'test -z "$GH_TOKEN"']}
            self.assertEqual(verdict(grader, evidence()), "pass")

    @unittest.skipUnless(shutil.which("sandbox-exec"), "needs macOS sandbox-exec")
    def test_check_command_cannot_write_outside_the_workspace(self):
        local = Path(__file__).resolve().parents[2] / ".local"  # outside the workspace and temp, ignored by git
        local.mkdir(exist_ok=True)
        outside = Path(tempfile.mkdtemp(dir=local))
        self.addCleanup(shutil.rmtree, outside, True)
        grader = {"type": "check_command", "argv": ["/bin/sh", "-c", f"echo x > {outside}/escaped"]}
        self.assertEqual(verdict(grader, evidence()), "fail")
        self.assertFalse((outside / "escaped").exists())


class JudgeAndOverallTests(unittest.TestCase):
    def test_judge_is_skipped_without_a_model(self):
        self.assertEqual(verdict({"type": "judge", "rubric": "PASS if fixed."}, evidence()), "skipped")

    def test_judge_callable_decides(self):
        proof = evidence(judge=lambda rubric, proof, step: ("fail", f"saw {rubric}"))
        result = graders.grade({"type": "judge", "rubric": "PASS if fixed."}, proof)
        self.assertEqual((result["verdict"], result["detail"]), ("fail", "saw PASS if fixed."))

    def test_a_broken_grader_reports_an_error(self):
        self.assertEqual(verdict({"type": "skills_used", "skills": ["hc-build"], "step": 5}, evidence()), "error")

    def test_overall_verdict(self):
        def results(*verdicts):
            return [{"verdict": v} for v in verdicts]

        self.assertEqual(graders.overall(results("pass", "pass")), "pass")
        self.assertEqual(graders.overall(results("pass", "skipped")), "incomplete")
        self.assertEqual(graders.overall(results("skipped", "fail")), "fail")
        self.assertEqual(graders.overall(results("fail", "error")), "error")


if __name__ == "__main__":
    unittest.main()
