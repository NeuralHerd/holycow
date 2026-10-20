# Verification

## Choose evidence from the requirement

Connect each acceptance criterion to an observable result. Reuse the testing boundaries and decisions already agreed in the brief. Inspect existing tests, package scripts, and CI configuration to find the project's actual commands; do not invent commands or an entirely new testing framework.

If a materially new testing boundary is needed, explain what it catches and misses and resolve any architectural choice it introduces. Routine use of an existing boundary does not require another approval round.

Use focused automated tests where they protect meaningful behavior. For a bug, reproduce the failure and add a regression check at the relevant boundary when practical. For visual, configuration, or documentation changes, use the checks that actually establish correctness, including manual or browser verification where appropriate.

For behavior-preserving refactors, first capture the relevant existing behavior with characterization checks where coverage is missing. Preserve observable results, errors, and side effects. These checks should pass before and after; do not manufacture a failing test or fix an unrelated defect to justify a structural change.

## Keep the red-green cycle meaningful

For a behavior change, observe a new test fail for the intended behavioral reason before implementing it. A syntax error, missing dependency, or broken fixture is not evidence of the intended failure. If the test already passes, investigate whether the behavior exists or the test misses the problem.

Use independent expected values from accepted examples, contracts, or worked cases. Do not reproduce the implementation inside the assertion. Avoid tests that assert private call sequences or require unrelated internal structure to stay unchanged.

Mock external boundaries when useful for focused behavior tests. Record what the mock excludes; a simulated service cannot verify an actual external contract, persistence guarantee, or deployment configuration.

Identify any pivotal claim the change depends on, such as a library operation being idempotent or an old consumer tolerating a new field. Check the actual dependency version and relevant configuration. Prefer a focused executable probe against the real boundary; source reasoning can support a claim but must not be reported as runtime verification.

## Run the appropriate checks

Use targeted tests and relevant type or static checks during implementation. Before handoff, run the project's required final checks at the documented repository or package scope. Broaden testing when shared changes, failures, or unresolved risks justify it; do not repeatedly run unchanged checks without a reason.

For UI behavior, exercise the affected flow when browser tools are available, including relevant keyboard/focus behavior and loading or failure states. Inspect console or network evidence when the claim depends on it; a screenshot alone cannot establish that an action worked. If browser tools are unavailable, report the limitation and provide specific manual steps. For multi-repository contracts or migrations, verify the compatibility assumptions and relevant consumer behavior, not merely each package in isolation.

Keep the result of every required check clear: passed, failed, or not run, with the reason and practical impact. Do not call an unobserved check passing or a partial suite complete.

If an unrelated failure predates the task, identify the evidence establishing that. Without that evidence, describe the failure as unresolved rather than blaming the baseline. Do not reset the user's work to investigate.

Do not obtain a green result by skipping tests, weakening assertions, lowering budgets, or suppressing a checker. A legitimate check change must follow an accepted behavior or policy change and explain why the previous check no longer applies. Inspect such changes during review; passing a weakened gate is not evidence that the original requirement was met.

## After fixes and review

Rerun the checks invalidated by a correction. Prior results remain useful for unaffected work; changes to shared behavior may require broader revalidation.

Keep implementation complete, review complete, CI complete, and delivery complete separate. A blocked check can justify a draft handoff with clear limitations when requested, but cannot justify claiming the feature is verified.
