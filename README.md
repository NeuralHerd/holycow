# HolyCow

**From idea to PR, with better questions and verified code.**

Portable, on-demand development skills by [NeuralHerd](https://github.com/NeuralHerd) for **Claude Code, Codex, and Cursor**. Use them to challenge an idea, run an experiment, plan useful increments, implement, review, and learn from the work.

Start where you are. A new idea can begin with questions and prototypes; a clear bug can go straight to implementation. A formal specification is optional.

> **Early release:** ten foundational skills are available. Live workflow evaluation across all three harnesses is still pending. The scenarios in `evals/` describe expected behavior, not passing results.

[Install](#install) · [Choose a skill](#choose-a-skill) · [Example workflows](#example-workflows) · [Contribute](#contribute)

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

## First use

Ask HolyCow recommends the smallest useful next step:

| Harness | Example prompt in the agent chat |
| --- | --- |
| Claude Code | `/ask-holycow We have a new feature idea. Where should we start?` |
| Codex | `$ask-holycow We have a new feature idea. Where should we start?` |
| Cursor | `/ask-holycow We have a new feature idea. Where should we start?` |

These are chat invocations, not shell commands. Replace `ask-holycow` with any skill below when you already know what you need. `holycow-init` is optional repository onboarding; the other skills work without it.

## Choose a skill

| Skill | Use it for | Outcome |
| --- | --- | --- |
| [ask-holycow](skills/ask-holycow/SKILL.md) | Choosing what to do next | A recommendation, reason, and expected result |
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

Preview the banner from the repository root with Python 3:

```sh
python3 skills/holycow-init/scripts/banner.py
```

Run its automated checks:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s evals -p 'test_init_banner.py'
```

The [evaluation directory](evals/) contains manual scenarios for all ten skills and invocation behavior. Run those in fresh harness sessions, record the version, inputs, actual actions, and results, and keep expected answers hidden from the executing agent. Passing renderer tests or parsing a skill file does not establish workflow quality. The [design review](docs/skill-design-review.md) records the current foundations and evaluation approach.

## Contribute

[Open an issue](https://github.com/NeuralHerd/holycow/issues) with a concrete failure or improvement, or submit a focused PR. Include the affected skill, a sanitized reproducer, expected versus observed behavior, and relevant harness details. Update the matching evaluation scenarios when behavior changes.

Prefer improving an existing skill or conditional reference when it already owns the responsibility. Propose a new skill when the need is distinct and reusable. Keep organization-specific examples, machine configuration, and private evaluation records in the ignored `.local/` directory.

## Credits and license

HolyCow draws from three complementary sources:

- [Matt Pocock's skills](https://github.com/mattpocock/skills): questioning, discovery, prototypes, and delivery workflows.
- [Lauren Tan / poteto's pstack](https://github.com/cursor/plugins/tree/main/pstack): domain modeling, design judgment, and verification of downstream effects.
- [Addy Osmani's agent-skills](https://github.com/addyosmani/agent-skills): quality requirements, focused review, and operational readiness.

The PR guidance also retains the credit to Dex Horthy / HumanLayer's `show-me` through Matt's work. See [full attribution](docs/attribution.md) for pinned source links and adaptation details, and the [design review](docs/skill-design-review.md) for the choices adopted and omitted.

[MIT licensed](LICENSE). Each skill carries its own `LICENSE` with the applicable upstream notices so credit travels with selective installation.
