"""Run an agent or check command with a hard time limit."""

from __future__ import annotations

import os
import signal
import subprocess

GRACE_SECONDS = 5


def _text(value) -> str:
    if value is None:
        return ""
    return value.decode(errors="replace") if isinstance(value, bytes) else value


def _kill_group(pid: int) -> None:
    try:
        os.killpg(pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


def run(argv: list, cwd, env: dict, timeout: int, grace: int = GRACE_SECONDS) -> tuple:
    """Return (stdout, stderr, exit code or None, timed out).

    The command gets its own process group, which is killed when the command ends or times out, so
    background leftovers stop too. A descendant that starts its own session can escape the group; if it
    keeps the output pipes open after a timeout, reading stops after the grace period instead of waiting.
    """
    process = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        _kill_group(process.pid)
        try:
            stdout, stderr = process.communicate(timeout=grace)
        except subprocess.TimeoutExpired as error:
            stdout, stderr = _text(error.stdout), _text(error.stderr)
            for pipe in (process.stdout, process.stderr):
                pipe.close()
            process.wait()
        return _text(stdout), _text(stderr), None, True
    _kill_group(process.pid)
    return _text(stdout), _text(stderr), process.returncode, False
