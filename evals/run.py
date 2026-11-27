#!/usr/bin/env python3
"""Run HolyCow eval cases against a coding agent, with and without the skills.

Examples:
  python3 evals/run.py --list
  python3 evals/run.py invocation/ordinary-request --agent claude --arm both
  python3 evals/run.py invocation --agent codex --runs 3

Models come from evals/agents.json; --model and --judge-model override them. Results are written under
.local/evals/. See docs/maintainers/evals-design.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from runner.agents import ADAPTERS, AgentNotReady  # noqa: E402
from runner.cases import ARMS, ROOT, CaseError, list_cases, load_case  # noqa: E402
from runner.execute import run_case  # noqa: E402
from runner.judge import make_judge  # noqa: E402

CONFIG = Path(__file__).resolve().parent / "agents.json"


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("cases", nargs="*", help="case IDs such as invocation/ordinary-request, or a group such as invocation")
    parser.add_argument("--list", action="store_true", help="list cases and exit")
    parser.add_argument("--agent", choices=sorted(ADAPTERS), help="agent to run")
    parser.add_argument("--arm", choices=[*ARMS, "both"], default="both", help="with or without HolyCow (default: both)")
    parser.add_argument("--runs", type=int, default=1, help="runs per case and arm (default: 1)")
    parser.add_argument("--model", help="agent model, overriding evals/agents.json")
    parser.add_argument("--judge-model", help="Claude model for judge graders, overriding evals/agents.json")
    parser.add_argument("--allow-default-model", action="store_true",
                        help="run without a pinned agent model; results are not comparable across runs")
    parser.add_argument("--allow-keychain-prompt", action="store_true",
                        help="allow Cursor runs, which currently show a macOS keychain dialog (click Cancel)")
    parser.add_argument("--keep-workspace", action="store_true", help="keep each run's workspace for inspection")
    parser.add_argument("--out", type=Path, help="results folder (default: .local/evals/<timestamp>)")
    return parser.parse_args(argv)


def resolve_cases(names: list) -> list:
    available = list_cases()
    selected = []
    for name in names:
        matches = [case for case in available if case == name or case.startswith(name.rstrip("/") + "/")]
        if not matches:
            raise CaseError(f"no case or group named {name!r}; see --list")
        selected += [case for case in matches if case not in selected]
    return [load_case(case) for case in selected]


def main(argv=None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.list:
        print("\n".join(list_cases()))
        return 0
    if not args.cases or not args.agent:
        print("error: give one or more cases and --agent (or use --list)", file=sys.stderr)
        return 2
    if args.runs < 1:
        print("error: --runs must be at least 1", file=sys.stderr)
        return 2
    if args.agent == "cursor" and not args.allow_keychain_prompt:
        print("error: Cursor runs show a macOS keychain dialog ('A keychain cannot be found to store \"cursor-user\"').\n"
              "Click Cancel if it appears, never Reset To Defaults. Pass --allow-keychain-prompt to run anyway.",
              file=sys.stderr)
        return 2
    config = json.loads(CONFIG.read_text())
    model = args.model or (config.get(args.agent) or {}).get("model")
    if not model and not args.allow_default_model:
        print(f"error: set a model for {args.agent} in {CONFIG.relative_to(ROOT)} or pass --model "
              "(or --allow-default-model for a quick check)", file=sys.stderr)
        return 2
    judge_model = args.judge_model or (config.get("judge") or {}).get("model")
    judge = make_judge(judge_model) if judge_model else None
    try:
        cases = resolve_cases(args.cases)
    except CaseError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    adapter = ADAPTERS[args.agent]
    try:
        adapter.preflight()
    except AgentNotReady as error:
        print(f"error: {args.agent} is not ready: {error}", file=sys.stderr)
        return 2

    out = args.out or ROOT / ".local" / "evals" / datetime.now().strftime("%Y%m%d-%H%M%S")
    arms = ARMS if args.arm == "both" else (args.arm,)
    if not judge_model and any(grader["type"] == "judge" for case in cases for grader in case.graders):
        print("note: no judge model set, so judge graders are skipped and those runs are incomplete", file=sys.stderr)
    tally = {}
    for case in cases:
        for arm in arms:
            for run in range(1, args.runs + 1):
                folder = out / case.id.replace("/", "__") / f"{args.agent}-{arm}-{run}"
                result = run_case(case, adapter, arm, run, folder, model=model, judge=judge,
                                  keep_workspace=args.keep_workspace)
                tally[result["verdict"]] = tally.get(result["verdict"], 0) + 1
                reason = f" ({result['reason']})" if result["reason"] else ""
                print(f"{case.id} {args.agent} {arm} #{run}: {result['verdict']} in {result['duration_seconds']}s{reason}")
    print(f"\n{sum(tally.values())} runs: " + ", ".join(f"{count} {verdict}" for verdict, count in sorted(tally.items())))
    print(f"results: {out}")
    return 0 if set(tally) <= {"pass"} else 1


if __name__ == "__main__":
    sys.exit(main())
