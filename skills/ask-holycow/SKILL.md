---
name: ask-holycow
description: Use when the user asks which HolyCow skill or workflow to use next, or whether the toolkit needs an additional skill.
license: MIT
disable-model-invocation: true
---

# Ask HolyCow

Recommend the smallest useful next step from the user's current situation. Help them use the toolkit without memorizing it or following a mandatory sequence.

## Establish the situation

Distinguish choosing a skill for project work from deciding what to add to the toolkit itself. Reuse the stated outcome, accepted decisions, completed work, and actual blockers. Ask a concise clarifying question only when missing information changes the recommendation.

Inspect the relevant available skill definitions before describing their behavior or recommending that a step be skipped. The table below is an orientation aid, not a substitute for current instructions. Check availability in the active harness; a skill mentioned in the catalogue is not necessarily installed.

| Immediate need | Candidate |
| --- | --- |
| Initialize or refresh repository workflow configuration | `holycow-init` |
| Resolve consequential uncertainty across multiple sessions | `hc-compass` |
| Challenge an idea or settle requirements through discussion | `hc-grill` |
| Answer a question with a prototype, experiment, or diagram | `hc-lab` |
| Turn accepted understanding into a brief or delivery tickets | `hc-slice` |
| Implement agreed behavior or investigate and fix a failure | `hc-build` |
| Examine changes for defects and requirements or standards gaps | `hc-review` |
| Explain changes, evidence, and merge risks in a PR description | `hc-pr` |
| Improve future work using evidence from past sessions | `hc-retro` |

## Recommend a bounded route

Lead with one recommendation and why it fits now. State the expected result and any material prerequisite. Include a short alternative only when a real trade-off warrants it.

Start from the current stage. Clear work can go directly to Build; reviewing an existing PR need not restart planning. Init is optional, and Compass is for uncertainty that benefits from a persistent map. A failed check calls for investigation, not automatically a retrospective.

For a longer flow, show only the steps justified by the task and stop at the requested boundary. Do not prescribe every skill, an automatic new session, context clearing, or delegation.

If the useful skill is missing, disclose that and offer a direct approach or installation guidance as appropriate. Do not silently install it or pretend it ran. If no skill fits, say so rather than forcing the task into the catalogue.

For toolkit additions, compare the missing capability with existing skills and references first. Recommend a separate skill only when it has a distinct, reusable responsibility; otherwise propose a focused extension or evaluation of the existing behavior.

Advice alone does not launch agents, modify files, or publish work. When the user also requests the recommended action, load and follow the available skill and carry out that action within the established scope.
