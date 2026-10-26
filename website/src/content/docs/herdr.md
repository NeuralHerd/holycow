# Recommended setup: HolyCow + Herdr

**For coordinating several coding agents, we recommend HolyCow with Herdr and herdr-projects.** This is the setup Anil uses. You can still use HolyCow directly in Claude Code, Codex, or Cursor.

## What each part does

[Herdr](https://herdr.dev) keeps agent terminals organized into workspaces, tabs, and panes, with visible working, idle, and blocked states. It helps when you are juggling several sessions and need to find the one waiting for you.

[herdr-projects](https://github.com/eliasstravik/herdr-projects) adds a work board and a Coordinator. Track tasks, delegate when ready, and follow checks, review, and approval in one place. Delegated tasks run in their own Herdr spaces and Git worktrees.

**HolyCow provides the working method:** clarify decisions, plan, build, and review. Our role instructions tell agents which guidance to read, so you can describe the work without naming a skill every time.

## Install

This walkthrough is for **macOS or Linux**. The board requires Herdr **0.9.3+**, Git, and curl or wget. Install and sign in to the agent CLIs you want to use first. HolyCow's installer also needs Node.js 22.20+. See the [Herdr installation docs](https://herdr.dev/docs/install/) and [board quick start](https://github.com/eliasstravik/herdr-projects/blob/main/docs/get-started.md).

Install Herdr using its official installer, then open it from your project directory:

```sh
curl -fsSL https://herdr.dev/install.sh | sh
herdr --version
cd /path/to/your-project
herdr
```

In a terminal pane **inside Herdr**, install and open the board:

```sh
herdr plugin install eliasstravik/herdr-projects
herdr plugin action invoke open --plugin herdr-projects
```

Accept the board shortcut offered on its first screen. For the commands below, add `export PATH="$HOME/.herdr-projects/data/bin:$PATH"` to your shell's startup file and open a new shell. Then install HolyCow for your agents:

```sh
npx skills@latest add NeuralHerd/holycow -g -a claude-code codex cursor --skill '*'
herdr-projects doctor
```

Keep only the agents you use after `-a`. Reopen their sessions after installation. The [board installation guide](https://github.com/eliasstravik/herdr-projects/blob/main/docs/install.md) covers prerequisites and troubleshooting.

## Anil's setup

As of **22 October 2026**, this is the assignment for each job. These are personal choices, not required models.

| Skill or role | Harness | Model | Effort |
| --- | --- | --- | --- |
| Coordinator and `holycow-guide` | Cursor | Auto | Automatic |
| `hc-plan` | Cursor | Auto | Automatic |
| `hc-compass`, `hc-refine`, `hc-retro` | Codex | GPT-6 Astra | Extra High |
| `holycow-init`: routine setup | Claude Code | Opus 5.5 | Extra High |
| `holycow-init`: deeper investigation | Codex | GPT-6 Astra | Extra High |
| `hc-build` | Claude Code | Opus 5.5 | Extra High |
| `hc-review` | Codex | GPT-6.1 Sol | High |
| `hc-lab`: default | Codex | GPT-6 Astra | Extra High |
| `hc-lab`: explicitly chosen alternative | Claude Code | Opus 5.5 | Extra High |
| `hc-pr` | Cursor | Auto | Automatic |
| Background watcher | Claude Code | Haiku 5.5 | Default |

**Cursor Auto does not pin Grok 4.7.** Cursor chooses the underlying model. Extra High is written as `xhigh` in Codex and Claude settings.

Init uses Astra when the authorized work needs substantial investigation, conflicting conventions resolved, or cross-project context. Routine setup and refreshing known project guidance stay on Claude. Lab uses Astra unless you choose its Opus alternative.

**A skill does not switch the model in an existing chat.** The Coordinator uses this table when handing work to a suitable agent. Moving from discovery to planning, for example, means a handoff from Astra to Cursor with the accepted decisions.

Check what your installed agents accept before copying model choices:

```sh
herdr-projects models claude
herdr-projects models codex
herdr-projects models cursor
```

Use a listed model, or leave off the model suffix to use the agent's default. Model availability depends on your installation and account. See [models and effort](https://github.com/eliasstravik/herdr-projects/blob/main/docs/models.md).

### Copy the role choices

Run only the choices you want. These set personal defaults for board tasks; repo and task overrides can take precedence.

```sh
herdr-projects set coordinator.agent cursor/auto
herdr-projects set coordinator.effort default
herdr-projects set plan.agent cursor/auto
herdr-projects set plan.approve you
herdr-projects set worker.agent claude/claude-opus-5-5
herdr-projects set worker.effort xhigh
herdr-projects set worker.fallback none
herdr-projects set reviewer.agent codex/gpt-6.1-sol
herdr-projects set reviewer.effort high
herdr-projects set reviewer.fallback none
herdr-projects set board.open popup
herdr-projects show
```

Anil's personal default asks for plan approval. Interaction Service overrides `plan.approve` to `none`; its discovery workflow uses a separate ordinary pane, as described below. The commands above leave access permissions unchanged. See the [settings reference](https://github.com/eliasstravik/herdr-projects/blob/main/docs/settings.md).

## Make HolyCow the default inside Herdr

Installation alone does **not** enable automatic selection. We opt in through `coordinator.instructions`, `worker.instructions`, and `reviewer.instructions`. The settings above choose role defaults; the instructions below add the skill assignments. Ordinary panes need explicit model arguments and the same guidance in their handoff.

<details>
<summary>Copy the setup prompt into your board's Coordinator chat</summary>

```text
Enable HolyCow guidance only for software work coordinated through Herdr.
Merge this into coordinator.instructions, worker.instructions, and
reviewer.instructions, preserving my access, approval and review settings:

Read the selected installed SKILL.md and its required references before
that work. Resolve references relative to the skill directory. Retrieve
needed sections if output was truncated; reuse unchanged guidance already
read. Say which guidance you use and disclose missing files.

Coordinator: use holycow-guide to select the smallest useful route, then
use this fixed assignment at each authorized handoff:
- Coordinator, holycow-guide, hc-plan, hc-pr: cursor/auto, effort default.
- hc-compass, hc-refine, hc-retro: codex/gpt-6-astra, effort xhigh.
- holycow-init: claude/claude-opus-5-5, effort xhigh for routine setup;
  codex/gpt-6-astra, effort xhigh for deeper investigation already in scope.
- hc-build: claude/claude-opus-5-5, effort xhigh.
- hc-review: codex/gpt-6.1-sol, effort high.
- hc-lab: codex/gpt-6-astra, effort xhigh; use claude/claude-opus-5-5,
  effort xhigh only when I explicitly choose that alternative.

For a board task, explicitly set worker.agent, worker.effort and
worker.fallback none from the assignment. Verify with show <id> --json.
The optional plan-before-build phase uses plan.agent cursor/auto.
A standalone hc-plan task also needs worker.agent cursor/auto and
worker.effort default. Do not enable a build phase for a planning-only task.
Keep the independent board reviewer on codex/gpt-6.1-sol, effort high,
including plan reviews, which use hc-plan guidance.

For ordinary panes, pass the corresponding native model/effort arguments;
board defaults do not reach them. Reuse a session only when its harness,
model and effort match. Include the skill, repository, accepted context,
current stage, model assignment and stopping boundary in each handoff.
Verify the recorded launch. Report a model mismatch before domain work.
Loading a skill never changes the current chat's model.

Set research.only only for reports with no repository changes. Selecting
Astra does not make a task read-only: maps, decisions, setup and experiments
can need authorized writes.

Worker: follow the handoff; use hc-plan for planning, hc-build for
implementation or debugging, and hc-compass or hc-refine for research.
Also honor explicitly assigned hc-retro, hc-lab, hc-pr and holycow-init.
Reviewer: use hc-review for code and hc-plan for plans. Preserve the
board's verdict format and review-only role.

The board owns the review-and-correction cycle. Workers retain self-checks
but do not launch another independent review before the board's review.
The assigned reviewer performs the review directly and does not recruit
more reviewers. Only the Coordinator assigns an authorized specialist
for a distinct risk or a fresh readiness reader when no plan reviewer
already covers it. Keep small, settled work direct.

Give each authorized worker one outcome, explicit ownership, accepted
constraints, source pointers, check evidence and a stopping boundary.
Fresh reviewers receive the contract, project rules and exact target,
without the author's conversation or conclusions. Return concise findings
and coverage limits. On correction rounds, carry finding identities and
recheck the fixes and affected dependencies; retain unresolved blockers.

Skip routing for greetings, simple facts, status, and board administration.
Do not start agents, add tasks, create worktrees, or publish work merely
because a skill suggests it. Follow my scope and repository instructions.
Keep installed skill files unchanged. Show me the saved settings.
```

</details>

This is Coordinator guidance, not a built-in per-skill router. Check the selected model at handoff and confirm that the receiving agent reads the skill and its references.

<details>
<summary>Exact task settings and ordinary-pane arguments</summary>

For an existing planning task, save its assignment before its next authorized start. This does not start the task:

```sh
herdr-projects set worker.agent cursor/auto --task <id>
herdr-projects set worker.effort default --task <id>
herdr-projects set worker.fallback none --task <id>
herdr-projects show <id>
```

For an Astra task, use `codex/gpt-6-astra` and `xhigh` instead. Keep its output boundary and approval settings separate from its model assignment.

In an ordinary Herdr pane, pass these native arguments after `--` in an authorized `herdr agent start` command:

| Assignment | `--kind` | Native arguments |
| --- | --- | --- |
| Cursor Auto | `cursor` | `--model auto` |
| Astra Extra High | `codex` | `-m gpt-6-astra -c 'model_reasoning_effort="xhigh"'` |
| Sol High | `codex` | `-m gpt-6.1-sol -c 'model_reasoning_effort="high"'` |
| Opus Extra High | `claude` | `--model claude-opus-5-5 --effort xhigh` |

Use a discovered, available pane ID and carry the skill/context in the prompt. Follow the installed Herdr skill; these settings do not authorize another agent or worktree.

`worker.fallback none` removes the configured fallback chain. The board can still retry a rejected model on that harness's default model. Report that mismatch instead of treating it as the requested assignment. See [model refusal behavior](https://github.com/eliasstravik/herdr-projects/blob/main/docs/models.md#a-model-refused-while-the-agent-works).

</details>

## Bound review cost

HolyCow defaults to one independent reviewer for substantial work, with additional specialists only for distinct risks or an explicit request. An existing board plan review also counts as Plan's readiness review. Fresh context still includes accepted decisions and project instructions. Use a fresh agent session where supported; reopening a pane or resuming a chat does not establish isolation. A small task does not need a new board task, worktree, or reviewer group for each check.

For a new review policy, start with one automatic correction cycle followed by a focused recheck. Inspect `herdr-projects show <id> --json` before changing task settings. Existing user and board policy remains authoritative; installing skills does not change it. If approved, `herdr-projects set review.rounds 1 --task <id>` limits automatic send-backs **per reason**, not the total number of reviews. Check worker fallback behavior too: a fallback can continue after rounds are exhausted.

Use an agreed task budget through `limit.tokens` and, when useful, `limit.time`. Token enforcement depends on harness support and is checked at turn boundaries, so a turn can exceed the limit. Verify effective settings and counter support rather than promising a hard cap from instructions. Keep required checks, blocking severity, and merge approval intact. Remaining blockers or missing critical evidence require a decision; a spent budget is not a passing verdict. See the board's [settings and limit semantics](https://github.com/eliasstravik/herdr-projects/blob/main/docs/settings.md).

Measure total task usage, including reviewers and corrections, alongside defects caught and remaining verification. Shorter prompts alone do not demonstrate savings. See [Retro](../../../../skills/hc-retro/SKILL.md) for evidence-based comparisons.

## Apply the changes to a fresh session

**Closing and reopening Herdr can restore the old agent and model.** After saving the settings, start a fresh Coordinator from a terminal inside Herdr:

```sh
herdr-projects coordinator new
```

This replaces the Coordinator chat using the saved defaults. Save any handoff context you need first. `coordinator restart` resumes the old conversation and its saved model; use `new` to adopt the new assignment. A project Coordinator is separate: use `herdr-projects coordinator --project <repo> new` for it.

Anil also has **Ctrl+B, then Shift+Y** bound to a fresh Coordinator. **Ctrl+B, then Y** opens the existing one. Existing task agents keep their current model until a new run; check task overrides before resuming work.

<details>
<summary>Optional Herdr shortcut for a fresh Coordinator</summary>

Add an unused shortcut to `~/.config/herdr/config.toml`:

```toml
[[keys.command]]
key = "prefix+shift+y"
type = "shell"
command = 'exec "$HOME/.herdr-projects/data/bin/herdr-projects" coordinator new'
description = "Start a fresh Coordinator with current defaults"
```

Use your configured prefix if it differs from Ctrl+B. Reload Herdr's configuration from inside Herdr with `herdr server reload-config` to register the shortcut in an already-running server.

</details>

## Example: Interaction Service

Anil's workflow starts with `holycow-init`, which records repository context in `docs/agents/holycow.md`. The Coordinator hands discovery to an ordinary Codex pane in the original checkout. Compass keeps the open questions and accepted decisions in `.hc/compass/interaction-service/map.md`; Refine presents recommendations, alternatives, and trade-offs.

A prompt after the defaults are configured:

```text
Continue discovery for Interaction Service in our existing research pane.
Reuse docs/agents/holycow.md and the current Compass map. Resolve the next
open decision with recommended options and trade-offs. Stay in discovery;
do not create a board task or start implementation.
```

The Coordinator routes the work; the research agent applies Compass and Refine. When accepted decisions are ready for delivery, Plan prepares the work, Build implements it, and Review checks it. **Board delegation creates a worktree**, so request it only when that is the workflow you want. For work in the original checkout, continue in an ordinary Herdr pane.

## Keep it current

Use `herdr update` for Herdr's installer-managed version, or your package manager for its installation. Update the board with `herdr-projects update` and follow [HolyCow's update instructions](../../../../README.md#update). Ask ongoing agents to re-read changed guidance, or start a fresh session with the accepted context.
