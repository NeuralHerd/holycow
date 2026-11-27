"""Grade a run against a written rubric with Claude Code as the judge.

The judge sees the task, a summary of the agent's tool calls, its final reply and the diff. It is not told
which arm the run belongs to.
"""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path

from .agents import ClaudeAdapter, clean_env

LIMIT = 30_000
PROMPT = """You are grading one run of an AI coding agent against a rubric. Judge only what the evidence shows.

## Rubric

{rubric}

## What the user asked

{prompts}

## Tool calls the agent made

{tools}

## The agent's final reply

{reply}

## Changes left in the workspace

{diff}

Reply with only a JSON object: {{"verdict": "pass" or "fail", "reason": "one sentence"}}"""


def _clip(text: str) -> str:
    return text if len(text) <= LIMIT else text[:LIMIT] + "\n[truncated]"


def build_prompt(rubric: str, evidence, step: int) -> str:
    trace = evidence.traces[step]
    tools = "\n".join(
        f"- {call.kind} {call.name}" + (f": {call.command or call.path}" if call.command or call.path else "")
        for call in trace.tool_calls
    )
    prompts = "\n\n".join(f"Message {index}: {prompt}" for index, prompt in enumerate(evidence.prompts[: step + 1], 1))
    return PROMPT.format(
        rubric=rubric.strip(),
        prompts=_clip(prompts),
        tools=_clip(tools or "(none)"),
        reply=_clip(trace.final_message or "(empty)"),
        diff=_clip(evidence.diff or "(none)"),
    )


def parse_verdict(output: str) -> tuple:
    try:
        text = json.loads(output).get("result") or ""
    except (json.JSONDecodeError, AttributeError):
        return "error", "judge output was not JSON"
    matches = re.findall(r"\{[^{}]*\"verdict\"[^{}]*\}", text)
    if not matches:
        return "error", f"no verdict in judge reply: {text[:200]!r}"
    try:
        verdict = json.loads(matches[-1])
    except json.JSONDecodeError:
        return "error", f"unreadable verdict: {matches[-1][:200]!r}"
    if verdict.get("verdict") not in ("pass", "fail"):
        return "error", f"unexpected verdict: {verdict!r}"[:200]
    return verdict["verdict"], str(verdict.get("reason", ""))[:500]


def make_judge(model: str, run=subprocess.run, timeout: int = 300):
    """Return a judge callable for graders.Evidence.judge."""

    def judge(rubric: str, evidence, step: int) -> tuple:
        with tempfile.TemporaryDirectory(prefix="holycow-judge-") as folder:
            argv = [
                "claude", "-p", "--output-format", "json", "--no-session-persistence",
                "--setting-sources", "project", "--strict-mcp-config", "--disable-slash-commands",
                "--max-turns", "1", "--model", model,
            ]
            try:
                result = run(argv, cwd=folder, env=clean_env(), input=build_prompt(rubric, evidence, step),
                             capture_output=True, text=True, timeout=timeout)
            except subprocess.TimeoutExpired:
                return "error", f"judge timed out after {timeout}s"
            finally:
                ClaudeAdapter().cleanup(Path(folder))
        if result.returncode != 0:
            return "error", f"judge exited {result.returncode}: {(result.stderr or result.stdout)[-200:]}"
        return parse_verdict(result.stdout)

    return judge
