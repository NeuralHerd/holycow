# Review coordination

Read this for delegated review, a board-managed handoff, or review corrections. Direct review of a small change does not need a separate orchestration phase.

## One owner and proportional coverage

Use the user's chosen coordinator, including Herdr within its supported environment, or native agent tools. The existing board or coordinator owns the review-and-correction cycle; otherwise Build owns authorized corrections. Review returns findings without starting its own fix-and-review loop.

Start with one independent reviewer for substantial work. When assigned as the board's reviewer, perform the review directly instead of spawning a replacement group. Only the coordinator assigns additional authorized specialists for a distinct risk, such as authorization, concurrency, or migration recovery, or an explicit request. Split coverage without dropping requirements, correctness, or applicable standards. Reviewers must not recursively delegate.

## Fresh context and compact handoffs

Start independent reviewers without inherited conversation. Supply the same baseline and target state, accepted contract, applicable instructions, source pointers, assigned responsibility, permitted actions, and stopping boundary. Omit the author's persuasive narrative and other reviewers' conclusions while preserving factual constraints. Reviewers may inspect consequential dependencies beyond the initial pointers.

Assign read-only work and request concise findings with evidence and coverage limits. Reviewers do not edit shared files or publish comments. The existing coordinator validates and consolidates findings; no additional aggregation agent is needed by default. Keep the result in the existing handoff or report rather than requiring a new artifact for every reviewer.

## One correction cycle by default

Follow the existing user or coordinator policy. Without one, default to an initial review, one batch of authorized corrections, and one focused recheck. A worker restart, replacement reviewer, or fallback must not reset that boundary. Changing runtime limits requires user authorization; prose guidance is not a hard token cap.

Keep stable finding identities and dispositions: open, fixed with evidence, or rejected with a reason. Pass that record, cycle position, correction diff, and check results into the recheck. Recheck affected findings and consequential dependencies; reuse unchanged evidence. Broaden coverage when additional changes or unresolved risk justify it, including regressions introduced by fixes. Do not reopen settled choices without new evidence or search for optional improvements to fill another round.

Apply the project's blocking threshold without inflating severity to force a fix. With no threshold, distinguish required behavior and safety defects from optional suggestions. At the boundary, return unresolved material findings and coverage gaps for a decision. Never treat exhausted time, tokens, or rounds as approval, silently accept a blocker, or weaken a required check to finish.
