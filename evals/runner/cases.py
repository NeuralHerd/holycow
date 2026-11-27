"""Load and validate cases in evals/cases/<group>/<slug>/."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASES_DIR = ROOT / "evals" / "cases"
SKILLS_DIR = ROOT / "skills"
ARMS = ("with", "without")
DEFAULT_TIMEOUT_SECONDS = 900

# Required keys for each grader type. Every grader may also set "arms", "step" and "name".
GRADERS = {
    "skills_not_used": {"skills"},
    "skills_used": {"skills"},
    "no_command": {"patterns"},
    "diff_matches": {"patterns"},
    "changed_files": {"exactly"},
    "check_command": {"argv"},
    "judge": {"rubric"},
}
OPTIONAL_GRADER_KEYS = {"type", "arms", "step", "name"}


class CaseError(ValueError):
    """A case is missing or malformed."""


@dataclass(frozen=True)
class Step:
    prompt: str
    invoke: str | None


@dataclass(frozen=True)
class Case:
    id: str
    path: Path
    scenario: str
    steps: tuple
    graders: tuple
    timeout_seconds: int

    @property
    def fixture(self) -> Path:
        return self.path / "fixture"


def skill_names(skills_dir: Path = SKILLS_DIR) -> list:
    return sorted(path.name for path in skills_dir.iterdir() if (path / "SKILL.md").is_file())


def heading_anchor(heading: str) -> str:
    """GitHub-style anchor for a Markdown heading."""
    return re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", heading.strip().lower()))


def list_cases(cases_dir: Path = CASES_DIR) -> list:
    return sorted(path.parent.relative_to(cases_dir).as_posix() for path in cases_dir.glob("*/*/case.json"))


def load_case(case_id: str, cases_dir: Path = CASES_DIR, root: Path = ROOT) -> Case:
    path = cases_dir / case_id
    try:
        data = json.loads((path / "case.json").read_text())
    except FileNotFoundError:
        raise CaseError(f"{case_id}: no case.json") from None
    except json.JSONDecodeError as error:
        raise CaseError(f"{case_id}: case.json is not valid JSON: {error}") from None
    if not isinstance(data, dict):
        raise CaseError(f"{case_id}: case.json must be an object")

    problems = []
    unknown = set(data) - {"scenario", "steps", "graders", "timeout_seconds"}
    if unknown:
        problems.append(f"unknown keys {sorted(unknown)}")
    skills = set(skill_names(root / "skills"))
    scenario = data.get("scenario")
    problems += _scenario_problems(scenario, root)
    steps = _steps(data.get("steps"), path, skills, problems)
    graders = data.get("graders")
    if not isinstance(graders, list) or not graders:
        problems.append("graders must be a non-empty list")
        graders = []
    for index, grader in enumerate(graders, 1):
        problems += [f"grader {index}: {problem}" for problem in _grader_problems(grader, len(steps), skills)]
    timeout = data.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS)
    if not isinstance(timeout, int) or isinstance(timeout, bool) or timeout <= 0:
        problems.append("timeout_seconds must be a positive integer")
    if problems:
        raise CaseError(f"{case_id}: " + "; ".join(problems))
    return Case(case_id, path, scenario, tuple(steps), tuple(graders), timeout)


def _scenario_problems(scenario, root: Path) -> list:
    if not isinstance(scenario, str) or "#" not in scenario:
        return ["scenario must look like evals/<file>.md#<heading-anchor>"]
    file, anchor = scenario.split("#", 1)
    source = root / file
    if not source.is_file():
        return [f"scenario file {file} does not exist"]
    anchors = {heading_anchor(match) for match in re.findall(r"^## (.+)$", source.read_text(), re.M)}
    return [] if anchor in anchors else [f"no '## ' heading in {file} matches #{anchor}"]


def _steps(raw, path: Path, skills: set, problems: list) -> list:
    if not isinstance(raw, list) or not raw:
        problems.append("steps must be a non-empty list")
        return []
    steps = []
    for index, step in enumerate(raw, 1):
        if not isinstance(step, dict) or set(step) != {"prompt", "invoke"}:
            problems.append(f"step {index} must have exactly 'prompt' and 'invoke'")
            continue
        invoke = step["invoke"]
        if invoke is not None and invoke not in skills:
            problems.append(f"step {index} invokes unknown skill {invoke!r}")
        prompt_file = path / str(step["prompt"])
        prompt = prompt_file.read_text().strip() if prompt_file.is_file() else ""
        if not prompt:
            problems.append(f"step {index} prompt file {step['prompt']!r} is missing or empty")
        elif prompt.startswith("-"):
            problems.append(f"step {index} prompt must not start with '-'")
        steps.append(Step(prompt, invoke))
    return steps


def _grader_problems(grader, step_count: int, skills: set) -> list:
    if not isinstance(grader, dict) or grader.get("type") not in GRADERS:
        return [f"type must be one of {sorted(GRADERS)}"]
    required = GRADERS[grader["type"]]
    problems = [f"missing {sorted(required - set(grader))}"] if required - set(grader) else []
    unknown = set(grader) - required - OPTIONAL_GRADER_KEYS
    if unknown:
        problems.append(f"unknown keys {sorted(unknown)}")
    arms = grader.get("arms", list(ARMS))
    if not isinstance(arms, list) or not arms or not set(arms) <= set(ARMS):
        problems.append(f"arms must be a non-empty list drawn from {list(ARMS)}")
    step = grader.get("step", step_count)
    if not isinstance(step, int) or isinstance(step, bool) or not 1 <= step <= max(step_count, 1):
        problems.append(f"step must be between 1 and {step_count}")
    if "skills" in grader:
        named = grader["skills"]
        if named != "*" and (not isinstance(named, list) or not named or not set(named) <= skills):
            problems.append("skills must be '*' or a list of known skill names")
    if "patterns" in grader:
        patterns = grader["patterns"]
        if not isinstance(patterns, list) or not patterns or not all(isinstance(p, str) for p in patterns):
            problems.append("patterns must be a non-empty list of regular expressions")
        else:
            for pattern in patterns:
                try:
                    re.compile(pattern)
                except re.error as error:
                    problems.append(f"bad pattern {pattern!r}: {error}")
    if "exactly" in grader and not (isinstance(grader["exactly"], list) and all(isinstance(f, str) for f in grader["exactly"])):
        problems.append("exactly must be a list of paths")
    if "argv" in grader and not (isinstance(grader["argv"], list) and grader["argv"] and all(isinstance(a, str) for a in grader["argv"])):
        problems.append("argv must be a non-empty list of strings")
    if "rubric" in grader and not (isinstance(grader["rubric"], str) and grader["rubric"].strip()):
        problems.append("rubric must be non-empty text")
    return problems
