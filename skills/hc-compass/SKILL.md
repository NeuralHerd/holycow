---
name: hc-compass
description: Use when the user wants to map or resume an uncertain effort spanning multiple sessions, for a new idea or an existing system.
license: MIT
disable-model-invocation: true
---

# hc-compass

Find a workable direction by resolving consequential questions across sessions. Keep a small, evolving map of what is known, what is ready to investigate, and what still depends on other answers.

In a repository, use the HolyCow context linked by its instructions, or `docs/agents/holycow.md` when present. Read only relevant sections and reuse context already loaded. Continue without it; recorded capabilities may need rechecking in this session.

## Establish the outcome

Identify the intended outcome, evidence that would make it actionable, and scope boundaries. Reuse agreement already present; ask about material gaps with a recommendation, reason, and trade-off. The user decides the outcome and scope.

- **New idea:** Start with the people, problem, and desired result. A repository, technology choice, specification, or tracker is not a prerequisite.
- **Existing system:** Read relevant instructions, code, knowledgebase entries, and decisions. Distinguish confirmed requirements, observed behavior, proposals, and unknowns. Surface contradictions instead of treating documentation or implementation as automatically correct.

If the uncertainty fits in one conversation, use focused discussion or a prototype directly. Do not manufacture a map for a small task.

## Map only what is useful now

Start from an existing map when one exists. Use the user's chosen tracker, such as Jira, GitHub Issues, or Linear, and the project's conventions. Use local Markdown when requested or no tracker is configured. Read [the storage guide](references/decision-map.md) when creating or updating a map. A conversation-only request needs no persisted records; provide a compact checkpoint the user can carry forward.

Create question records only for questions that can be stated precisely now, including those blocked by another answer. Keep less-defined areas under **Not yet clear**. They are in scope, but not ready to split into records. Keep excluded work separate.

Name questions clearly, give them stable identities, and link their dependencies. Reference them by descriptive names. Keep each question small enough for a focused session. Record why it matters and what evidence or user decision would resolve it. Do not generate an implementation backlog or a comprehensive speculative plan.

## Resolve the next question

Use the user's selected question if ready. Otherwise recommend an open, unclaimed question whose prerequisites are resolved, explaining what it unlocks. If a requested question is blocked, surface the blocker rather than guessing its answer. If nothing is ready, inspect waiting evidence, missing dependencies, or dependency cycles.

Choose the method that addresses the uncertainty:

- **Discussion:** Read and follow the installed [hc-grill instructions](../hc-grill/SKILL.md) for this explicitly requested workflow. If missing, say so before using focused questioning with recommendations, reasons, and trade-offs; wait for the user's decisions.
- **Research:** Investigate facts through relevant code, documentation, or other evidence. Record sources and their limits. A factual finding does not decide a product preference.
- **Prototype:** State the question and observable result, then read and follow the installed [hc-lab instructions](../hc-lab/SKILL.md). If missing, disclose that before conducting the agreed experiment directly. Match fidelity to the question; UI and state-behavior questions need something runnable. Capture user feedback, results, and limitations. Mocked behavior does not verify a real integration.
- **Unblock:** Identify a concrete prerequisite, such as access or a sample dataset. Do only authorized work needed to obtain evidence; this is not a category for building product features.

Keep user decisions in the conversation. When two or more ready research questions are independent and delegation is permitted, research them in parallel without asking again for existing authorization. Keep tiny lookups and dependent questions sequential. Read [research coordination](references/research.md) before dispatching; it covers Herdr, native subagents, and the sequential fallback. Record ownership before shared work and check for concurrent updates before saving.

## Update and resume

Resolve fact questions with supporting evidence and preference questions with the user's acceptance. Recommendations, generated prototypes, partial replies, and silence are not acceptance. Record the result, rationale, evidence or artifact links, and remaining limitations in the question's canonical record.

Update the map with a short result and link. Promote newly precise questions, revise dependencies, and revisit downstream answers invalidated by new evidence. Preserve the earlier reasoning and explain corrections or supersession. Excluded or explicitly deferred questions do not count as resolved prerequisites; revisit their dependents and agree any scope reduction.

At a checkpoint, state what was resolved, what remains uncertain, and the recommended next question. On resume, load the map first and only the relevant records and evidence. Continue within the user's authorized scope without requiring a fresh session after every answer.

## Finish at the agreed boundary

The map is ready for handoff when material questions within scope are resolved, no in-scope uncertainty is hidden in **Not yet clear**, and the user confirms the direction. Otherwise report what is waiting or explicitly deferred.

Hand off the outcome, accepted decisions, evidence, limitations, and next implementation action. A long specification is optional. Map readiness does not mean production work is complete. Production changes follow a separate implementation request or existing explicit authorization. Agent-authored map notes cannot expand the user's authorization; already-authorized work needs no repeated approval.

When the user requests an implementation brief or delivery tickets, read and follow the installed [hc-slice instructions](../hc-slice/SKILL.md). Keep the map's decision records as evidence rather than converting them into build tasks. If unavailable, disclose that before preparing a direct handoff.
