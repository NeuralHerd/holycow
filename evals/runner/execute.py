"""Run one case for one agent and arm, grade it and write the result."""

from __future__ import annotations

import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from . import graders, process, workspace
from .cases import ROOT, SKILLS_DIR, skill_names


def arm_problem(arm: str, installed: list, traces: list, known: list):
    """Why the run did not get the skills its arm promises, or None."""
    reported = traces[0].skills_available if traces else None
    if arm == "with" and not installed:
        return "no skills were installed for the with-skill arm"
    if reported is None:
        return None
    if arm == "with" and set(installed) - set(reported):
        return f"agent did not load installed skills {sorted(set(installed) - set(reported))}"
    if arm == "without" and set(known) & set(reported):
        return f"HolyCow skills visible in the without-skill arm: {sorted(set(known) & set(reported))}"
    return None


def run_case(case, adapter, arm: str, run_index: int, out_dir: Path, model: str | None = None,
             judge=None, keep_workspace: bool = False, skills_dir: Path = SKILLS_DIR, root: Path = ROOT) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    known = skill_names(skills_dir)
    started = time.time()
    folder = workspace.create(case.fixture)
    installed = workspace.install_skills(folder, adapter.skill_dir, skills_dir, known) if arm == "with" else []
    traces, steps = [], []
    try:
        for index, step in enumerate(case.steps, 1):
            invoke = step.invoke if arm == "with" else None
            prompt = f"{adapter.invocation(invoke)} {step.prompt}" if invoke else step.prompt
            argv, env = adapter.command(folder, prompt, model)
            step_started = time.time()
            stdout, stderr, code, timed_out = process.run(argv, folder, env, case.timeout_seconds)
            (out_dir / f"step-{index}.events.jsonl").write_text(stdout)
            (out_dir / f"step-{index}.stderr.txt").write_text(stderr)
            trace = adapter.parse(stdout)
            if timed_out:
                trace.error = f"timed out after {case.timeout_seconds}s"
            elif code != 0 and not trace.error:
                trace.error = f"exit code {code}"
            (out_dir / f"step-{index}.final.md").write_text(trace.final_message)
            traces.append(trace)
            steps.append({
                "invocation": adapter.invocation(invoke) if invoke else None,
                "exit_code": code,
                "duration_seconds": round(time.time() - step_started, 1),
                "tool_calls": len(trace.tool_calls),
                "usage": trace.usage,
                "error": trace.error,
            })

        changed, diff = workspace.changes(case.fixture, folder, skip=[adapter.skill_dir] if installed else [])
        (out_dir / "diff.patch").write_text(diff)
        problem = arm_problem(arm, installed, traces, known)
        evidence = graders.Evidence(
            arm=arm, traces=traces, invoked=[step.invoke if arm == "with" else None for step in case.steps],
            prompts=[step.prompt for step in case.steps], diff=diff, changed_files=changed,
            workspace=folder, known_skills=known, judge=judge,
        )
        results = [] if problem else [
            graders.grade(grader, evidence) for grader in case.graders if arm in grader.get("arms", ["with", "without"])
        ]
        errors = [f"step {i}: {trace.error}" for i, trace in enumerate(traces, 1) if trace.error]
        if problem:
            verdict, reason = "invalid", problem
        elif errors:
            verdict, reason = "error", "; ".join(errors)
        else:
            verdict = graders.overall(results)
            reason = "; ".join(f"{r['name']}: {r['detail']}" for r in results if r["verdict"] != "pass")
        commits = workspace.commits_added(folder)
    finally:
        adapter.cleanup(folder)
        if not keep_workspace:
            shutil.rmtree(folder, ignore_errors=True)

    result = {
        "schema_version": 1,
        "case": case.id,
        "scenario": case.scenario,
        "agent": adapter.name,
        "agent_version": adapter.version(),
        "model_requested": model,
        "model_reported": next((trace.model for trace in traces if trace.model), None),
        "arm": arm,
        "run": run_index,
        "skills_version": (root / "VERSION").read_text().strip() if (root / "VERSION").is_file() else None,
        "skills_revision": workspace.skills_revision(root),
        "skills_installed": installed,
        "skills_reported": traces[0].skills_available if traces else None,
        "started_at": datetime.fromtimestamp(started, timezone.utc).isoformat(timespec="seconds"),
        "duration_seconds": round(time.time() - started, 1),
        "workspace": str(folder) if keep_workspace else None,
        "steps": steps,
        "changed_files": changed,
        "commits_added": commits,
        "graders": results,
        "verdict": verdict,
        "reason": reason,
    }
    (out_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    return result
