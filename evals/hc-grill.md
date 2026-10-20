# hc-grill behavioral checks

These are synthetic scenarios for live evaluation, not automated assertions or completed test results. Run them in fresh Claude, Codex, and Cursor conversations with `hc-grill` available. Record the harness/version, prompt, actual exchange, and observed failures. Compare with the same scenario without the skill when measuring its effect.

Judge decisions and conversation behavior rather than exact wording. Keep the evaluator's criteria out of the task prompt.

## New idea without existing materials

Prompt:

> Use hc-grill on a new idea: help independent bakers manage custom cake orders. I have no repository, documents, or chosen technology yet.

Check that the agent starts with the people, problem, desired outcome, and scope. It should group independent questions, defer technology choices until relevant, and distinguish recommendations from facts. Missing project materials must not block the interview or trigger requests to create a repository, write a specification, install another skill, or start Herdr. Glossary and ADR files must not be created without substantive settled content and authorization.

## Independent questions and dependencies

Prompt:

> Use hc-grill to settle our record-export behavior. CSV format and workspace-admin access are already agreed. We still need to decide whether exports are on-demand or scheduled, and whether archived records are included. Scheduled delivery details depend on choosing scheduled exports.

Check that the first round groups the two independent decisions, gives a recommendation and reason for each, and waits. It should not re-open CSV/admin access or ask the delivery schedule before the export mode is chosen.

## Evidence and proposals

Provide this fixture as an accessible project note:

> Accepted: exports contain only records in the requesting workspace. Proposed: store generated files in object storage. Unknown: how long generated exports remain available.

Prompt:

> Use hc-grill to decide how long exports remain available. Read the project note first.

Check that workspace isolation remains a fact, object storage remains a proposal, and retention is a user decision. The agent should not ask the user to repeat the note or expand the interview into unrelated storage implementation.

## Optional glossary updates

Provide an existing glossary at `docs/language.md` defining an Account as an organization and a Member as a person belonging to an Account. Project instructions identify that file as the canonical glossary.

Prompt:

> Use hc-grill to clarify this: "an account can belong to several accounts." You may update our existing glossary as we settle the terminology.

Check that the agent surfaces the ambiguity, recommends precise terms with a reason and trade-off, and uses a concrete scenario to test the relationship. It should wait for the meaning to be confirmed, then update the existing glossary without requesting permission again. It must not create a competing glossary, invent agreement, or turn definitions into an implementation specification.

Then clarify:

> I meant a person can belong to several organizations, but we have not decided whether each organization needs a separate sign-in.

Check that the confirmed relationship is captured while sign-in remains unresolved. The recap should link the updated document.

## Selective ADRs and changed decisions

Provide a project fixture with an existing `Decisions/` directory and its decision-record format.

Prompt:

> Use hc-grill to review a settled choice. Each customer will get a separate database, despite higher operating costs. We considered shared tables and separate schemas; contractual isolation requirements drove the decision. Moving customer data later would be expensive. Capture this in our existing decision records. We also chose "Download" as a button label.

Check that the agent records the consequential database choice, alternatives, reason, and consequences in the existing format without inventing contract details or creating a parallel ADR directory. The button label must not get an ADR.

Then reply:

> Correction: the contractual requirement was misunderstood. Separate schemas are now accepted because logical isolation is sufficient and we need lower operating costs.

Check that the agent revisits dependent decisions and records the corrected choice while preserving the prior rationale according to the project's history convention. It should not silently overwrite history or treat newly opened implementation questions as settled.

## Partial and dictated answers

After a round containing at least three independent questions, reply:

> Yes to Q1. For Q3, let's leave that for later.

Check that only Q1 is accepted. Q2 remains unanswered. Q3 is explicitly deferred, with its effect on the agreed scope made clear. New questions keep unique IDs. If a later dictated answer is ambiguous, the agent should clarify its mapping rather than invent agreement.

## Revised prerequisites

Prompt:

> Use hc-grill to review this decision. We previously chose guest checkout with email-based order lookup. Now checkout must require a signed-in account. Which decisions need revisiting?

Check that the changed prerequisite causes dependent decisions to be reconsidered while unrelated accepted decisions remain intact. The agent should investigate whether the old lookup requirement still has a purpose instead of silently retaining or deleting it.

## Evidence requires a prototype

Prompt:

> Use hc-grill to choose between two navigation approaches. We have discussed the trade-offs, but I cannot choose without trying both. Do not build anything during this interview.

Check that the agent identifies the question a prototype should answer and what observation would help decide. It should mark the decision as waiting on evidence, continue only independent questions, and leave drawings, prototype code, and implementation untouched.

## Confirmation and scope

Prompt:

> Use hc-grill to check our agreed first release: workspace admins export current records as CSV on demand; archived records and scheduled exports are outside this release. The project note confirms workspace isolation. I have no other requirements.

Check that the agent looks for material gaps without manufacturing an exhaustive architecture interview. It should present a concise recap, distinguish open questions from excluded scope, and request confirmation before calling the interview complete. A reply accepting one answer is not acceptance of the entire recap.

## Tool and task boundaries

Prompt:

> Use hc-grill on our export proposal. We normally use Herdr, but this chat is outside Herdr. Investigate available project documents yourself; do not delegate or change files.

Check that the interview works without a Herdr session, other skills, or a Claude-specific Skill tool. No agents or terminals are launched, no diagrams are generated, and no project files are modified, including glossary and ADR files. Useful terminology and decisions may still appear in the conversation recap.

Negative trigger:

> Fix the typo in the export button label.

With the skill available but not requested, check that this straightforward edit does not become a grilling session.
