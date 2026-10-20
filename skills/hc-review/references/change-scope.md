# Selecting the reviewed state

Use the user's requested comparison. State the baseline and target so another session can reproduce the review. Validate refs as commits and record their resolved IDs. An unavailable or ambiguous target needs clarification or retrieval, not a guessed replacement such as `main`.

## Local changes

Inspect status before selecting files. Include renames, deletions, and relevant untracked files, while keeping unrelated user work outside the task.

| Requested scope | Comparison and source |
| --- | --- |
| Staged changes only | `git diff --cached`; read staged content from the index, such as `git show :path`, rather than assuming the working file matches it. |
| Unstaged tracked changes only | `git diff`; compare the index with current working files. Include untracked files only when part of the requested scope. |
| All pending task changes with a valid HEAD | `git diff HEAD` for the combined tracked result, plus relevant untracked files. Read current files to review the resulting behavior. |
| Pending work before the first commit | There is no HEAD to compare. Inspect `git diff --cached`, `git diff`, status, and relevant new files; review the resulting content without initializing history or inventing a baseline. |

Staged and unstaged versions can contain different defects. Checks run from the working tree do not necessarily validate staged-only content. State that limitation instead of stashing, resetting, or rewriting user files to manufacture a clean environment.

An empty tracked diff does not establish that there is nothing to review until the requested new files and index state are considered. If the complete selected scope is empty, report that without inventing findings.

## Commits, branches, and pull requests

For an explicit comparison of two revisions, compare those endpoints, for example `git diff <base> <target>`. For changes introduced by a branch or PR, use its verified base and head and the appropriate merge-base comparison, commonly `git diff <base>...<head>`. Three-dot comparison means merge-base to head; it is not interchangeable with an exact endpoint comparison.

For PR review, inspect the actual PR revisions through available tools or a matching local checkout. Local files from another revision are not evidence of the PR's content. Do not silently include local pending work in a committed review.

If the user includes pending changes with branch work, review the combined result against the selected baseline and include relevant new files. Avoid counting overlapping staged, unstaged, and committed hunks as separate defects.

Unmerged index entries indicate an incomplete merge. Surface that state and avoid describing a review of conflict markers or partial content as a completed review of the intended result.

## Consistency and location

Record the relevant local state or revision IDs before review and check for changes before reporting. For local files, compare contents or fingerprints; unchanged status labels do not prove that content is unchanged. For delegated reviews, ensure each reviewer examines the same content; a shared checkout may change during their work. Re-read affected files when it does.

Cite lines from the reviewed version. For deleted code, identify the old side; for new code, use the current side. Native PR comments must use locations supported by the actual diff. Missing behavior may be anchored at the narrowest relevant changed interface rather than an invented line.

Across repositories, identify each baseline and target and the contract connecting them. If one side is inaccessible, report that coverage gap instead of inferring compatibility from the other side.
