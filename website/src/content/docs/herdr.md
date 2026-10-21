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

These are the configured roles as of **21 October 2026**, not a requirement to buy or use these models. The research choice comes from Coordinator instructions; the other model choices come from role settings.

| Job | Agent / model | Configured effort | HolyCow guidance |
| --- | --- | --- | --- |
| Coordination and handoffs | Claude Code / Sonnet 5.5 | Agent default | Guide selects the route |
| Research and open decisions | Codex / GPT-6 Astra | `max` for delegated research | Compass, Refine; Lab when an experiment is authorized |
| Delivery planning | Codex / GPT-6 Astra | No separate planner effort configured | Plan |
| Implementation | Claude Code / Opus 5.5 | `xhigh` | Build and its applicable references |
| Review | Codex / GPT-6.1 Sol | `high` | Review; Plan for a plan review |
| Implementation fallback | Cursor | Agent default; no model pinned | Same task and relevant guidance |

Check what your installed agents accept before copying model choices:

```sh
herdr-projects models claude
herdr-projects models codex
```

Use a listed model, or leave off the model suffix to use the agent's default. Model availability depends on your installation and account. See [models and effort](https://github.com/eliasstravik/herdr-projects/blob/main/docs/models.md).

### Copy the role choices

Run only the choices you want. These set personal defaults for board tasks; repo and task overrides can take precedence.

```sh
herdr-projects set coordinator.agent claude/claude-sonnet-5-5
herdr-projects set plan.agent codex/gpt-6-astra
herdr-projects set plan.approve you
herdr-projects set worker.agent claude/claude-opus-5-5
herdr-projects set worker.effort xhigh
herdr-projects set worker.fallback cursor
herdr-projects set reviewer.agent codex/gpt-6.1-sol
herdr-projects set reviewer.effort high
herdr-projects set board.open popup
herdr-projects show
```

Anil's personal default asks for plan approval. Interaction Service overrides `plan.approve` to `none`; its discovery workflow uses a separate ordinary pane, as described below. The commands above leave access permissions unchanged. See the [settings reference](https://github.com/eliasstravik/herdr-projects/blob/main/docs/settings.md).

## Make HolyCow the default inside Herdr

Installation alone does **not** enable automatic selection. We opt in through `coordinator.instructions`, `worker.instructions`, and `reviewer.instructions` in herdr-projects. Ordinary panes need the same guidance in their handoff.

Paste this into the **board's Coordinator chat** to configure a compact version of our setup:

```text
Enable HolyCow guidance only for software work coordinated through Herdr.
Merge this into coordinator.instructions, worker.instructions, and
reviewer.instructions, preserving my existing role and approval settings:

Read the selected installed SKILL.md and its required references before
that work. Resolve references relative to the skill directory. Retrieve
needed sections if output was truncated; reuse unchanged guidance already
read. Say which guidance you use and disclose missing files.

Coordinator: use holycow-guide to select the smallest useful route.
Keep the assigned roles. Pass the skill name, repository, accepted
context, current stage, and stopping boundary in authorized handoffs,
including handoffs to ordinary panes.
Worker: follow the handoff; use hc-plan for planning, hc-build for
implementation or debugging, and hc-compass or hc-refine for research.
Reviewer: use hc-review for code and hc-plan for plans. Preserve the
board's verdict format and review-only role.

Skip routing for greetings, simple facts, status, and board administration.
Do not start agents, add tasks, create worktrees, or publish work merely
because a skill suggests it. Follow my scope and repository instructions.
Keep installed skill files unchanged. Show me the saved settings.
```

To match Anil's research routing too, add this Coordinator instruction after confirming the model is available: “When I authorize a research-only board task, use `--research --worker.agent codex/gpt-6-astra --worker.effort max`. Use an ordinary pane when I request one.”

This is agent guidance, not a guarantee that every session follows it. Verify the saved instructions with `herdr-projects show`, then check that the receiving agent actually reads the selected skill and relevant references. New role settings apply when the corresponding step starts; include updated guidance explicitly in an ongoing session.

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
