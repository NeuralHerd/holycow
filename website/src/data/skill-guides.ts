export interface SkillGuide {
  intro: string;
  steps: [string, string][];
  exampleTitle: string;
  prompt: string;
  response: { title: string; body: string; points?: string[]; outcome: string };
  note: string;
  next: { skill: string; label: string };
  examples: { label: string; prompt: string; result: string; skill?: string }[];
}

export const skillGuides: Record<string, SkillGuide> = {
  'holycow-guide': {
    intro: 'Not sure which skill to use? Tell Guide what you’re working on. It suggests a useful next step and explains why.',
    steps: [['Describe your task', 'Your goal, what’s done, and what’s stuck.'], ['Get a recommendation', 'One useful skill, with a reason.'], ['Choose your next move', 'Use that skill or keep discussing.']],
    exampleTitle: 'Try it with an idea',
    prompt: 'We want to add CSV exports. We haven’t decided who can use them. Where should we start?',
    response: { title: 'Start with hc-refine.', body: 'Decide who can export before planning the build.', outcome: 'You’ll leave with agreed permissions and scope.' },
    note: 'You choose when to continue.',
    next: { skill: 'hc-refine', label: 'See how to use hc-refine' },
    examples: [
      { label: 'A bug to fix', prompt: 'Retrying an export creates duplicates. Where should I start?', result: 'Reproduce it, fix it, verify it.', skill: 'hc-build' },
      { label: 'Code ready to review', prompt: 'My changes are ready. What should I do next?', result: 'Check the actual changes.', skill: 'hc-review' },
    ],
  },
  'holycow-init': {
    intro: 'New to a repository? Init finds its conventions, useful commands, and tools, then saves the context your agent needs.',
    steps: [['Inspect the project', 'Read existing guidance, scripts, and setup.'], ['Keep useful context', 'Link the conventions that already exist.'], ['Check what works', 'Report verified checks and any gaps.']],
    exampleTitle: 'Try it in a repository',
    prompt: 'Prepare this repository for HolyCow. Preserve our conventions and check which verification commands work.',
    response: { title: 'Project context is ready.', body: 'Saved the repository guidance and check commands in docs/agents/holycow.md.', outcome: 'Build verified. Tracker access still needs checking.' },
    note: 'Setup is optional for every other skill.',
    next: { skill: 'holycow-guide', label: 'Choose your next step' },
    examples: [
      { label: 'Inspect without editing', prompt: 'Audit our HolyCow setup. Report gaps without changing files.', result: 'A short list of what works, what’s missing, and what to fix.' },
      { label: 'Refresh existing context', prompt: 'Our test commands changed. Refresh the project context and preserve my notes.', result: 'Updated commands and pointers, with your notes kept.' },
    ],
  },
  'hc-compass': {
    intro: 'Too many open questions to settle in one chat? Compass keeps a map of decisions, dependencies, and the next question worth answering.',
    steps: [['Name the unknowns', 'What must you learn or decide?'], ['Resolve one question', 'Discuss, research, or try an experiment.'], ['Update the map', 'Save the evidence and pick what’s next.']],
    exampleTitle: 'Try it with a larger feature',
    prompt: 'Map the open questions for scheduled exports. Admin-only access is agreed; delivery, storage, and retries are still open. Keep the map in local Markdown.',
    response: { title: 'Start with how exports are delivered.', body: 'That choice affects where files live and how failed deliveries recover.', points: ['Decided: workspace admins only.', 'Ready: download link or email attachment?', 'Waiting: storage and retry behavior.'], outcome: 'A decision map you can resume in the next session.' },
    note: 'Keep unresolved questions on the map.',
    next: { skill: 'hc-refine', label: 'Discuss the next question' },
    examples: [
      { label: 'Resume an effort', prompt: 'Resume our export decision map. What is ready to resolve next?', result: 'The next unblocked question, using the decisions already recorded.' },
      { label: 'Start without a repository', prompt: 'We want a tool for community event organizers. Map what we need to learn before choosing a direction.', result: 'Questions about people, problems, and outcomes before choosing technology.' },
    ],
  },
  'hc-refine': {
    intro: 'Have an idea with unanswered questions? Refine helps you compare options, challenge assumptions, and agree what to build.',
    steps: [['Share the idea', 'Who is it for, and what should it do?'], ['Discuss the choices', 'Get a recommendation and trade-offs.'], ['Agree the scope', 'Confirm decisions and what stays out.']],
    exampleTitle: 'Try it with an open decision',
    prompt: 'Refine our CSV export idea. Workspace-admin access is agreed. Should exports include archived records?',
    response: { title: 'Which records should the export include?', body: 'Choose the scope before planning the work.', points: ['Current records only · Recommended. Matches the current view; leaves out history.', 'Current and archived records. Supports historical analysis; adds records outside the view.'], outcome: 'Your answer becomes an agreed requirement.' },
    note: 'You make the decisions.',
    next: { skill: 'hc-lab', label: 'Need evidence? Try a prototype' },
    examples: [
      { label: 'Challenge an assumption', prompt: 'We assume every export needs scheduling. Challenge that before we commit.', result: 'A discussion of the actual need and simpler options.' },
      { label: 'Settle an edge case', prompt: 'Admin-only exports are agreed. What should happen if access is removed during an export?', result: 'A concrete decision about the permission boundary and user experience.' },
    ],
  },
  'hc-lab': {
    intro: 'Can’t settle a question by talking? Lab makes a prototype, experiment, or diagram you can inspect before committing to an approach.',
    steps: [['Choose a question', 'Name what the experiment should reveal.'], ['Make it testable', 'Build only enough to try the idea.'], ['Inspect and decide', 'Use the result to choose what comes next.']],
    exampleTitle: 'Try it with a design choice',
    prompt: 'Prototype two export scheduling flows: a guided setup and a single form. Let us compare how easy they are to use.',
    response: { title: 'Two flows are ready to try.', body: 'Create a weekly export in each version, then change its delivery time.', outcome: 'Compare clarity and effort. Scheduling is simulated.' },
    note: 'A prototype needs further work before production.',
    next: { skill: 'hc-build', label: 'Accepted a direction? Build it' },
    examples: [
      { label: 'Explain a flow', prompt: 'Draw an editable diagram of the export retry flow so we can discuss failure recovery.', result: 'A diagram showing states, decisions, and open questions.' },
      { label: 'Test a behavior', prompt: 'Make a small runnable experiment to compare two ways of preventing duplicate exports.', result: 'Observed results and limits you can use to choose an approach.' },
    ],
  },
  'hc-plan': {
    intro: 'Know what you want to build? Plan turns agreed decisions into a short brief or small delivery tickets with clear checks for success.',
    steps: [['Bring the decisions', 'Share the agreed scope and evidence.'], ['Break down delivery', 'Define useful, verifiable increments.'], ['Hand off ready work', 'Include checks, dependencies, and blockers.']],
    exampleTitle: 'Try it with agreed scope',
    prompt: 'Plan admin-only CSV exports of current records. Retrying must not create duplicates. Draft small delivery tickets here; scheduling is out of scope.',
    response: { title: 'Two delivery tickets, with clear checks.', body: 'Keep each ticket focused on behavior a reviewer can verify.', points: ['Export current records: admins can download a CSV; other users are denied.', 'Make retries safe: repeating the request returns the same export. Depends on the first ticket.'], outcome: 'Draft tickets with scope, acceptance criteria, and dependencies.' },
    note: 'A short brief may be enough; tickets are optional.',
    next: { skill: 'hc-build', label: 'Implement the ready work' },
    examples: [
      { label: 'Keep a small task small', prompt: 'Write a brief for adding an empty-state message to exports. We don’t need separate tickets.', result: 'One concise brief with the behavior and how to verify it.' },
      { label: 'Keep unknowns visible', prompt: 'Plan the agreed manual export. Leave scheduled exports blocked until we decide the delivery method.', result: 'Ready work stays separate from work with an unresolved decision.' },
    ],
  },
  'hc-build': {
    intro: 'Ready to implement, or have a bug to fix? Build makes focused changes, checks the behavior, and shows what was verified.',
    steps: [['Understand the task', 'Read the requirements or reproduce the bug.'], ['Make the change', 'Follow the project’s existing conventions.'], ['Verify and review', 'Check the outcome and report the evidence.']],
    exampleTitle: 'Try it with a bug',
    prompt: 'Fix the duplicate export created when a request is retried. Reproduce the failure, make a focused change, and verify the retry behavior.',
    response: { title: 'Retries now reuse the existing export.', body: 'Reproduced the duplicate, corrected the retry handling, and reviewed the change.', outcome: 'The retry check fails before the fix and passes after it.' },
    note: 'A clear task can go straight to Build.',
    next: { skill: 'hc-review', label: 'Review the changes' },
    examples: [
      { label: 'Implement agreed behavior', prompt: 'Add the agreed empty state: “No exports yet” and a button to create one. Verify the flow.', result: 'The implemented state, checked against the agreed behavior.' },
      { label: 'Investigate first', prompt: 'Find why large exports time out. Diagnose the cause without changing code.', result: 'A supported diagnosis and the next useful check or fix.' },
    ],
  },
  'hc-review': {
    intro: 'Have changes ready to inspect? Review checks the actual code against the intended behavior and project standards, then reports the problems that matter.',
    steps: [['Choose the changes', 'Point to a PR, branch, commit, or local work.'], ['Trace the behavior', 'Check intent, correctness, and conventions.'], ['Act on findings', 'Get evidence, impact, and a focused fix direction.']],
    exampleTitle: 'Try it on local changes',
    prompt: 'Review my uncommitted export changes. Only workspace admins should be able to create exports. Prioritize correctness; do not edit files.',
    response: { title: 'High priority: check permissions on the server.', body: 'The button is hidden for members, but a direct API request can still create an export.', outcome: 'Add the server-side permission check and verify member access is denied.' },
    note: 'Review alone leaves files and published comments unchanged.',
    next: { skill: 'hc-build', label: 'Fix a confirmed finding' },
    examples: [
      { label: 'Review a branch', prompt: 'Review this branch against main for retry safety. Report findings and anything you could not verify.', result: 'Prioritized findings tied to the branch’s actual changes.' },
      { label: 'Review against a decision', prompt: 'Review these changes against our decision to export current records only.', result: 'Evidence of whether the implementation matches the agreed scope.' },
    ],
  },
  'hc-pr': {
    intro: 'Need to explain a change to reviewers? PR turns the actual diff and check results into a concise description of what changed, why, and the risks.',
    steps: [['Read the changes', 'Use the actual diff and agreed intent.'], ['Explain the result', 'Show before, after, and verification.'], ['Return or publish', 'Draft or update the PR as requested.']],
    exampleTitle: 'Try it with a finished fix',
    prompt: 'Draft a PR description for this export retry fix. Use the actual diff and test results, follow our template, and keep it concise.',
    response: { title: 'Prevent duplicate exports on retry', body: 'Repeated requests now reuse the existing export instead of creating another.', points: ['Evidence: the retry regression check passes.', 'Merge risk: changes request reuse; existing exports stay intact.'], outcome: 'A draft grounded in the change and its observed checks.' },
    note: 'Ask explicitly when you want the PR created or updated.',
    next: { skill: 'hc-review', label: 'Need a review of the code?' },
    examples: [
      { label: 'Update an existing PR', prompt: 'Update this PR description to match the latest changes and checks. Preserve the relevant human-written context.', result: 'An updated description, verified against the actual PR.' },
      { label: 'Explain a small change', prompt: 'Draft a brief PR description for this empty-state copy fix. Mention what was checked.', result: 'A proportionate explanation without unnecessary sections.' },
    ],
  },
  'hc-retro': {
    intro: 'Want the next session to go better? Retro looks at what happened, finds the causes of friction, and recommends a few practical improvements.',
    steps: [['Look at the evidence', 'Use the session, corrections, and results.'], ['Find the cause', 'Separate observed problems from guesses.'], ['Choose an improvement', 'Fix the smallest useful thing and evaluate it.']],
    exampleTitle: 'Try it after a difficult session',
    prompt: 'Review this session for avoidable friction. We repeatedly used the wrong test command. Find the cause and recommend a small improvement.',
    response: { title: 'Correct the stale command in project guidance.', body: 'The setup notes point to the old command; the current package script uses a different one.', outcome: 'Update the source note, then check that the next session finds and runs the right command.' },
    note: 'Recommendations stay proposals until you ask to apply them.',
    next: { skill: 'hc-build', label: 'Apply an agreed improvement' },
    examples: [
      { label: 'Keep what worked', prompt: 'Review this session. Which practices helped, and which caused avoidable rework?', result: 'Evidence-backed lessons, including useful practices to keep.' },
      { label: 'Evaluate a previous change', prompt: 'Compare this session with our last retrospective. Did the new check catch the problem it was meant to catch?', result: 'Observed improvement or remaining uncertainty, without assuming success.' },
    ],
  },
};
