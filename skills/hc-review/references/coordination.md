# Review coordination

Read this for delegated review, a board-managed handoff, or review corrections. Direct review of a small change does not need a separate orchestration phase.

## One owner and proportional coverage

The existing board or coordinator owns the cycle; otherwise Build owns authorized corrections. Use the user's chosen coordination tool within its supported environment. Review returns findings without starting another fix-and-review loop.

An assigned reviewer performs the review directly. Only the coordinator adds authorized specialists for distinct risks or an explicit request, preserving requirements, correctness, and standards coverage. Reviewers do not recursively delegate.

## Fresh context and compact handoffs

Start independent reviewers without inherited conversation. Supply one assignment with the same baseline and target, accepted contract, project instructions, known source and applicable guidance paths, responsibility, permitted actions, and stopping boundary. Preserve factual constraints, omit persuasive conclusions, and allow inspection of consequential dependencies.

Assign read-only work; reviewers neither edit shared files nor publish comments. Dispatch once, use a bounded completion wait, and inspect compact status on timeout before acting. Do not resend possibly delivered work or repeatedly read transcripts. Retrieve logs for failures, missing evidence, or requested measurements. The existing coordinator validates and consolidates completed findings once, with evidence and coverage limits, in the existing handoff or report; no extra aggregation agent or per-reviewer artifact is needed by default.

## One correction cycle by default

Follow the existing user or coordinator policy. Without one, default to an initial review, one batch of authorized corrections, and one focused recheck. A worker restart, replacement reviewer, or fallback must not reset that boundary. Changing runtime limits requires user authorization; prose guidance is not a hard token cap.

Carry stable finding identities and dispositions (open, fixed with evidence, or rejected with a reason), cycle position, correction diff, and check evidence into the recheck. Bind check evidence to its command, outcome, reviewed state, and relevant environment. Reuse it only while those dependencies remain valid; a prior pass or completion summary alone is insufficient. Inspect the actual correction and affected callers, rerun invalidated checks, and broaden for new changes or unresolved risks. Do not reopen settled choices without new evidence or search for optional improvements to fill another round.

Apply the project's blocking threshold without inflating severity to force a fix. With no threshold, distinguish required behavior and safety defects from optional suggestions. At the boundary, return unresolved material findings and coverage gaps for a decision. Never treat exhausted time, tokens, or rounds as approval, silently accept a blocker, or weaken a required check to finish.
