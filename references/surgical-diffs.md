# Surgical Diff Discipline and Blast Radius Control

This document governs how code modifications must be scoped and bounded.

## The Diff Containment Protocol

Every modification must maintain a tight blast radius.

### 1. Zero Adjacent Drift
- Do not fix indentation on lines outside your target block.
- Do not convert quotes or formatting styles in surrounding code.
- Do not rewrite adjacent comments to sound better.
- Do not change variable naming conventions in functions you were not asked to edit.

Violations pollute `git blame` and obscure the genuine intent of the pull request.

### 2. Orphan Management
When editing code, your modifications may render previous symbols unused:
- Identify newly unused `import` statements and remove them.
- Identify local variables that are no longer referenced and delete them.
- Identify internal helper functions that lost their sole caller due to your changes and remove them.

**Pre-Existing Dead Code Rule.** If an unused symbol existed before your changes, leave it untouched. Report it to the user in your response summary. Never delete unrequested code.

### 3. Traceability Test
For every line present in `git diff`, answer this question:
"Which specific phrase or requirement in the prompt demanded this line?"

If a line exists only because of personal aesthetic preference or unrequested cleanups, revert that line immediately.

## Automated Diff Audit Rules

| Diff Pattern | Status | Action Required |
| --- | --- | --- |
| Target bugfix logic | Allowed | Keep |
| Target feature implementation | Allowed | Keep |
| Removal of newly orphaned import | Allowed | Keep |
| Formatting edits on untouched functions | Forbidden | Revert immediately |
| Deletion of pre-existing unused functions | Forbidden | Revert and mention in report |
| Renaming unrequested parameters | Forbidden | Revert to existing naming |
| Adding unrequested abstraction layers | Forbidden | Flatten to direct concrete call |
