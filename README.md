# HolyCow

**From idea to PR, with better questions and verified code.**

Portable, on-demand development skills by [NeuralHerd](https://github.com/NeuralHerd) for **Claude Code, Codex, and Cursor**. Use them to challenge an idea, run an experiment, plan useful increments, implement, review, and learn from the work.

Start where you are. A new idea can begin with questions and prototypes; a clear bug can go straight to implementation. A formal specification is optional.

> **Early release:** ten foundational skills are available. Live workflow evaluation across all three harnesses is still pending. The scenarios in `evals/` describe expected behavior, not passing results.

[Install](#install) · [Update](#update) · [Choose a skill](#choose-a-skill) · [Example workflows](#example-workflows) · [Contribute](#contribute)

## Install

Use the [Skills CLI](https://github.com/vercel-labs/skills). It currently requires **Node.js 22.20 or later**; Git must also be available for repository downloads.

Install all ten skills globally for Claude Code, Codex, and Cursor:

```sh
npx skills@latest add NeuralHerd/holycow -g -a claude-code codex cursor --skill '*'
```

Or install just the skill you need:

```sh
npx skills@latest add NeuralHerd/holycow -g -a claude-code codex cursor --skill hc-refine
```

Keep only the agents you use after `-a`. For a project-scoped installation, run from that project and omit `-g`. Review the installer's destinations and confirmation before proceeding. See the [CLI installation reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) for options.

Open your project in the harness and check its skill picker. If the new skills do not appear, reload skill discovery or restart the harness.

## Update

The installation commands above follow this repository's default branch, `main`. Maintainers publish skill updates by pushing changes there; a separate npm release is not required. `@latest` selects the Skills CLI version, not a HolyCow version.

To refresh **only HolyCow**, including newly added skills, rerun the installation command:

```sh
npx skills@latest add NeuralHerd/holycow -g -a claude-code codex cursor --skill '*'
```

Keep your original agents and installation scope: omit `-g` and run from the project root for a project installation. Replace `'*'` with specific skill names if you only want a subset. Reinstallation can overwrite local edits to installed skills.

For routine maintenance of skills already tracked by the CLI:

```sh
# Check for available updates
npx skills@latest check

# Update one globally installed skill
npx skills@latest update hc-refine -g

# Update all globally installed skills, including other repositories
npx skills@latest update -g
```

Use `-p` instead of `-g` with `update` for project installations, from the project root. See the [Skills CLI update reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-update).

### Renamed skills

Install the replacement name, confirm it is available, then remove the old name. For the `ask-holycow` to `holycow-guide` rename:

```sh
npx skills@latest add NeuralHerd/holycow -g -a claude-code codex cursor --skill holycow-guide
```

After confirming `holycow-guide` is installed:

```sh
npx skills@latest remove ask-holycow -g -a claude-code codex cursor
```

Use your original agents and scope for both commands. Check the skill picker after updating. Start a fresh conversation for the updated instructions, or ask an ongoing session to re-read the changed skill before continuing.

## First use

HolyCow Guide recommends the smallest useful next step:

| Harness | Example prompt in the agent chat |
| --- | --- |
| Claude Code | `/holycow-guide We have a new feature idea. Where should we start?` |
| Codex | `$holycow-guide We have a new feature idea. Where should we start?` |
| Cursor | `/holycow-guide We have a new feature idea. Where should we start?` |

These are chat invocations, not shell commands. Replace `holycow-guide` with any skill below when you already know what you need. `holycow-init` is optional repository onboarding; the other skills work without it.

## Recommended setup: Herdr + herdr-projects

For coordinating several agents, we recommend **HolyCow + [Herdr](https://herdr.dev) + [herdr-projects](https://github.com/eliasstravik/herdr-projects)**. Herdr organizes the agent terminals; herdr-projects adds a task board, delegation, and review; HolyCow supplies the workflow guidance. Our role instructions select the useful skills automatically inside Herdr.

The [setup guide](website/src/content/docs/herdr.md) includes installation, Anil's model choices, copyable configuration, and the Interaction Service example. HolyCow also works directly in your usual agent chat.

## Choose a skill

| Skill | Use it for | Outcome |
| --- | --- | --- |
| [holycow-guide](skills/holycow-guide/SKILL.md) | Choosing what to do next | A recommendation, reason, and expected result |
| [holycow-init](skills/holycow-init/SKILL.md) | Preparing or auditing a repository's workflow | Small project context, useful pointers, and verified capability status |
| [hc-compass](skills/hc-compass/SKILL.md) | Uncertainty that spans several sessions | An evolving map of questions, dependencies, decisions, and evidence |
| [hc-refine](skills/hc-refine/SKILL.md) | Challenging an idea or settling requirements | Agreed scope and decisions, with recommendations and trade-offs |
| [hc-lab](skills/hc-lab/SKILL.md) | Answering a question through a prototype or diagram | An inspectable experiment, observations, limitations, and feedback |
| [hc-plan](skills/hc-plan/SKILL.md) | Turning accepted understanding into deliverable work | A concise brief and, when requested, dependency-aware tickets |
| [hc-build](skills/hc-build/SKILL.md) | Implementing agreed work or diagnosing a failure | Scoped changes or diagnosis, verification evidence, and a handoff |
| [hc-review](skills/hc-review/SKILL.md) | Reviewing changes against intent and project standards | Prioritized, substantiated findings and coverage limits |
| [hc-pr](skills/hc-pr/SKILL.md) | Explaining a change to reviewers | A PR description covering behavior, evidence, and merge risk |
| [hc-retro](skills/hc-retro/SKILL.md) | Improving future work from session evidence | A few concrete improvements and ways to evaluate them |

Refine includes optional glossary and decision-record updates. Build includes debugging, meaningful testing, behavior-preserving refactoring, and conditional production guidance. Separate skills for those steps are unnecessary for this workflow.

## Example workflows

Choose only the steps the task needs:

- **An uncertain feature:** Compass maps the open questions; Refine resolves product decisions; Lab tests the questions that need an experiment. Plan prepares accepted work for Build.
- **A clear bug:** Build reproduces the failure, investigates, fixes it, verifies the outcome, and reviews the change.
- **An existing PR:** Review examines the actual changes. PR can then improve the description using the observed evidence.
- **A frustrating session:** Retro identifies supported causes and recommends improvements at the appropriate scope.

For example, in Claude Code or Cursor:

```text
/hc-refine Challenge this export idea. Workspace-admin access is agreed; scheduling and failure recovery are still open. Give recommendations with trade-offs.
```

After the decisions are accepted:

```text
/hc-plan Turn the accepted export behavior into small delivery tickets in our configured tracker. Keep unresolved decisions explicit.
```

In Codex, use `$hc-refine` and `$hc-plan` for the same requests. If your standing instructions require one question at a time, Refine follows them; explicitly allow grouped rounds if you prefer that format.

Build reads Review when available and uses PR for a requested PR description. Missing companions are disclosed before a direct fallback. PR descriptions, commits, pushes, tracker updates, and deployment follow the user's authorization and repository policy; selecting a skill does not grant blanket permission for the rest of the workflow.

## Invocation and context use

HolyCow is configured for **explicit invocation**. An ordinary request such as “fix this bug” should not automatically select `hc-build`.

- **Claude Code and Cursor:** `disable-model-invocation: true` in each `SKILL.md`. See [Claude Code skills](https://code.claude.com/docs/en/skills) and [Cursor skills](https://cursor.com/docs/skills).
- **Codex:** `policy.allow_implicit_invocation: false` in each `agents/openai.yaml`. See [OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills).

Full skill instructions load when selected, and supporting references are read as needed. A selected workflow may read relevant companion guidance within its scope and the harness's permissions. Discovery metadata can still consume context depending on the harness, and loaded instructions may remain in the conversation. HolyCow makes no zero-token or measured token-saving claim.

Use the [invocation scenarios](evals/invocation.md) to check your harness's behavior in fresh sessions.

## Project context and tools

Init reuses repository conventions and creates or updates a small context document only when appropriate. The default is `docs/agents/holycow.md`; an existing location linked by project instructions takes precedence. Skills read relevant sections and continue without that document when it is absent. See [project context](skills/holycow-init/references/project-context.md).

**Trackers:** Compass and Plan use the configured Jira, GitHub Issues, Linear, or other supported tracker through tools available in the current harness. Connections and permissions must already exist or be configured separately. Local Markdown is available when chosen or no tracker is configured. An unavailable selected tracker is reported, not silently replaced.

**Coordination:** Herdr is optional. Authorized parallel work can use Herdr within its supported environment or native subagents; otherwise the workflow continues directly. Installing HolyCow does not itself authorize delegation. See [research coordination](skills/hc-compass/references/research.md).

**Technology guidance:** AWS, framework, and provider skills are separate installations. HolyCow uses relevant installed guidance when the task needs it; those tools and services are not bundled here.

**Terminal identity:** Init includes a Cyber Halo Cow with a gold halo and cyan-to-violet shading. The Python renderer adapts to terminal width and color support; captured agent output can use plain text. See [terminal presentation](skills/holycow-init/references/terminal.md).

## Local development and evaluation

From a local checkout, inspect the skill catalogue without installing anything:

```sh
npx skills@latest add . --list
```

To install from that checkout:

```sh
npx skills@latest add . -g -a claude-code codex cursor --skill '*'
```

Keep the checkout available if the installer links to it. Preserve each whole skill directory, including references, assets, scripts, `agents/openai.yaml`, and `LICENSE`.

To update an installation linked directly to this checkout, run `git pull --ff-only` here. If the installation contains copies, rerun the local installation command after pulling. New or renamed skill directories also need the installation command again; remove obsolete names as described under [Update](#renamed-skills).

Preview the banner from the repository root with Python 3:

```sh
python3 skills/holycow-init/scripts/banner.py
```

Run its automated checks:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s evals -p 'test_init_banner.py'
```

The [evaluation directory](evals/) contains manual scenarios for all ten skills and invocation behavior. Run those in fresh harness sessions, record the version, inputs, actual actions, and results, and keep expected answers hidden from the executing agent. Passing renderer tests or parsing a skill file does not establish workflow quality. The [design review](docs/skill-design-review.md) records the current foundations and evaluation approach.

## Documentation website

The Astro website in [`website/`](website/) renders this README, skill instructions, supporting references, and public documentation directly from the repository. It is live at [holycow.neuralherd.dev](https://holycow.neuralherd.dev) on Cloudflare Workers Static Assets. See the [website setup and publishing guide](website/src/content/docs/hosting.md) for local preview, automatic publishing from GitHub, and custom-domain setup.

## Contribute

[Open an issue](https://github.com/NeuralHerd/holycow/issues) with a concrete failure or improvement, or submit a focused PR. Include the affected skill, a sanitized reproducer, expected versus observed behavior, and relevant harness details. Update the matching evaluation scenarios when behavior changes.

Prefer improving an existing skill or conditional reference when it already owns the responsibility. Propose a new skill when the need is distinct and reusable. Keep organization-specific examples, machine configuration, and private evaluation records in the ignored `.local/` directory.

## Credits and license

Thanks to Matt Pocock, Lauren Tan, Addy Osmani, and Dex Horthy / HumanLayer for the work HolyCow builds on. See [credits](docs/attribution.md).

[MIT licensed](LICENSE). Each skill carries its own `LICENSE` with the applicable upstream notices so credit travels with selective installation.
