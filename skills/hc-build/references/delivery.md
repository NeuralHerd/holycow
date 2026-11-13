# Delivery and handoffs

Use this for releases and delivery spanning sessions or repositories. Reuse the project's workflow, native tools and existing records; a simple edit needs no release packet or new coordinator.

## Establish the candidate and current authority

Resolve the requested source and base revisions before acting. A receiving checkout, task summary or older successful run may describe a different candidate. Reviewers need the same exact target; inspect its content before proposing a fix that may already exist.

Keep one current entry in the existing release record or task, linking rather than copying:

- Accepted outcome, exclusions, owner and next unresolved action.
- Participating source/configuration revisions and, when built, immutable artifact identity.
- Required checks with native run links, their outcomes and the candidate they verified.
- Completed external effects, uncertain submissions and their native operation IDs.
- Live baseline, acceptance and recovery evidence where the task requires deployment.

Preserve historical receipts as history. Reconcile contradictory current claims against source and native evidence; do not overwrite history to make it look current. On resume, check relevant files, processes and submitted operations before repeating work. Carry accepted decisions forward without widening their scope or requesting the same permission again.

## Get feedback before expensive qualification

Run relevant inexpensive checks before slow integration or warehouse checks when the existing workflow permits it. Measure the critical path before adding workers or changing selection. DORA's roughly ten-minute fast-feedback guidance is an optimization target, not a timeout or waiver for required acceptance tests.

Stabilize the candidate before expensive qualification, without freezing other teams' work or postponing correctness fixes. Reuse evidence only where its inputs and required validity still match. Changed code, configuration, dependencies or data may invalidate different checks. One final source-validation pass per stable candidate is a useful efficiency target, never a maximum number of allowed runs.

After a passing expensive qualification, retain the actual artifacts and native run identity. Test subsequent changes against that qualified candidate and refresh production parity and freshness before activation. Separate source validity from data validity: a small source change need not invalidate every earlier test, while unchanged code does not prove today's production data matches. Check dependencies, configuration, tools and environment as well as code. Broaden validation when those dependencies or prior evidence cannot be established.

For dbt, prefer native state selection and deferral, preserving required test coverage and coherent inputs. Keep the original manifest/results and check the applied relations before deferring to them; logical equality does not establish that a parent exists in production. A reconstructed manifest is comparison evidence, not an original run artifact. An exact-final-commit CI requirement is repository policy, not a universal dbt requirement to rebuild the whole graph. Implement evidence reuse through the project's reviewed CI path; never relabel an old run or bypass an existing guard. Do not restart useful in-flight qualification solely to add process improvements.

Keep required, optional, skipped, failed and unavailable checks distinguishable. A successful workflow does not imply that every step ran. Cancel superseded disposable CI only when interruption and cleanup are safe; do not apply that policy to production mutations. Native concurrency is scoped by its platform and configuration, not automatically a cross-repository release lock.

## Promote and recover through existing mechanisms

Verify the configured automation identity has the permissions needed for the operation. Where unattended service access exists, repair or explain that path instead of falling back to recurring personal sign-in. Do not create permanent keys, export secrets or broaden access merely to proceed.

Promote the tested artifact with versioned environment configuration. A recorded build or attestation needs verification; it does not establish functional correctness. Preserve native protection, exact-candidate checks and post-deployment acceptance. Repository validation code remains repository-owned even when it calls official vendor tools.

Prefer independently releasable changes. Keep necessary compatibility and migration ordering explicit; do not bundle an unrelated repair because it was discovered during validation. Use staged comparison or limited exposure when appropriate to the system and already authorized. A rollout mechanism is not required for every small change.

After a timeout or disconnect, inspect the native operation and resulting state before retrying. Completed and unknown effects must not be blindly replayed. Keep source validation, artifact preparation, data migration, activation and live verification separate. A code revert may leave persisted data or external effects unchanged. Board readiness, acceptance and merge cannot substitute for the user's requested live outcome.

## Evaluate improvements through observed behavior

Use a few representative tasks in an authorized test environment: a straightforward change, a stale-candidate resume, a failed required check and an interrupted external operation. Inspect commands, artifacts and outcomes; reading a skill or reporting success does not prove adherence. Keep fixtures distinct from live integration evidence.

Compare time to useful feedback and delivery, avoidable versus necessary reruns, repeated user interventions, review rounds and escaped defects. Include total agent usage when available and leave missing values unknown. Retain an improvement only when comparable evidence supports it; do not claim measured savings from a proposed workflow.

## Sources and application limits

These sources inform the guidance; they are not additional mandatory workflows or proof of performance in a particular repository.

- [DORA: small batches](https://dora.dev/capabilities/working-in-small-batches/) — independently testable delivery; avoid regrouping small changes into a large release.
- [DORA: continuous integration](https://dora.dev/capabilities/continuous-integration/) — quick feedback with longer checks in appropriate pipeline stages.
- [DORA: deployment automation](https://dora.dev/capabilities/deployment-automation/) — tested artifacts, versioned configuration and reduced deployment coupling.
- [Google SRE: canarying releases](https://sre.google/workbook/canarying-releases/) — bounded exposure and measured acceptance; adapt to the system rather than copying traffic-routing patterns into every workflow.
- [Anthropic: long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) — incremental progress and explicit resumption evidence from an engineering case study.
- [OpenAI: skill evaluations](https://developers.openai.com/blog/eval-skills) — assess actual actions and artifacts, including negative cases.
- [Google Cloud: deployment federation](https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines) — unattended access using short-lived workload credentials.

- [dbt: state and deferral](https://docs.getdbt.com/reference/node-selection/defer) — native scoped execution with separate comparison and applied state.
- [dbt: state limitations](https://docs.getdbt.com/reference/node-selection/state-comparison-caveats) — seeds, variables, macros and mixed-environment tests need explicit coverage.
