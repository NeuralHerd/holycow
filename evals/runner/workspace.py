"""Disposable git workspaces for eval runs."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


def git(workspace: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=workspace, check=True, capture_output=True, text=True).stdout


def create(fixture: Path, parent: Path | None = None) -> Path:
    """Copy the fixture into a new temporary directory and commit it as the starting state."""
    workspace = Path(tempfile.mkdtemp(prefix="holycow-eval-", dir=parent)).resolve()
    if fixture.is_dir():
        shutil.copytree(fixture, workspace, dirs_exist_ok=True)
    git(workspace, "init", "-q", "-b", "main")
    git(workspace, "config", "user.name", "HolyCow Eval")
    git(workspace, "config", "user.email", "eval@holycow.invalid")
    git(workspace, "add", "-A")
    git(workspace, "commit", "-q", "--allow-empty", "-m", "Fixture")
    return workspace


def install_skills(workspace: Path, skill_dir: str, skills_dir: Path, names: list) -> list:
    """Copy skills into the agent's project-level skill folder, hidden from git status and diffs."""
    target = workspace / skill_dir
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        shutil.copytree(skills_dir / name, target / name)
    with (workspace / ".git" / "info" / "exclude").open("a") as exclude:
        exclude.write(f"/{skill_dir}/\n")
    return sorted(names)


def _track_new_files(workspace: Path) -> None:
    git(workspace, "add", "-A", "--intent-to-add")


def changed_files(workspace: Path) -> list:
    """Paths added, changed or deleted since the fixture commit, including untracked files."""
    _track_new_files(workspace)
    return sorted(filter(None, git(workspace, "diff", "HEAD", "--name-only", "--no-renames").splitlines()))


def diff(workspace: Path) -> str:
    _track_new_files(workspace)
    return git(workspace, "diff", "HEAD", "--no-color", "--no-ext-diff", "--no-renames")


def commits_added(workspace: Path) -> int:
    return int(git(workspace, "rev-list", "--count", "HEAD").strip()) - 1


def skills_revision(root: Path) -> dict:
    """The repository commit the skills came from, and whether skills/ had uncommitted changes."""
    try:
        commit = git(root, "rev-parse", "HEAD").strip()
        dirty = bool(git(root, "status", "--porcelain", "--", "skills").strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {"commit": None, "dirty": None}
    return {"commit": commit, "dirty": dirty}
