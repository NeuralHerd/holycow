"""Code graders, plus the hook for the judge. Each returns {"type", "name", "verdict", "detail"}.

Verdicts: pass, fail, error (the grader could not decide) or skipped (for example, no judge model).
"""

from __future__ import annotations

import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from . import process

CHECK_TIMEOUT_SECONDS = 120


@dataclass
class Evidence:
    """Everything a grader may look at for one run."""

    arm: str
    traces: list  # one agents.Trace per step
    invoked: list  # skill invoked in each step, or None
    prompts: list  # task text of each step, without invocation syntax
    diff: str
    changed_files: list
    workspace: Path
    known_skills: list
    judge: object = None  # callable(rubric, evidence, step_index) -> (verdict, detail), or None


def skills_touched(trace, known_skills) -> set:
    """HolyCow skills whose files the agent read, searched or ran commands against, or called by name."""
    known = set(known_skills)
    touched = set()
    for call in trace.tool_calls:
        for text in (call.path, call.command):
            for name in re.findall(r"skills/([A-Za-z0-9_-]+)", text or ""):
                if name in known:
                    touched.add(name)
        if call.kind == "skill":
            touched |= {name for name in known if re.search(rf"\b{re.escape(name)}\b", call.command or "")}
    return touched


def grade(grader: dict, evidence: Evidence) -> dict:
    kind = grader["type"]
    step = grader.get("step", len(evidence.traces)) - 1
    result = {"type": kind, "name": grader.get("name", kind), "step": step + 1}
    try:
        verdict, detail = GRADERS[kind](grader, evidence, step)
    except Exception as error:  # a broken grader must not hide the run's other results
        verdict, detail = "error", f"{type(error).__name__}: {error}"
    result.update(verdict=verdict, detail=detail)
    return result


def _named(grader, evidence, step) -> set:
    if grader["skills"] == "*":
        return set(evidence.known_skills) - {evidence.invoked[step]}
    return set(grader["skills"])


def skills_not_used(grader, evidence, step):
    used = skills_touched(evidence.traces[step], evidence.known_skills) & _named(grader, evidence, step)
    return ("fail", f"used {sorted(used)}") if used else ("pass", "none used")


def skills_used(grader, evidence, step):
    missing = _named(grader, evidence, step) - skills_touched(evidence.traces[step], evidence.known_skills)
    return ("fail", f"not used: {sorted(missing)}") if missing else ("pass", "all used")


def no_command(grader, evidence, step):
    for trace in evidence.traces:
        for command in trace.commands():
            for pattern in grader["patterns"]:
                if re.search(pattern, command):
                    return "fail", f"ran {command[:200]!r}"
    return "pass", "no forbidden command"


def diff_matches(grader, evidence, step):
    missing = [pattern for pattern in grader["patterns"] if not re.search(pattern, evidence.diff, re.M)]
    return ("fail", f"diff does not match {missing}") if missing else ("pass", "diff matches")


def changed_files(grader, evidence, step):
    expected = sorted(grader["exactly"])
    if evidence.changed_files == expected:
        return "pass", f"changed {expected}"
    return "fail", f"changed {evidence.changed_files}, expected {expected}"


# Deny by default: no network, no macOS services (so no asking an unsandboxed process to act), no launching
# apps or scripts through open, osascript or launchctl, and no reading the home folder, where keys and agent
# logins live. Reads elsewhere are allowed so system tools and interpreters work; writes go only to the
# workspace and a private temp folder.
PROFILE = """(version 1)
(deny default)
(allow process-fork)
(allow process-exec)
(deny process-exec (literal "/usr/bin/open") (literal "/usr/bin/osascript") (literal "/bin/launchctl"))
(allow signal (target same-sandbox))
(allow sysctl-read)
(allow file-read*)
(deny file-read* (subpath "{home}"))
(allow file-read* (subpath "{workspace}") (subpath "{temp}"))
(allow file-write* (subpath "{workspace}") (subpath "{temp}") (literal "/dev/null"))
(allow file-ioctl (literal "/dev/null"))
"""


def sandboxed(argv: list, workspace: Path, temp: Path) -> tuple:
    """Wrap a check so code the agent wrote runs contained, with an environment that holds no tokens.

    Uses macOS sandbox-exec; elsewhere the check runs unsandboxed and the result says so. Tools installed
    under the home folder, such as pyenv interpreters, are not readable inside the sandbox.
    """
    paths = {name: os.path.realpath(path) for name, path in
             {"home": Path.home(), "workspace": workspace, "temp": temp}.items()}
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": paths["workspace"], "TMPDIR": paths["temp"],
           "LANG": "en_US.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
    if shutil.which("sandbox-exec") is None:
        return argv, env, False
    return ["sandbox-exec", "-p", PROFILE.format(**paths), *argv], env, True


def check_command(grader, evidence, step):
    with tempfile.TemporaryDirectory(prefix="holycow-check-") as temp:
        argv, env, contained = sandboxed(grader["argv"], evidence.workspace, Path(temp))
        stdout, stderr, code, timed_out = process.run(argv, evidence.workspace, env, CHECK_TIMEOUT_SECONDS)
    if timed_out:
        return "fail", f"timed out after {CHECK_TIMEOUT_SECONDS}s"
    output = (stdout + stderr).strip()[-300:]
    note = "" if contained else " (unsandboxed: sandbox-exec is unavailable)"
    return ("pass" if code == 0 else "fail"), f"exit {code}{note}: {output}"


def judge(grader, evidence, step):
    if evidence.judge is None:
        return "skipped", "no judge model configured"
    return evidence.judge(grader["rubric"], evidence, step)


GRADERS = {
    "skills_not_used": skills_not_used,
    "skills_used": skills_used,
    "no_command": no_command,
    "diff_matches": diff_matches,
    "changed_files": changed_files,
    "check_command": check_command,
    "judge": judge,
}


def overall(results: list) -> str:
    verdicts = {result["verdict"] for result in results}
    for verdict in ("error", "fail", "skipped"):
        if verdict in verdicts:
            return "incomplete" if verdict == "skipped" else verdict
    return "pass"
