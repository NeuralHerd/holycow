---
name: hc-retro
description: Use when the user asks for a retrospective on development sessions to identify evidence-backed improvements to agent workflows, instructions, tooling, or checks.
license: MIT
disable-model-invocation: true
---

# hc-retro

Turn observed session friction and successful practices into a few useful improvements for future work. Prefer fixing the cause over accumulating instructions. A retrospective may cover completed, interrupted, or unsuccessful work; it does not require a merged PR.

In a repository, use the HolyCow context linked by its instructions, or `docs/agents/holycow.md` when present. Read only relevant sections and reuse context already loaded. Continue without it; recorded capabilities may need rechecking in this session.

## Establish the evidence

Use the requested session or sessions; default to the current conversation. Read relevant primary evidence such as user corrections, tool results, implementation changes, test outcomes, and review findings. Retrieve only the transcript or log segments needed to understand a candidate issue, not unrelated histories or entire global configurations.

State material coverage limits. A summary can locate evidence but cannot establish that an action ran or a result passed. If earlier records are unavailable, analyze the visible portion without inventing the missing sequence.

For each candidate, connect the intended outcome, what actually happened, and the practical consequence. Distinguish observation from a possible cause. Verify claims of repetition; one consequential failure can justify action, but one occurrence is not a recurring pattern.

Changing requirements, deliberate experiments, legitimate permission boundaries, and unavailable services are not automatically agent failures. Identify what could realistically have improved the result with the information available then.

## Diagnose before prescribing

Inspect the relevant current instructions, scripts, checks, and workflow before recommending additions. Determine whether guidance was missing, inaccessible, contradictory, outdated, or present but ignored. Another copy of an ignored rule rarely addresses its cause.

Consider only areas supported by the evidence:

- **Finding information:** Missing navigation pointers, hidden dependencies, or stale references that caused unnecessary exploration or incorrect assumptions.
- **Verification:** Important mistakes a focused check could catch, or an existing check that was skipped, misconfigured, or disconnected from the actual workflow.
- **Decisions and handoffs:** Lost accepted decisions, unclear ownership, missing prerequisites, or ambiguous completion evidence between sessions or agents.
- **Instructions and review:** Conflicting guidance, unsupported review findings, or judgment calls that need a clearer rule or example.
- **Tool and context use:** Repeated broad reads, oversized outputs, duplicated work, or missing access that materially affected the task.

Also preserve demonstrated practices that worked. Do not propose a change merely to fill a category or turn ordinary task history into a process defect.

For context-efficiency claims, separate installed content from evidence of what the harness actually loaded. Word counts and file sizes are estimates, not measured token use or savings. Do not recommend removing a useful skill solely because its files are large.

When evaluating review or delegation costs, count the whole task: planning, workers, reviewers, corrections, retries, and fallbacks. Use available provider or harness usage records; distinguish input, cached input, and output where reported, and mark missing usage as unknown. Tokens, price, and elapsed time are different measures.

Compare similar tasks under recorded skill revisions, harnesses, models, permissions, and quality requirements. Pair total usage and correction rounds with substantiated findings, repeated or rejected findings, rework, required checks, and defects discovered later. Attribute a repeated pass to its actual cause, such as changed scope, a failed check, or duplicate review ownership. Fewer tokens with missed defects or incomplete verification do not establish an improvement; a single successful task does not establish a reliable saving.

## Choose a proportionate remedy

Prefer deterministic checks for mechanically detectable problems when their benefit justifies maintenance. Reuse the project's existing lint, type, test, or CI mechanism before proposing another one. A missing hook or CI job is not automatically a defect without considering the repository's purpose and risk.

Use concise guidance for genuine judgment calls. Correct a stale pointer or conflicting instruction at its source; avoid duplicating policy across steering files and skills. Keep frequently loaded instructions small and link conditional detail where the harness can discover it.

Place each remedy at the narrowest useful scope: implementation or test, project guidance, reusable skill, or user-wide setup. Keep private domain rules and session evidence in the project's approved private location. Public skill improvements need a reusable lesson and sanitized examples, not copied internal logs, identifiers, or machine-specific paths.

Do not weaken a required check, permission boundary, or review step merely to reduce friction. Recommend a concrete improvement and explain its cost or trade-off. Rank candidates by demonstrated impact, likely recurrence, and implementation cost; separate urgent defects from optional workflow experiments.

## Propose or apply within scope

A retrospective request normally asks for analysis and recommendations. If the user already requested improvements to be applied, carry out those authorized changes without another approval round. Otherwise, provide concrete proposals without silently editing files, changing global settings, publishing tickets, or installing tools.

Before an authorized edit, inspect the target and current working changes, preserve unrelated work, and follow the repository workflow. Reuse existing guidance or tooling where suitable. Avoid turning one session into a broad rewrite.

For a substantial implementation, use `hc-build` when installed; use `hc-plan` if delivery tickets are requested. Disclose a missing companion before proceeding directly. These skills are optional, and a small authorized correction needs no additional workflow.

Verify applied changes at the relevant boundary. A deterministic check should catch the intended failure and allow an acceptable case; an instruction edit should retain valid structure and links. Behavioral improvement from new guidance remains unproven until a later relevant run demonstrates it.

## Return a usable result

For each worthwhile recommendation, provide the evidence, suspected or established cause, proposed change and destination, why it is preferable, and how improvement could be verified. Keep the list short enough to act on; no findings is a valid result when the evidence supports none.

Clearly distinguish proposed, applied, verified, and deferred work. Link actual changed files or authorized tracker records, report failed or unavailable checks, and identify any decision needed from the user.

On a later retrospective, compare relevant outcomes with previous recommendations before adding new rules. Resolve or revise stale lessons instead of accumulating them. Do not claim an improvement saved time, reduced tokens, or prevented recurrence without supporting observations.
