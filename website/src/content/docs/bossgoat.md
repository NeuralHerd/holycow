# BossGoat setup with Herdr and HolyCow

**For coordinating several coding agents, we recommend HolyCow + Herdr + BossGoat.** Herdr keeps the agents visible, BossGoat coordinates their tasks, and HolyCow gives each task the guidance it needs. HolyCow also works on its own in Claude Code, Codex, or Cursor.

[BossGoat](https://github.com/NeuralHerd/BossGoat) is NeuralHerd's fork of [Shepherdr](https://github.com/eliasstravik/shepherdr) by Elias Stråvik. It adds Cursor support, usage reporting, and HolyCow skill and model settings. This guide covers BossGoat **3.1.30** as documented on **10 November 2026**.

## How the tools fit together

| Tool | Role |
| --- | --- |
| [Herdr](https://herdr.dev) | The desktop app for spaces, chats, and terminals. Agents run in herdr-core and keep working when the window closes. |
| [BossGoat](https://github.com/NeuralHerd/BossGoat) | A Herdr layout with an Assistant per space, tasks, questions, review, and acceptance. Supports Claude Code, Codex, and Cursor. |
| [HolyCow](../../../../README.md) | Guidance for discovery, planning, implementation, review, and learning. BossGoat assigns a skill to each software task. |

BossGoat retains the `shepherdr` command, `herdr-task` helpers, and Shepherdr storage paths for compatibility. Use the **BossGoat** layout in the app; the command names below are intentional. For upstream Shepherdr, use the separate [Herdr and Shepherdr guide](herdr.md).

## Install

You need macOS or Linux, Herdr app **0.1.12+**, herdr-core **0.1.17+**, Python **3.8+**, Git, and at least one installed and signed-in agent CLI. For Cursor, `cursor-agent` must be on the agent machine's `PATH`. The BossGoat installer adds Bun if missing. Installing HolyCow through the Skills CLI also needs Node.js **22.20+**. See the [BossGoat installation reference](https://github.com/NeuralHerd/BossGoat/blob/main/docs/install.md) and [Cursor guide](https://github.com/NeuralHerd/BossGoat/blob/main/docs/cursor.md).

If Shepherdr is already installed, follow [Move from Shepherdr](#move-from-shepherdr) before applying the BossGoat installation.

Install Herdr using its [current distribution](https://herdr.dev):

```sh
curl -fsSL https://releases.herdr.dev/app/install.sh | sh
herdr-app --version
hc --version
```

Open Herdr once to create its configuration. Keep the BossGoat checkout for future updates:

```sh
git clone https://github.com/NeuralHerd/BossGoat
cd BossGoat
./install.sh --dry-run
```

Review the proposed changes, then install and check:

```sh
./install.sh
shepherdr doctor
```

Make sure `~/.local/bin` is on your `PATH`. In Herdr, press **Ctrl+Shift+L** and select **BossGoat**. Create a space for your project folder with **Ctrl+Shift+N**.

Install HolyCow on **each machine that runs your tasks**:

```sh
npx skills@latest add NeuralHerd/holycow -g -a claude-code codex cursor --skill '*'
```

Keep only the agents you use after `-a`. For a project installation, run from the project folder and omit `-g`. Open fresh agent sessions after installation so they load the skills and hooks.

For browser-only access, follow [BossGoat's web guide](https://github.com/NeuralHerd/BossGoat/blob/main/docs/web.md). That setup uses herdr-core, Bun, and Tailscale with `./install.sh --web`.

## Configure HolyCow

Open **BossGoat settings → HolyCow**. **Skill assignment** is **Required for software tasks**: the Assistant uses HolyCow Guide to choose the relevant skill. There is no mandatory sequence, and greetings or routine status questions can stay in the Assistant chat.

Each of the ten skills has its own agent and model picker, with the selected CLI's supported reasoning, speed, and permission options. Settings apply **Everywhere** or to one **space**; a space's choice overrides the default. Preserve your existing choices unless you intend to change them.

- **Guide** inherits the Assistant role when unset. Its picker controls delegated Guide tasks, not the running Assistant.
- **Review** inherits the Reviewer role when unset and runs read-only.
- **The other skills** inherit the Workers role when unset.

Use **Use role defaults** to remove a global skill override or **Reset to inherited settings** for a space. Explicit task agent and model overrides take priority over a skill's settings. Changed skill settings apply to new launches; running sessions and already-queued commands retain their choice. See [BossGoat's HolyCow settings](https://github.com/NeuralHerd/BossGoat/blob/main/docs/settings.md#holycow).

BossGoat checks the skill assignment and installed instructions before launching software tasks. A missing skill stops the launch with installation guidance. Install the skill on the machine doing the work; a successful installation on your desktop does not cover a remote machine. For an older unassigned task, assign the skill that fits its purpose before starting or resuming it:

```sh
herdr-task edit <task-id> --skill hc-build
```

Use `hc-build` only for implementation or debugging; choose another skill for other work. An old disabled HolyCow switch does not bypass the current assignment requirement. Existing custom role instructions are preserved during installation: remove conflicting hard-coded model routing when adopting the HolyCow settings, while retaining task, review, and proof rules.

## Choose where tasks work

Before starting work, check **BossGoat settings → Tasks** for **Worktrees**, **Review**, **Must fix**, **Proof**, and **Merge**. From your project's folder, inspect the effective configuration:

```sh
herdr-task config --json
```

Git tasks use separate worktrees by default. If your repository requires its original checkout, configure **Tasks → Worktrees** for that space accordingly, or explicitly request an original-folder task. Confirm the task's actual folder before editing, and run tasks that touch the same files sequentially. The [Assistant instructions](https://github.com/NeuralHerd/BossGoat/blob/main/templates/assistant.md) describe these choices.

When review is enabled, BossGoat's existing worker-led review uses the HolyCow **Review** model and `hc-review` instructions. It remains read-only and does not add a second review loop. Task review, proof, and merge settings still apply. Read `herdr-task show <task-id>` for that task's Settings block; ready, accepted, merged, and deployed are distinct outcomes.

## Try it with your Assistant

Paste this into your project's Assistant chat:

```text
I want to add team invitations to this project.
Use HolyCow to clarify who can invite people, which roles they can grant,
and when invitations expire. Follow this repository's checkout policy.
Keep this work in discovery until I accept the decisions; do not begin
implementation or change my model, review, or merge settings.
```

For a clear implementation task, describe the intended behavior and how to verify it. The Assistant selects the skill and the task uses your configured agent and model. You can follow progress, answer questions, and inspect the evidence before accepting work.

## Move from Shepherdr

BossGoat shares Shepherdr's command names and data paths. Treat this as a migration of the existing setup. Clone BossGoat and inspect its install dry run first. To preserve an existing `shepherdr` layout's pane sizes and preferences, run the following with Herdr open and your terminal in the BossGoat checkout:

```sh
herdr-app do layout.clone '{"name":"shepherdr","as":"BossGoat"}'
./install.sh --adopt --keys keep
shepherdr doctor
```

Skip the clone command if the **BossGoat** layout already exists. `--adopt` backs up and takes over conflicting installation files; `--keys keep` keeps existing shortcuts. Tasks, chats, and agent settings retain their storage paths. Inspect preserved custom instructions, `.new` files, and reported backups after installation. Select **BossGoat** with **Ctrl+Shift+L**. See the [layout migration instructions](https://github.com/NeuralHerd/BossGoat/blob/main/docs/install.md#upgrading-an-existing-shepherdr-layout).

For Shepherdr **2.x** or the older herdr-projects setup, read the [upgrade guide](https://github.com/NeuralHerd/BossGoat/blob/main/docs/upgrading.md) first. Do not pull `main` into a 2.x checkout; its task data does not carry into 3.x.

## Keep it current

From the BossGoat checkout used for installation:

```sh
git pull --ff-only
shepherdr update
shepherdr doctor
```

Review any custom files kept beside new versions or moved to backups. Update HolyCow separately using the [HolyCow update instructions](../../../../README.md#update). After changing installed guidance, start a fresh session or ask the active agent to re-read it; closing the Herdr window does not restart agents.
