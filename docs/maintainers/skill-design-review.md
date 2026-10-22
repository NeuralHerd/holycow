# HolyCow skill design review

Reviewed on 2026-10-20 against the repositories' then-current revisions. This compares workflow design and relevant source instructions; it is not a benchmark of agent performance.

## What each source contributes

| Source | Useful contribution | HolyCow decision |
| --- | --- | --- |
| [Matt Pocock](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills) | Dependency-aware questioning, evolving decision maps, experiments, vertical delivery slices, and distinct review perspectives. | Keep the existing workflow foundation. This is the same revision already credited by HolyCow. A clear request can still go directly to Build. |
| [pstack by Lauren Tan / poteto](https://github.com/cursor/plugins/tree/88d47514b82e7c44f00f2b2a72ff6dd12158038c/pstack) | Deliberate domain models, simpler interfaces, tracing consequences beyond the diff, and checking pivotal assumptions against running code. | Strengthen Build and Review without adopting the full orchestration framework. |
| [Addy Osmani's agent-skills](https://github.com/addyosmani/agent-skills/tree/aeac41d4d005999432bb7312f7ff06383a91d59d) | Standing quality requirements, protection against weakened checks, focused adversarial review, and operational verification. | Strengthen Init, Plan, Build, and Review. Keep detailed production guidance conditional. |

## Review of all ten skills

| Skill | Decision and reason |
| --- | --- |
| `holycow-guide` | Keep. It already selects the smallest useful next step and reads actual skill definitions. |
| `holycow-init` | Extend discovery to standing quality requirements. Link canonical policy; distinguish enforced checks, aspirations, and exceptions. Do not manufacture numerical budgets. |
| `hc-compass` | Keep. It already separates questions from delivery tickets, records evidence, and coordinates bounded research under the user's delegation rules. |
| `hc-refine` | Keep. Recommendations, dependency-aware rounds, factual investigation, partial answers, and optional glossary/ADR updates are already present. |
| `hc-lab` | Keep. It already offers executable experiments, fair alternatives, real-service evidence when necessary, and explicit limits on simulations. |
| `hc-plan` | Link standing quality requirements separately from acceptance criteria and include affected operational concerns in the delivery brief. |
| `hc-build` | Identify state ownership and invariants before implementation. Characterize behavior before refactoring, probe critical external assumptions, preserve checks, and retain a concrete resumption checkpoint. Load production guidance only for affected work. |
| `hc-review` | Follow serialized data and runtime dependencies beyond symbol callers. Check critical safety assumptions and changes that weaken tests or gates. Give authorized reviewers the contract and evidence without persuasive author framing. |
| `hc-pr` | Keep. Its existing evidence, compatibility, and recovery guidance already distinguishes a Git revert from undoing system effects. |
| `hc-retro` | Keep. It already prefers structural remedies over more instructions and distinguishes applied changes from demonstrated improvement. |

## Sources for the enhancements

From pstack:

- [Model the domain](https://github.com/cursor/plugins/blob/88d47514b82e7c44f00f2b2a72ff6dd12158038c/pstack/skills/principle-model-the-domain/SKILL.md) and [architect](https://github.com/cursor/plugins/blob/88d47514b82e7c44f00f2b2a72ff6dd12158038c/pstack/skills/architect/SKILL.md): caller needs, state shape, invariants, and recognizing a mistaken model.
- [Blast radius](https://github.com/cursor/plugins/blob/88d47514b82e7c44f00f2b2a72ff6dd12158038c/pstack/skills/blast-radius/SKILL.md) and [prove it works](https://github.com/cursor/plugins/blob/88d47514b82e7c44f00f2b2a72ff6dd12158038c/pstack/skills/principle-prove-it-works/SKILL.md): trace non-obvious consumers and test the assumption a safety claim depends on.

From Addy's toolkit:

- [Definition of done](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/references/definition-of-done.md) and [constraint-driven development](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/constraint-driven-development/SKILL.md): standing requirements and detecting weakened quality gates.
- [Code simplification](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/code-simplification/SKILL.md) and [doubt-driven development](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/doubt-driven-development/SKILL.md): preserve behavior and review artifacts against contracts without inheriting the author's conclusions.
- [Security](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/security-and-hardening/SKILL.md), [API design](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/api-and-interface-design/SKILL.md), [observability](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/observability-and-instrumentation/SKILL.md), and [shipping](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/shipping-and-launch/SKILL.md): access boundaries, retry safety, useful operational signals, and recovery.
- [Browser testing](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/browser-testing-with-devtools/SKILL.md) and [context engineering](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/context-engineering/SKILL.md): runtime evidence and restartable handoffs.

The affected standalone skills retain upstream MIT copyright notices in their own `LICENSE` files so attribution travels with selective installation.

## Deliberate boundaries

HolyCow does not adopt pstack's persistent mode, automatic external actions, fixed model defaults, or mandatory parallel design candidates. It does not adopt a mandatory spec phase, universal test ratios, numerical release thresholds, or repeated cross-model approval prompts from Addy's toolkit. These choices must fit the user's task, project, harness capabilities, and authorization.

Herdr remains optional. Claude, Codex, and Cursor keep explicit invocation controls. No additional skill, hook, global instruction, or agent runtime is introduced by this review.

## Evaluation still needed

The new cases in [Init](../../evals/holycow-init.md), [Plan](../../evals/hc-plan.md), [Build](../../evals/hc-build.md), and [Review](../../evals/hc-review.md) describe expected behavior; they are not passing results.

For live comparison, use equivalent fixtures and permissions in fresh sessions, keep expected results hidden from the executing agent, and record the skill revision, harness/model, actual outcomes, and observed context use. Include simple tasks to detect unnecessary process as well as failure cases. Repeat consequential cases before attributing a difference to the skill change. File validation and word counts cannot establish behavioral improvement or token savings.
