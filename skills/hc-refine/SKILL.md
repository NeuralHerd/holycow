---
name: hc-refine
description: Use when the user asks to refine or stress-test an idea, requirement, plan, or decision before acting.
license: MIT
disable-model-invocation: true
---

# hc-refine

Reach shared understanding through questions that expose consequential assumptions. The user makes decisions; the agent investigates facts.

In a repository, use the HolyCow context linked by its instructions, or `docs/agents/holycow.md` when present. Read only relevant sections and reuse context already loaded. Continue without it; recorded capabilities may need rechecking in this session.

## Frame the discussion

Establish the intended outcome and scope from the context provided. For a new idea, clarify who it serves, the problem, and what success means; no repository or knowledgebase is required. Keep unrelated work outside this discussion.

Track decisions and their dependencies: accepted, ready to ask, waiting on a prerequisite or evidence, and explicitly deferred. This is a reasoning aid, not a diagram or required document.

## Investigate facts

When project materials exist, read relevant instructions, code, and decisions before asking questions they can answer. Distinguish confirmed requirements, observed implementation, proposals, and unknowns. Link evidence where it affects a decision.

Challenge contradictions and weak assumptions with their consequences. Preserve accepted decisions unless new evidence or the user's changes require revisiting them.

Challenge ambiguous terms against the project's language. Recommend precise names and use concrete edge cases to test relationships and boundaries before treating a definition as settled.

Investigate directly. Delegate research only when requested, using the user's chosen coordination tool, such as Herdr, within its execution constraints. The interview works without delegation or another installed skill.

## Work in rounds

Ask the ready questions: those whose prerequisites are settled. Group independent questions into manageable rounds. Ask a single question when it gates the others or the user requests that format. Questions dependent on an unanswered question belong in a later round.

For each decision question, present a short numbered list of viable options immediately below the question. Put the recommended option first and label it **Recommended**. Give each option's reason and main trade-off; usually two or three options are enough. Keep the choice self-contained rather than burying the recommendation in earlier analysis or ending with only "Shall we?"

> ❓ **Q1: Which records should this export include?**
>
> 1. **Current records only — Recommended.** Matches the current view and keeps the export focused; omits historical records.
> 2. **Current and archived records.** Supports historical analysis; adds records outside the current view.

Do not invent weak alternatives to fill the list. If only one option fits the accepted constraints, explain why and ask for confirmation. If missing evidence prevents a recommendation, state what is missing. Factual clarifications can be direct questions without options. Accept a custom answer as well as an option number.

Use stable, unique question numbers across rounds so short or dictated replies are easy to map. Wait for the user's answers.

Apply only answers actually given. Clarify ambiguous replies; unanswered questions stay open. Recompute dependencies after each round. If an answer changes, revisit affected downstream decisions.

When discussion cannot resolve a question, identify the missing evidence. If a prototype is needed, state the question it should answer and the observation that would help decide. Mark that decision as waiting and continue independent questions. Drawing, prototype execution, and production changes belong outside this skill.

## Preserve useful knowledge when wanted

Offer glossary or decision-record updates when they would help future work. Update files when the user accepts, has already requested them, or project instructions require them; do not ask again for existing authorization. A request not to change files takes precedence. Otherwise keep findings in the conversation.

Reuse the canonical documents, locations, and formats for the relevant domain. If none exist, include a simple proposed location in the offer. Create files only when there is substantive, settled content; no empty scaffolding or mandatory specification.

- **Glossary:** Capture agreed domain terms, meanings, and distinctions. Keep implementation details and unresolved proposals out of definitions. Surface conflicts with existing terms before changing them.
- **Architectural decision record (ADR):** Offer one only when the choice is costly to reverse, would be surprising without context, and resolves a real trade-off among alternatives. Capture the context, accepted choice, alternatives, reasons, and consequences using the project's format. Routine choices stay in the recap.

Record accepted findings as they settle; unanswered questions are not agreement. If an answer changes, update affected definitions and preserve decision history through the project's correction or supersession convention.

## Close the discussion

When material questions within the agreed scope are resolved, present a concise recap:

- Outcome and scope.
- Decisions, reasons, and supporting evidence.
- Remaining uncertainties, explicit deferrals, and their consequences.
- The next action.

Link any documents updated during the interview and identify remaining documentation work.

Keep the recap in the conversation unless the user requests a saved record or the project requires one. Follow the existing location and format.

Ask the user to confirm the recap. Incorporate corrections before marking the interview complete. A blocking unknown means the discussion is paused, not complete; deferring it requires an explicit scope decision. Subsequent work follows the user's instructions and existing authorization.
