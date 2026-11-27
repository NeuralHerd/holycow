"""How to run each agent headless, keep it away from globally installed skills, and read its events.

Observed behavior behind these commands is recorded in docs/maintainers/evals-design.md.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

EVAL_HOMES = Path(os.environ.get("HOLYCOW_EVALS_HOME", str(Path.home() / ".holycow-evals")))
CURSOR_KEY_SERVICE = "holycow-evals-cursor"


class AgentNotReady(RuntimeError):
    """The agent cannot run evals yet, for example because its eval login is missing."""


@dataclass
class ToolCall:
    kind: str  # read, edit, shell, search, skill or other
    name: str
    path: str | None = None
    command: str | None = None


@dataclass
class Trace:
    final_message: str = ""
    tool_calls: list = field(default_factory=list)
    usage: dict | None = None
    model: str | None = None
    # Skills the agent reported at startup. None when the agent does not report them.
    skills_available: list | None = None
    error: str | None = None

    def commands(self) -> list:
        return [call.command for call in self.tool_calls if call.kind == "shell" and call.command]


def clean_env(base: dict | None = None) -> dict:
    """Environment without Claude Code session variables, which change how a nested claude behaves."""
    env = dict(os.environ if base is None else base)
    for key in [key for key in env if key.startswith(("CLAUDE", "ANTHROPIC"))]:
        del env[key]
    return env


def events(text: str):
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


class Adapter:
    name = ""
    executable = ""
    skill_dir = ""

    def invocation(self, skill: str) -> str:
        return f"/{skill}"

    def version(self) -> str:
        try:
            result = subprocess.run([self.executable, "--version"], capture_output=True, text=True, timeout=60)
        except (OSError, subprocess.TimeoutExpired):
            return "unknown"
        output = (result.stdout or result.stderr).strip()
        return output.splitlines()[0] if output else "unknown"

    def preflight(self) -> None:
        if shutil.which(self.executable) is None:
            raise AgentNotReady(f"{self.executable} is not on PATH")

    def command(self, workspace: Path, prompt: str, model: str | None) -> tuple:
        raise NotImplementedError

    def parse(self, text: str) -> Trace:
        raise NotImplementedError

    def cleanup(self, workspace: Path) -> None:
        """Remove anything the agent left outside the workspace for this run."""


class ClaudeAdapter(Adapter):
    name = "claude"
    executable = "claude"
    skill_dir = ".claude/skills"
    # Bash runs in Claude Code's sandbox and is approved automatically; edits are limited to the workspace.
    SETTINGS = json.dumps({"sandbox": {"enabled": True, "autoAllowBashIfSandboxed": True}})

    def command(self, workspace, prompt, model):
        argv = [
            self.executable, "-p", prompt,
            "--output-format", "stream-json", "--verbose", "--no-session-persistence",
            # Project and local settings only: user-level skills, instructions and MCP servers stay out.
            "--setting-sources", "project,local", "--strict-mcp-config",
            "--permission-mode", "acceptEdits", "--settings", self.SETTINGS,
        ]
        if model:
            argv += ["--model", model]
        return argv, clean_env()

    def parse(self, text):
        trace, texts, result_text = Trace(), [], None
        for event in events(text):
            kind = event.get("type")
            if kind == "system" and event.get("subtype") == "init":
                trace.model = event.get("model")
                trace.skills_available = sorted(
                    str(skill.get("name") if isinstance(skill, dict) else skill) for skill in event.get("skills") or []
                )
            elif kind == "assistant":
                for block in (event.get("message") or {}).get("content") or []:
                    if block.get("type") == "tool_use":
                        trace.tool_calls.append(_claude_tool(block.get("name", ""), block.get("input") or {}))
                    elif block.get("type") == "text" and block.get("text"):
                        texts.append(block["text"])
            elif kind == "result":
                trace.usage = dict(event.get("usage") or {}, total_cost_usd=event.get("total_cost_usd"))
                if isinstance(event.get("result"), str):
                    result_text = event["result"]
                if event.get("is_error"):
                    trace.error = f"{event.get('subtype')}: {event.get('result')}"[:500]
        trace.final_message = result_text if result_text else (texts[-1] if texts else "")
        return trace

    def cleanup(self, workspace):
        # Claude Code creates ~/.claude/projects/<workspace>/memory/ even without session persistence.
        for path in {workspace, workspace.resolve()}:
            folder = Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(path))
            if folder.is_dir() and not any(item.is_file() for item in folder.rglob("*")):
                shutil.rmtree(folder, ignore_errors=True)


def _claude_tool(name: str, data: dict) -> ToolCall:
    path = data.get("file_path") or data.get("notebook_path") or data.get("path")
    if name in ("Read", "NotebookRead"):
        return ToolCall("read", name, path=path)
    if name in ("Edit", "MultiEdit", "Write", "NotebookEdit"):
        return ToolCall("edit", name, path=path)
    if name == "Bash":
        return ToolCall("shell", name, command=data.get("command"))
    if name in ("Glob", "Grep"):
        return ToolCall("search", name, path=path, command=data.get("pattern"))
    if name == "Skill":
        return ToolCall("skill", name, command=str(data.get("skill") or data.get("command") or data))
    return ToolCall("other", name, path=path)


class CodexAdapter(Adapter):
    name = "codex"
    executable = "codex"
    skill_dir = ".agents/skills"

    @property
    def home(self) -> Path:
        return EVAL_HOMES / "codex"

    def invocation(self, skill):
        return f"${skill}"

    def _env(self) -> dict:
        # Codex reads skills from $HOME/.agents/skills, so a dedicated HOME keeps global skills out.
        env = clean_env()
        env["HOME"] = str(self.home)
        env.pop("CODEX_HOME", None)
        return env

    def preflight(self):
        super().preflight()
        if not self.home.is_dir():
            raise AgentNotReady(f"create {self.home} and sign in: HOME=\"{self.home}\" codex login")
        status = subprocess.run([self.executable, "login", "status"], env=self._env(), stdin=subprocess.DEVNULL,
                                capture_output=True, text=True, timeout=60)
        reported = (status.stdout + status.stderr).lower()
        if "not logged in" in reported or "logged in" not in reported:
            raise AgentNotReady(f"Codex eval login missing: HOME=\"{self.home}\" codex login")

    def command(self, workspace, prompt, model):
        argv = [
            self.executable, "exec", "--json", "--ephemeral",
            "-s", "workspace-write", "-c", "features.memories=false", "-C", str(workspace),
        ]
        if model:
            argv += ["-m", model]
        return argv + [prompt], self._env()

    def parse(self, text):
        trace, texts = Trace(), []
        for event in events(text):
            kind = event.get("type")
            item = event.get("item") or {}
            if kind == "item.completed":
                item_type = item.get("type")
                if item_type == "agent_message" and item.get("text"):
                    texts.append(item["text"])
                elif item_type == "command_execution":
                    trace.tool_calls.append(ToolCall("shell", "command_execution", command=item.get("command")))
                elif item_type == "file_change":
                    for change in item.get("changes") or []:
                        trace.tool_calls.append(ToolCall("edit", "file_change", path=change.get("path")))
                elif item_type in ("mcp_tool_call", "web_search"):
                    trace.tool_calls.append(ToolCall("other", item_type))
            elif kind == "turn.completed":
                trace.usage = event.get("usage")
            elif kind in ("error", "turn.failed"):
                message = event.get("message") or (event.get("error") or {}).get("message") or kind
                trace.error = str(message)[:500]
        trace.final_message = texts[-1] if texts else ""
        return trace


class CursorAdapter(Adapter):
    name = "cursor"
    executable = "cursor-agent"
    skill_dir = ".cursor/skills"

    @property
    def home(self) -> Path:
        return EVAL_HOMES / "cursor"

    def _key(self) -> str:
        found = subprocess.run(
            ["security", "find-generic-password", "-s", CURSOR_KEY_SERVICE, "-a", os.environ.get("USER", ""), "-w"],
            capture_output=True, text=True,
        )
        if found.returncode != 0 or not found.stdout.strip():
            raise AgentNotReady(
                f"store a Cursor API key: security add-generic-password -s {CURSOR_KEY_SERVICE} -a \"$USER\" -w"
            )
        return found.stdout.strip()

    def preflight(self):
        super().preflight()
        if not self.home.is_dir():
            raise AgentNotReady(f"create {self.home}")
        self._key()

    def command(self, workspace, prompt, model):
        # Cursor reads global skills under $HOME, so it runs with a dedicated HOME and an API key,
        # because its keychain login cannot be saved there.
        env = clean_env()
        env["HOME"] = str(self.home)
        env["CURSOR_API_KEY"] = self._key()
        argv = [
            self.executable, "-p", prompt, "--output-format", "stream-json",
            "--trust", "--force", "--sandbox", "enabled", "--workspace", str(workspace),
        ]
        if model:
            argv += ["--model", model]
        return argv, env

    def parse(self, text):
        trace, texts, result_text = Trace(), [], None
        for event in events(text):
            kind = event.get("type")
            if kind == "system" and event.get("subtype") == "init":
                trace.model = event.get("model")
            elif kind == "assistant":
                for block in (event.get("message") or {}).get("content") or []:
                    if block.get("type") == "text" and block.get("text"):
                        texts.append(block["text"])
            elif kind == "tool_call" and event.get("subtype") == "started":
                trace.tool_calls.append(_cursor_tool(event.get("tool_call") or {}))
            elif kind == "result":
                trace.usage = event.get("usage")
                if isinstance(event.get("result"), str):
                    result_text = event["result"]
                if event.get("is_error"):
                    trace.error = str(event.get("result") or "error")[:500]
        trace.final_message = result_text if result_text else (texts[-1] if texts else "")
        return trace


def _cursor_tool(call: dict) -> ToolCall:
    name = next((key for key in call if key.endswith("ToolCall")), "unknown")
    data = (call.get(name) or {}).get("args") or {}
    path = data.get("path") or data.get("filePath")
    lowered = name.lower()
    if lowered.startswith("read"):
        return ToolCall("read", name, path=path)
    if lowered.startswith("shell"):
        return ToolCall("shell", name, command=data.get("command"))
    if lowered.startswith(("grep", "glob")):
        return ToolCall("search", name, path=path, command=data.get("pattern") or data.get("globPattern"))
    if any(word in lowered for word in ("edit", "write", "delete", "replace")):
        return ToolCall("edit", name, path=path)
    return ToolCall("other", name, path=path)


ADAPTERS = {adapter.name: adapter for adapter in (ClaudeAdapter(), CodexAdapter(), CursorAdapter())}
