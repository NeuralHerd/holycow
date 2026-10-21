---
name: hc-lab
description: Use when the user wants a prototype, interactive experiment, or diagram to answer a specific design, behavior, or integration question before implementation.
license: MIT
disable-model-invocation: true
---

# hc-lab

Make a focused experiment the user can inspect or try. The goal is evidence for a decision; the artifact is disposable implementation, worth preserving as a reference.

In a repository, use the HolyCow context linked by its instructions, or `docs/agents/holycow.md` when present. Read only relevant sections and reuse context already loaded. Continue without it; recorded capabilities may need rechecking in this session.

## Frame the experiment

Identify the unresolved question, relevant accepted decisions, and what observation would help answer it. Reuse context from the conversation or a Compass question without requiring either `hc-compass` or `hc-refine`.

For a new idea, start from the intended user and outcome; no repository or specification is required. In an existing system, inspect the relevant code, instructions, and design conventions before building.

Recommend an experiment and explain its trade-off in fidelity, effort, and what it can establish. Clarify material ambiguity before coding; do not turn a clear request into another full interview. A request to plan an experiment does not authorize building it.

## Choose the useful fidelity

- **UI or interaction:** Build something the user can operate. Read [UI experiments](references/ui.md). Compare alternatives when there is a real design choice, not to fill a variant quota.
- **Logic, state, or integration:** Make relevant behavior executable and observable. Read [behavior experiments](references/behavior.md). Distinguish exploring a model from testing the real runtime or API.
- **Structure or flow:** Use an editable diagram when relationships, boundaries, or sequencing are the question. Use the user's available drawing tool, such as tldraw, or a portable editable format. Label assumptions and decisions awaiting evidence. A diagram cannot establish interaction quality, runtime behavior, or integration correctness.

Start with the least work that produces useful evidence. Raise fidelity when the current artifact cannot answer the question; don't polish unrelated parts.

## Build within the agreed scope

Follow the user's repository workflow and project conventions. Preserve unrelated changes. Keep experiment files clearly marked and keep experimental behavior out of the normal production path. For a new idea, use a self-contained artifact or a small folder in the working directory; do not require a new repository, branch, or worktree.

Reuse existing tools and components when useful. Follow the project's visual theme. Make the artifact easy to run through one command, a local URL, or opening a file. Herdr can host previews or requested delegated work when available; follow its execution constraints. The experiment must not require Herdr.

Use in-memory state or fixtures by default, clearly identifying simulated behavior. Connect to real services only when the question requires it and the test environment is authorized. Keep UI experiments away from real mutations. Avoid speculative abstractions and production hardening unrelated to the question.

## Try, inspect, and iterate

Run the artifact and exercise the scenarios that could change the decision. Follow required project checks and verify affected existing behavior. Report what actually ran and any limitations; writing code or starting a server alone does not verify the experiment.

Provide the artifact or exact run instructions and a short list of things to try. Recommend a direction with reasons and a meaningful trade-off, then obtain the user's feedback. Incorporate combinations of alternatives as well as requests for new behavior. Keep comparisons fair and earlier useful variants inspectable.

If the user is unavailable, prepare the bounded experiment and report that review is pending. Do not select a winner or claim acceptance on their behalf. If evidence remains inconclusive, identify the missing observation and the smallest useful next experiment.

## Preserve the learning

Once the user accepts the conclusion, capture:

- The question and accepted answer, with reasons.
- The artifact location and how to run or inspect it.
- Observed results, simulated parts, and unresolved limitations.
- What the next implementation step must preserve or still verify.

Update the existing decision record or tracker when requested or already authorized. Otherwise provide the handoff in the conversation. Link the artifact instead of replacing it with a prose specification.

Do not automatically delete alternatives, publish, or promote prototype code to production. Preserve useful evidence in the agreed location. Later implementation may reuse suitable code after review and validation against production requirements; a successful experiment alone does not establish production readiness.
