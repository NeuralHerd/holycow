export const groups = ['Get oriented', 'Find clarity', 'Ship with confidence', 'Keep improving'] as const;

export const skills = [
  {
    name: 'holycow-guide', title: 'Find your next step.', group: 'Get oriented', symbol: '↗',
    description: 'Tell it where you are. Get a useful next step without memorizing the toolkit.',
    when: 'You have a task, but you are unsure which skill will help or whether you need a workflow at all.',
    outcome: 'A recommendation, a reason, and the result to expect. Guide reads the relevant skill definitions before recommending a route.',
    prompt: 'We have a new feature idea, but several product decisions are still open. Where should we start?',
  },
  {
    name: 'holycow-init', title: 'Give your agent the lay of the land.', group: 'Get oriented', symbol: '⌂',
    description: 'Discover repository conventions, checks, and tools. Keep the useful context close.',
    when: 'You are starting in a repository or want to audit and refresh its HolyCow setup.',
    outcome: 'Small project context, pointers to existing guidance, and a clear account of what was verified. Setup is optional for every other skill.',
    prompt: 'Inspect this repository and prepare its HolyCow context. Preserve our existing conventions and report which checks are usable.',
  },
  {
    name: 'hc-compass', title: 'Keep the big questions in view.', group: 'Find clarity', symbol: '◎',
    description: 'Turn uncertainty into a living map of questions, dependencies, decisions, and evidence.',
    when: 'A feature has consequential unknowns that will take more than one conversation to resolve.',
    outcome: 'An evolving decision map and the next question worth answering. Compass uses Refine for discussion and Lab when an experiment is needed.',
    prompt: 'Map the open questions for our export feature. Permissions are agreed, but scheduling, recovery, and storage are still open.',
  },
  {
    name: 'hc-refine', title: 'Ask better questions first.', group: 'Find clarity', symbol: '?',
    description: 'Challenge the idea, compare realistic options, and make the trade-offs explicit.',
    when: 'Requirements or product choices need discussion before you can commit to an approach.',
    outcome: 'Agreed scope and recorded decisions. Decision questions include a recommendation when the evidence supports one, with alternatives and trade-offs.',
    prompt: 'Challenge our export idea. Workspace-admin access is agreed; scheduling and failure recovery are open. Give recommendations with trade-offs.',
  },
  {
    name: 'hc-lab', title: 'Make the unknown inspectable.', group: 'Find clarity', symbol: '◇',
    description: 'Test a question with a focused prototype, experiment, or diagram before committing.',
    when: 'Discussion cannot settle a question about usability, behavior, or technical feasibility.',
    outcome: 'An inspectable experiment, observations, limitations, and a decision informed by the result. A prototype is not treated as production-ready evidence.',
    prompt: 'Prototype the two export scheduling flows so we can compare how users recover from a failed run.',
  },
  {
    name: 'hc-plan', title: 'Make the work deliverable.', group: 'Ship with confidence', symbol: '≡',
    description: 'Turn accepted decisions into a concise brief and useful delivery increments.',
    when: 'You understand the intended behavior and need a practical way to deliver it.',
    outcome: 'A brief scaled to the task and, when requested, dependency-aware tickets in your configured tracker. Unresolved decisions stay visible.',
    prompt: 'Turn the accepted export behavior into small delivery tickets in our configured tracker. Keep unresolved decisions explicit.',
  },
  {
    name: 'hc-build', title: 'Build it. Check it. Show the evidence.', group: 'Ship with confidence', symbol: '↳',
    description: 'Implement scoped work, investigate failures, and verify the behavior that matters.',
    when: 'The task is ready to implement, or you have a concrete failure to diagnose and fix.',
    outcome: 'Scoped changes or a supported diagnosis, meaningful verification, self-review, and a handoff that distinguishes completed work from remaining limits.',
    prompt: 'Fix the duplicate export created when a request is retried. Reproduce the failure, make a focused change, and verify the retry behavior.',
  },
  {
    name: 'hc-review', title: 'Catch the problems that matter.', group: 'Ship with confidence', symbol: '✓',
    description: 'Review actual changes against intent, correctness, and project standards.',
    when: 'You want a review of a PR, branch, commit, or work in progress, including uncommitted files.',
    outcome: 'Prioritized findings backed by evidence and impact, with material coverage limits. Review alone does not authorize edits or published comments.',
    prompt: 'Review the current changes against the agreed export behavior. Prioritize correctness and report any coverage limits.',
  },
  {
    name: 'hc-pr', title: 'Help reviewers see the change.', group: 'Ship with confidence', symbol: '⇄',
    description: 'Explain what changed, why it matters, and which checks support the result.',
    when: 'An implemented change needs a clear PR description grounded in the actual work.',
    outcome: 'A reviewer-ready description covering behavior, evidence, and merge risk, following the repository template and your publishing instructions.',
    prompt: 'Draft the PR description from these changes. Explain the before and after, include verification evidence, and follow our template.',
  },
  {
    name: 'hc-retro', title: 'Make the next session better.', group: 'Keep improving', symbol: '↺',
    description: 'Look at what actually happened and turn friction into a few concrete improvements.',
    when: 'A session was frustrating, a workflow failed, or you want to learn from completed work.',
    outcome: 'Supported causes, focused improvements at the right scope, and ways to evaluate them. Missing evidence and uncertain causes remain explicit.',
    prompt: 'Review this session for avoidable friction. Support each finding with evidence and recommend the smallest useful improvements.',
  },
];

export const installCommand = "npx skills@latest add NeuralHerd/holycow -g -a claude-code codex cursor --skill '*'";
