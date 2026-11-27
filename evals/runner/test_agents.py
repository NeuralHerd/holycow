import json
import os
import re
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from runner import agents
from runner.agents import ClaudeAdapter, CodexAdapter, CursorAdapter


def stream(*events):
    return "\n".join(json.dumps(event) for event in events) + "\nnot json\n"


class ClaudeTests(unittest.TestCase):
    def test_parses_init_tools_reply_and_usage(self):
        trace = ClaudeAdapter().parse(stream(
            {"type": "system", "subtype": "init", "model": "claude-test", "skills": ["hc-review", "hc-build"]},
            {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "name": "Read", "input": {"file_path": "/w/.claude/skills/hc-review/SKILL.md"}},
                {"type": "tool_use", "name": "Bash", "input": {"command": "python3 -m unittest"}},
                {"type": "tool_use", "name": "Edit", "input": {"file_path": "/w/app.py"}},
                {"type": "text", "text": "Working."},
            ]}},
            {"type": "result", "subtype": "success", "is_error": False, "result": "Done.",
             "usage": {"input_tokens": 5, "output_tokens": 2}, "total_cost_usd": 0.01},
        ))
        self.assertEqual(trace.model, "claude-test")
        self.assertEqual(trace.skills_available, ["hc-build", "hc-review"])
        self.assertEqual([(call.kind, call.path or call.command) for call in trace.tool_calls], [
            ("read", "/w/.claude/skills/hc-review/SKILL.md"), ("shell", "python3 -m unittest"), ("edit", "/w/app.py"),
        ])
        self.assertEqual(trace.final_message, "Done.")
        self.assertEqual(trace.usage["total_cost_usd"], 0.01)
        self.assertIsNone(trace.error)

    def test_reports_result_errors(self):
        trace = ClaudeAdapter().parse(stream({"type": "result", "subtype": "error_max_turns", "is_error": True}))
        self.assertIn("error_max_turns", trace.error)

    def test_command_excludes_user_settings_and_session_variables(self):
        with mock.patch.dict(os.environ, {"CLAUDE_CODE_ENTRYPOINT": "x", "ANTHROPIC_MODEL": "y", "KEEP": "1"}):
            argv, env = ClaudeAdapter().command(Path("/w"), "/hc-build Fix it.", "claude-test")
        self.assertEqual(argv[:3], ["claude", "-p", "/hc-build Fix it."])
        self.assertIn("project,local", argv)
        self.assertIn("--strict-mcp-config", argv)
        self.assertEqual(argv[-2:], ["--model", "claude-test"])
        self.assertNotIn("CLAUDE_CODE_ENTRYPOINT", env)
        self.assertNotIn("ANTHROPIC_MODEL", env)
        self.assertEqual(env["KEEP"], "1")
        self.assertNotIn("--model", ClaudeAdapter().command(Path("/w"), "Fix it.", None)[0])

    def test_cleanup_removes_only_empty_project_folders(self):
        home = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, home, True)
        empty, used = Path("/tmp/eval-empty"), Path("/tmp/eval-used")
        projects = home / ".claude" / "projects"
        for path in (empty, used):
            (projects / re.sub(r"[^A-Za-z0-9]", "-", str(path)) / "memory").mkdir(parents=True)
        (projects / "-tmp-eval-used" / "memory" / "note.md").write_text("kept")
        with mock.patch.dict(os.environ, {"HOME": str(home)}):
            ClaudeAdapter().cleanup(empty)
            ClaudeAdapter().cleanup(used)
        self.assertFalse((projects / "-tmp-eval-empty").exists())
        self.assertTrue((projects / "-tmp-eval-used" / "memory" / "note.md").exists())


class CodexTests(unittest.TestCase):
    def test_parses_completed_items_only(self):
        trace = CodexAdapter().parse(stream(
            {"type": "thread.started", "thread_id": "t"},
            {"type": "item.started", "item": {"type": "command_execution", "command": "cat README.md"}},
            {"type": "item.completed", "item": {"type": "command_execution", "command": "cat README.md", "exit_code": 0}},
            {"type": "item.completed", "item": {"type": "file_change", "changes": [{"path": "README.md", "kind": "update"}]}},
            {"type": "item.completed", "item": {"type": "agent_message", "text": "First."}},
            {"type": "item.completed", "item": {"type": "agent_message", "text": "Final."}},
            {"type": "turn.completed", "usage": {"input_tokens": 9, "output_tokens": 3}},
        ))
        self.assertEqual([(call.kind, call.path or call.command) for call in trace.tool_calls],
                         [("shell", "cat README.md"), ("edit", "README.md")])
        self.assertEqual(trace.final_message, "Final.")
        self.assertEqual(trace.usage, {"input_tokens": 9, "output_tokens": 3})
        self.assertIsNone(trace.skills_available)

    def test_reports_failed_turns(self):
        trace = CodexAdapter().parse(stream({"type": "turn.failed", "error": {"message": "quota exceeded"}}))
        self.assertEqual(trace.error, "quota exceeded")

    def test_command_uses_the_eval_home_and_disables_memories(self):
        adapter = CodexAdapter()
        argv, env = adapter.command(Path("/w"), "$hc-build Fix it.", "gpt-test")
        self.assertEqual(adapter.invocation("hc-build"), "$hc-build")
        self.assertEqual(env["HOME"], str(agents.EVAL_HOMES / "codex"))
        self.assertNotIn("CODEX_HOME", env)
        self.assertIn("features.memories=false", argv)
        self.assertEqual(argv[argv.index("-C") + 1], "/w")
        self.assertEqual(argv[-3:], ["-m", "gpt-test", "$hc-build Fix it."])


class CursorTests(unittest.TestCase):
    def test_parses_started_tool_calls_and_result(self):
        trace = CursorAdapter().parse(stream(
            {"type": "system", "subtype": "init", "model": "Auto"},
            {"type": "user", "message": {"role": "user", "content": [{"type": "text", "text": "Fix it."}]}},
            {"type": "tool_call", "subtype": "started", "tool_call": {"readToolCall": {"args": {"path": "/w/.cursor/skills/hc-lab/SKILL.md"}}}},
            {"type": "tool_call", "subtype": "completed", "tool_call": {"readToolCall": {"args": {"path": "/w/x"}}}},
            {"type": "tool_call", "subtype": "started", "tool_call": {"shellToolCall": {"args": {"command": "ls"}}}},
            {"type": "tool_call", "subtype": "started", "tool_call": {"editToolCall": {"args": {"path": "/w/a.py"}}}},
            {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": "Done."}]}},
            {"type": "result", "subtype": "success", "is_error": False, "result": "Done.", "usage": {"inputTokens": 4}},
        ))
        self.assertEqual(trace.model, "Auto")
        self.assertEqual([(call.kind, call.path or call.command) for call in trace.tool_calls],
                         [("read", "/w/.cursor/skills/hc-lab/SKILL.md"), ("shell", "ls"), ("edit", "/w/a.py")])
        self.assertEqual(trace.final_message, "Done.")

    def test_api_key_goes_only_into_the_environment(self):
        with mock.patch.object(CursorAdapter, "_key", return_value="secret-key"):
            argv, env = CursorAdapter().command(Path("/w"), "/hc-build Fix it.", None)
        self.assertEqual(env["CURSOR_API_KEY"], "secret-key")
        self.assertEqual(env["HOME"], str(agents.EVAL_HOMES / "cursor"))
        self.assertNotIn("secret-key", " ".join(argv))
        self.assertIn("--force", argv)


if __name__ == "__main__":
    unittest.main()
