# Changelog

Notable changes to HolyCow's skills. The version is in [`VERSION`](VERSION) and in every skill's `metadata.version`, so an installed copy shows which release it came from.

Versions follow [Semantic Versioning](https://semver.org/), applied to skills:

- **Major:** a skill is removed or renamed, or how it is invoked changes.
- **Minor:** a new skill, or an intended change in what a skill does.
- **Patch:** clarifications and fixes that keep each skill's behavior.

Before 1.0.0, changes that would be major bump the minor version, and everything else bumps the patch.

## [Unreleased]

## [0.1.0] - 2026-11-27

First versioned release: holycow-guide, holycow-init, hc-compass, hc-refine, hc-lab, hc-plan, hc-build, hc-review, hc-pr and hc-retro.

### Added

- `metadata.version` in every skill.
- An eval runner, `evals/run.py`, that runs cases in Claude Code, Codex and Cursor with and without HolyCow, and the four invocation scenarios as runnable cases.

### Changed

- Build and Review batch independent reads, dispatch workers once and wait for them, and tie check evidence to its command, outcome, tested state and environment.
- Retro counts coordinator usage and cache conditions when comparing task costs.
- Compass research tells the Herdr app apart from the original TUI.

### Removed

- The documentation website, now built by the neuralherd.dev repository, and the BossGoat references.

[Unreleased]: https://github.com/NeuralHerd/holycow/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/NeuralHerd/holycow/releases/tag/v0.1.0
