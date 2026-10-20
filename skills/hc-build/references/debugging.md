# Debugging

Use this guidance for a reported bug, performance regression, or unexplained failure. Scale the investigation to the uncertainty; an obvious, reproducible defect does not need a fixed number of hypotheses or a separate planning ceremony.

## Establish the actual failure

Identify expected and observed behavior, the triggering inputs and conditions, and the evidence already available. Read relevant code and logs to locate the failing path and construct a useful check. Distinguish the user's symptom from unrelated setup errors or a nearby failing test.

Prefer an existing test, API or CLI invocation, browser flow, or focused harness that exercises the real failure path. Run it and record the specific observation that distinguishes failure from success. A command that merely exits successfully is insufficient if it cannot detect the reported bug.

Use the permitted environment and representative data. Replays, stress tests, and production instrumentation must stay within existing authorization and operational constraints. Keep credentials and sensitive payloads out of commands, diagnostic output, and shared artifacts; retain only the evidence needed to understand the failure.

For intermittent failures, record attempts, observed failures, and relevant timing or state. Where practical, control clocks, seeds, or scheduling to make the signal clearer. Use bounded repeated trials; one successful run does not establish that an intermittent bug is fixed.

If reproduction is unavailable, report what was tried and what evidence or access is missing. Source inspection can narrow possibilities, but label untested explanations as hypotheses. Recommend the smallest next probe or missing input instead of claiming a confirmed cause or applying speculative fixes.

## Narrow the cause

Reduce the reproducer where useful, changing one input or condition at a time while checking that the same symptom remains. Preserve the original scenario for final verification. Do not simplify away the caller sequence, timing, or integration behavior that makes the bug possible.

Consider plausible competing explanations. For each useful hypothesis, state a prediction and a probe that could distinguish it from the others. Share the leading explanation and next probe when the investigation is substantial; continue authorized work without requiring another approval for each routine probe.

Prefer debugger inspection, targeted logs, traces, or focused experiments at the relevant boundary. Each probe should answer a specific question. Change one causal variable at a time when feasible and record confounding changes when it is not. Revise the explanation when evidence contradicts it rather than layering more patches onto an unsupported theory.

Use revision or configuration comparison when it helps isolate a regression, while preserving the user's current work. Do not reset the checkout, start a history-changing investigation, or create another checkout contrary to the user's repository workflow.

Track temporary instrumentation and fixtures introduced by this investigation so they can be cleaned up without removing existing diagnostics or other work.

## Measure performance problems

Establish a baseline for the affected workload before optimizing. Use timings, a profiler, query plans, or appropriate runtime measurements to locate the bottleneck. Compare like workloads and conditions, including data size, concurrency, and cold versus warm state.

Repeat measurements enough to expose relevant variation and report the conditions and observed results. Use an agreed target when one exists; otherwise describe the measured change without inventing a performance requirement. Faster execution must still preserve the required behavior.

## Verify the correction or hand off the diagnosis

When a fix is requested and the cause is supported, make the smallest correction and use the existing [verification guidance](verification.md). Put regression coverage at a boundary that exercises the actual failure pattern. A helper test that omits the triggering interaction cannot establish that the original bug is fixed.

Re-run the original scenario as well as the focused regression check. For intermittent or performance issues, compare relevant trials or measurements under equivalent conditions and retain uncertainty where the evidence is limited. Explain any missing regression coverage or unavailable integration check.

Remove only temporary instrumentation and artifacts introduced for this investigation that are no longer needed. Preserve useful regression fixtures and any diagnostics the user asked to keep. Recheck affected behavior after cleanup.

Report the supported causal explanation, decisive evidence, correction if applied, verification results, and remaining limits. For diagnosis-only work, return the findings and recommended next action without proceeding to implementation or publication.
