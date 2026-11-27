import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from runner import judge
from runner.agents import ToolCall, Trace
from runner.graders import Evidence


def proof(diff="+fixed\n"):
    trace = Trace(final_message="I fixed it.", tool_calls=[ToolCall("shell", "Bash", command="python3 -m unittest")])
    return Evidence(arm="with", traces=[trace], invoked=["hc-build"], prompts=["Fix the bug."], diff=diff,
                    changed_files=["a.py"], workspace=Path(tempfile.gettempdir()), known_skills=["hc-build"])


def reply(text, code=0):
    return subprocess.CompletedProcess([], code, stdout=json.dumps({"result": text}), stderr="")


class ParseVerdictTests(unittest.TestCase):
    def test_reads_the_last_verdict_object(self):
        output = json.dumps({"result": 'Thinking {"verdict": "pass", "reason": "a"}\n{"verdict": "fail", "reason": "b"}'})
        self.assertEqual(judge.parse_verdict(output), ("fail", "b"))

    def test_unusable_output_is_an_error(self):
        self.assertEqual(judge.parse_verdict("oops")[0], "error")
        self.assertEqual(judge.parse_verdict(json.dumps({"result": "no verdict here"}))[0], "error")
        self.assertEqual(judge.parse_verdict(json.dumps({"result": '{"verdict": "maybe"}'}))[0], "error")


class MakeJudgeTests(unittest.TestCase):
    def test_sends_evidence_without_the_arm_and_returns_the_verdict(self):
        calls = []

        def run(argv, **kwargs):
            calls.append((argv, kwargs))
            return reply('{"verdict": "pass", "reason": "Fixed with a test."}')

        result = judge.make_judge("claude-test", run=run)("PASS if fixed.", proof(), 0)
        self.assertEqual(result, ("pass", "Fixed with a test."))
        argv, kwargs = calls[0]
        self.assertEqual(argv[argv.index("--model") + 1], "claude-test")
        sent = kwargs["input"]
        for expected in ("PASS if fixed.", "Fix the bug.", "python3 -m unittest", "I fixed it.", "+fixed"):
            self.assertIn(expected, sent)
        self.assertNotIn("hc-build", sent)
        self.assertNotIn("with-skill", sent)

    def test_failures_are_errors_not_verdicts(self):
        failing = judge.make_judge("m", run=lambda argv, **kwargs: reply("", code=1))
        self.assertEqual(failing("r", proof(), 0)[0], "error")

        def slow(argv, **kwargs):
            raise subprocess.TimeoutExpired(argv, 1)

        self.assertEqual(judge.make_judge("m", run=slow)("r", proof(), 0)[0], "error")

    def test_long_evidence_is_clipped(self):
        sent = judge.build_prompt("r", proof(diff="x" * (judge.LIMIT + 10)), 0)
        self.assertIn("[truncated]", sent)


if __name__ == "__main__":
    unittest.main()
