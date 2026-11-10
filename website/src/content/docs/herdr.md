# Herdr and Shepherdr setup

**Our recommended setup is now [HolyCow + Herdr + BossGoat](bossgoat.md).** BossGoat is NeuralHerd's fork of Shepherdr, with built-in HolyCow skill assignment and per-skill model settings. This guide covers upstream Shepherdr and its optional role instructions. HolyCow also works directly in Claude Code, Codex, or Cursor.

This guide follows **Shepherdr 3.1.12**, with upstream documentation checked on **6 November 2026**. It replaces our older herdr-projects setup. These are documentation checks, not a completed live integration evaluation.

## What each part does

[Herdr](https://herdr.dev) is the app where you see spaces, chats, and terminals. Its agents run in **herdr-core**, so closing the window does not stop their work. The original Herdr TUI is a separate application with its own server.

[Shepherdr](https://github.com/eliasstravik/shepherdr) adds an Assistant for each space, tasks, review, and acceptance. It is a layout and set of add-ons for the Herdr app. The Assistant coordinates through `herdr-task`; workers perform the assigned work.

**HolyCow provides the working method:** clarify decisions, plan, build, and review. The role instructions below tell agents which guidance to read. Installing skills alone does not enable automatic selection.

## Install

This walkthrough is for **macOS or Linux**. Shepherdr 3.1.12 requires the Herdr app **0.1.12+**, herdr-core **0.1.17+**, Python **3.8+**, Git, and a signed-in Claude Code or Codex CLI. Its installer installs Bun if missing. HolyCow's Skills CLI also needs Node.js **22.20+**. See the [Herdr website](https://herdr.dev) and [Shepherdr installation guide](https://github.com/eliasstravik/shepherdr/blob/main/docs/install.md).

Install the Herdr app using its current installer:

```sh
curl -fsSL https://releases.herdr.dev/app/install.sh | sh
herdr-app --version
hc --version
```

Open the Herdr app once so it creates its configuration. Clone Shepherdr into a location you will keep for updates, then inspect the installation before applying it:

```sh
git clone https://github.com/eliasstravik/shepherdr
cd shepherdr
./install.sh --dry-run
```

After reviewing the proposed changes:

```sh
./install.sh
shepherdr doctor
```

The installer adds the layout, helpers, role instructions, and question-card hooks. It backs up replaced files and preserves edited files, placing a new version beside them as `.new`. Inspect those differences rather than overwriting custom instructions. Helpers are linked in `~/.local/bin`; make sure it is on your `PATH`.

In Herdr, **Ctrl+Shift+L** selects the Shepherdr layout. Create a space for your project folder, then install HolyCow for the agents you use:

```sh
npx skills@latest add NeuralHerd/holycow -g -a claude-code codex --skill '*'
```

Keep only your agents after `-a`; add `cursor` if you also use HolyCow in Cursor. Open fresh agent sessions after installation. An install on this machine does not establish that HolyCow is available on another machine; verify the selected skill and references there too.

For a web-only setup, follow [Shepherdr's web instructions](https://github.com/eliasstravik/shepherdr/blob/main/docs/web.md). It has different prerequisites, including Tailscale, and uses `./install.sh --web`.

## Configure roles and task settings

Open **Shepherdr settings → Agents** to choose the Assistant, worker, reviewer, and backup agent. Keep existing choices unless you intend to change them. Select the CLI, model, and effort supported by your installed environment; loading a skill never changes the model in an existing chat.

Settings apply **Everywhere** or to a particular **space**. A space's setting overrides the Everywhere default. Role instructions are shared Everywhere; repository-specific rules belong in that repository's `AGENTS.md` or `CLAUDE.md`. See the [settings reference](https://github.com/eliasstravik/shepherdr/blob/main/docs/settings.md).

Under **Tasks**, inspect **Review**, **Must fix**, **Proof**, **Merge**, and **Worktrees** before starting work. From the project's folder, inspect the effective configuration with:

```sh
herdr-task config --json
```

Each task receives its own Settings block. Inspect an existing task with `herdr-task show <task-id>`; do not assume a settings change rewrites an already-running task's brief. Preserve approval, review, and access settings when adding HolyCow guidance.

### Original checkout or worktree

Git tasks use worktrees by default. Shepherdr also supports working in the original folder with **Tasks → Worktrees** disabled, or an explicitly requested `--here` task. Verify the effective configuration and task's actual folder before editing. Shared-checkout tasks that touch the same files must run sequentially.

Follow the user's repository policy. If it prohibits new worktrees, do not start a default worktree task or change the setting silently. Use an authorized original-folder workflow or continue directly in an ordinary agent session. The [Assistant instructions](https://github.com/eliasstravik/shepherdr/blob/main/templates/assistant.md) explain task creation and ownership.

## Make HolyCow the default inside Shepherdr

Shepherdr installs role instructions at `~/.config/herdr-core/templates/assistant.md`, `worker.md`, and `reviewer.md`. Merge the following guidance into the relevant roles while preserving their existing task protocol. Do not replace the files with this prompt.

<details>
<summary>Copy the setup prompt into a coding-agent chat</summary>

```text
Enable HolyCow guidance only for software work coordinated through Shepherdr.
Read the installed Shepherdr role instructions and current configuration.
Merge the role-specific guidance below into
~/.config/herdr-core/templates/assistant.md, worker.md, and reviewer.md.
Preserve their existing instructions and frontmatter, my model choices,
access permissions, review, merge, proof, worktree and Autopilot settings.

All roles: read the selected installed SKILL.md and its required references
before that work. Resolve references relative to the skill directory.
Retrieve needed sections if output was truncated; reuse unchanged guidance
already read. Disclose missing guidance. Verify availability on the machine
doing the work. Keep installed HolyCow skill files unchanged.

Assistant: use holycow-guide to select the smallest useful route. Use
hc-plan when preparing accepted work for delivery. Keep your coordination
role; do not implement code yourself. Preserve accepted decisions and the
user's current stage instead of restarting discovery. Use the configured
agents; do not silently replace a requested model or effort.

Worker: follow the assigned scope and stopping boundary. Use hc-build for
implementation or debugging, hc-plan for planning, and hc-compass or
hc-refine for discovery. Honor explicitly assigned holycow-init, hc-lab,
hc-retro and hc-pr work without adding an implementation phase.

When the task's Settings block enables review, use Shepherdr's existing
worker-led review protocol with the configured reviewer, model, effort,
Must fix threshold and Review rounds. That reviewer supplies HolyCow's
independent review: do not launch a second review group. Record reviews
against the actual reviewed commit using the task's supplied commands.
Keep required proof and verification evidence. Do not call ready with
blocking findings or an unreviewed final commit when review is required.

Reviewer: use hc-review for code and hc-plan for plans. Preserve
Shepherdr's blocker/major/minor findings format and read-only role.
Read the brief and actual change, report evidence and coverage limits,
and do not recruit other reviewers.

Send bounded handoffs with ownership, accepted constraints, repository and
target state, known source and guidance paths, check evidence, and the
stopping boundary. Fresh reviewers receive the contract and evidence,
without the author's conversation or persuasive conclusions. Dispatch
once; use completion waits and compact status before retrying anything.

Skip routing for greetings, simple facts, status, and task administration.
Follow my authorization and repository instructions. Do not add tasks,
start agents, create worktrees, publish or accept work merely because a
skill suggests it. A ready task is not proof of acceptance or deployment.
Show the changed instruction sections and any unresolved conflicts.
```

</details>

This is role guidance, not a built-in per-skill model router. Ordinary sessions still need the selected skill and accepted context in their prompt. After editing role instructions, start a fresh session with a compact handoff and verify its guidance and model; closing the Herdr window does not restart agents.

## Review and completion

Current Shepherdr has the **worker arrange the configured review**; `herdr-task` does not start a separate board reviewer. The worker records each review against its reviewed commit. HolyCow's self-checks remain useful, but must not create a duplicate independent-review loop. Follow the installed [worker](https://github.com/eliasstravik/shepherdr/blob/main/templates/worker.md) and [reviewer](https://github.com/eliasstravik/shepherdr/blob/main/templates/reviewer.md) instructions.

Use the task's actual **Review rounds** and **Must fix** settings. The old board's per-reason retry semantics and `limit.tokens` / `limit.time` commands are not configuration instructions for Shepherdr 3.x. If rounds are exhausted with blockers or the final commit unreviewed, report the decision needed rather than resetting the cycle or claiming success.

The worker's supplied `herdr-task ready` command can push a worktree branch and open a PR; subsequent merging follows the task's Merge setting. These are delivery actions, not a harmless status update. Match them to the user's authorization, and keep ready, accepted, merged, and deployed distinct. Preserve required proof artifacts and disclose unverified behavior.

Measure Assistant, worker, reviewer, correction, and retry usage together when available. Do not promise a hard token cap from prose instructions. See [Retro](../../../../skills/hc-retro/SKILL.md) for evidence-based comparisons.

## Finish and retire tasks

Workers hand back evidence at their assigned boundary; the Assistant coordinates the remaining lifecycle under the user's authorization. At handoff, name the next owner, current revision or report, checks, unresolved findings, and remaining permissions. Reconcile the task record, review target, PR or report, and requested deployment checks before calling the work done. A human merge outside the task workflow can leave stale status; verify the result before requesting another merge or restarting a worker merely to repeat its closing note.

Archiving hides work; it does not establish completion. Apply the owner's existing archive policy after its completion conditions are verified. If no policy is authorized, propose the choice once through the Assistant. Keep cancelled or unfinished work distinguishable from completed work. Archive permission does not grant merge permission, waive review, or complete an outstanding deployment.

Keep retirement in the task lifecycle, using controls supported by the installed version. Avoid adding a worker task per completion merely to hide another task, or copying an archive reminder into every HolyCow skill.

Before an authorized launch, check prerequisites that can prevent the assigned phase from running: supported planning isolation, usable reviewer access, and any shared browser or fixed-port ownership. Report-only tasks that forbid repository writes also forbid tool-created repository caches. Route a launch or access failure to its owner with the exact failed prerequisite; preserve the selected approval and review gates.

## Anil's setup

The **22 October 2026** model choices below describe the previous setup, not verified Shepherdr 3.x defaults. They remain a reference for standalone HolyCow sessions. The former Cursor Auto Coordinator and background watcher are not automatically migrated to current Shepherdr roles. Choose supported agents in Settings rather than copying old board commands or substituting a model silently.

| Skill or former role | Harness | Model | Effort |
| --- | --- | --- | --- |
| Former Coordinator and `holycow-guide` | Cursor | Auto | Automatic |
| `hc-plan` | Cursor | Auto | Automatic |
| `hc-compass`, `hc-refine`, `hc-retro` | Codex | GPT-6 Astra | Extra High |
| `holycow-init`: routine setup | Claude Code | Opus 5.5 | Extra High |
| `holycow-init`: deeper investigation | Codex | GPT-6 Astra | Extra High |
| `hc-build` | Claude Code | Opus 5.5 | Extra High |
| `hc-review` | Codex | GPT-6.1 Sol | High |
| `hc-lab`: default | Codex | GPT-6 Astra | Extra High |
| `hc-lab`: explicitly chosen alternative | Claude Code | Opus 5.5 | Extra High |
| `hc-pr` | Cursor | Auto | Automatic |
| Former background watcher | Claude Code | Haiku 5.5 | Default |

Model availability depends on the installed CLI and account. Cursor Auto chooses its underlying model. A model preference does not authorize delegation, repository writes, or a different checkout.

## Example: Interaction Service

For discovery in an existing agent session, reuse `docs/agents/holycow.md` and `.hc/compass/interaction-service/map.md`. Keep accepted decisions and the current question rather than restarting setup.

```text
Continue discovery for Interaction Service in this original checkout.
Reuse docs/agents/holycow.md and the current Compass map. Resolve the next
open decision with recommended options and trade-offs. Stay in discovery;
do not create a task, launch another agent, or start implementation.
```

Run this in the discovery agent's chat. For an authorized Shepherdr handoff, give the Assistant the same scope and the chosen checkout mode. When decisions are ready for delivery, Plan prepares the work, Build implements it, and Review checks it.

## Upgrading from the old setup

Herdr TUI / herdr-projects and current Herdr app / Shepherdr are different setups. Do not translate old `herdr-projects` commands by changing only the executable name.

Shepherdr's [upgrade guide](https://github.com/eliasstravik/shepherdr/blob/main/docs/upgrading.md) says 2.0 and 2.1 data does not carry into 3.x. Those versions remain on their own branches; do not pull `main` into a 2.x installation. Preserve old tasks and custom instructions, install the current setup separately, and reconcile what you need before retiring the old one.

## Keep it current

For an existing **3.x** installation, run from the Shepherdr checkout used to install it:

```sh
git pull --ff-only
shepherdr update
shepherdr doctor
```

Review preserved custom files and any `.new` copies after updates. Update the Herdr app through its current distribution instructions and follow [HolyCow's update instructions](../../../../README.md#update). Re-read changed guidance or start a fresh session with accepted context; an app restart alone does not refresh an agent's model or instructions.
