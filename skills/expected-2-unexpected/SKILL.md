---
name: expected-2-unexpected
description: >
  Behavioral guidelines to reduce common LLM coding mistakes. Enforces
  pre-coding assumption surfacing, minimal unbloated code, surgical diffs without
  adjacent noise, and goal-driven verification loops. Use when writing, reviewing,
  or refactoring code to avoid overcomplication and unverified changes.
license: MIT
metadata:
  author: Antigravity
  version: 1.0.0
  standard: omni-skill-v2
---

# expected-2-unexpected

Behavioral guidelines to eliminate common LLM coding mistakes.

Bias toward caution over speed. For trivial one-line tasks, use engineering judgment.

## Core Mission

Prevent common LLM failure modes before code touches disk.

Most agent failures stem from unstated assumptions, premature abstraction, accidental diff sprawl, and lack of executable verification. This skill enforces strict pre-coding clarity, radical simplicity, surgical edits, and automated verification loops.

## Impact Framing

For the consumer, features work reliably without unexpected regressions or surprise architectural changes.

For the maintainer, pull requests contain clean diffs that are easy to review and trace back to specific requirements.

## Foundational Principles

This skill operates under six core engineering principles.

1. **Laziness Protocol (`principle-laziness-protocol`).** Bias to deletion. Select the smallest change that solves the problem.
2. **Foundational Thinking (`principle-foundational-thinking`).** Pin data shapes and contracts before writing logic.
3. **Minimize Reader Load (`principle-minimize-reader-load`).** Eliminate one-caller wrappers. Keep control flow flat and readable.
4. **Prove It Works (`principle-prove-it-works`).** Never claim a fix works without running executable verification.
5. **Boundary Discipline (`principle-boundary-discipline`).** Validate inputs at external trust boundaries. Keep internal core logic pure.
6. **Test Behavior, Not Implementation (`principle-test-behavior-not-implementation`).** Assert outcomes against literal values rather than mocking internal functions.

---

## The Four Pillars

### 1. Think Before Coding

Do not assume. Do not hide confusion. Surface tradeoffs immediately.

Before implementing any request:
- State your core assumptions in plain text. If an assumption feels uncertain, ask first.
- Present multiple interpretations when ambiguity exists. Do not pick silently.
- Push back when a simpler path exists. Propose the simpler design clearly.
- Stop when requirements conflict. Name the exact conflict before proceeding.

### 2. Simplicity First

Write the minimum code that solves the problem. Never add speculative code.

Follow these hard constraints:
- Zero unrequested features.
- Zero abstractions for single-use logic.
- Zero flexibility or configuration parameters that were not requested.
- Zero defensive error handling for mathematically impossible conditions.
- If a solution takes 200 lines but could be done in 50 lines, rewrite it.

Apply the Senior Engineer Litmus Test. Ask whether a senior engineer would call this overcomplicated. If yes, strip it down.

### 3. Surgical Changes

Touch only what you must. Clean up only your own mess.

When modifying existing files:
- Do not improve adjacent code, reformat untouched lines, or rewrite existing comments.
- Do not refactor stable working routines outside the requested scope.
- Match existing repository style and formatting conventions.
- Report pre-existing dead code in your summary. Do not delete it unprompted.

When your changes create orphans:
- Remove imports, variables, and helper functions that your changes rendered obsolete.
- Keep pre-existing unused symbols intact unless the user explicitly requested cleanup.

Apply the Traceability Rule. Every changed line in your diff must trace directly to the user's explicit request.

### 4. Goal-Driven Execution

Define unambiguous success criteria. Loop until verified.

Convert every task into a verifiable target:
- "Add validation" transforms into "Write tests for invalid inputs, then make them pass."
- "Fix the bug" transforms into "Write a reproduction test, then make it pass."
- "Refactor module" transforms into "Ensure tests pass before and after the change."

For multi-step work, state a three-step plan:
```text
1. [Step 1] -> verify: [check command]
2. [Step 2] -> verify: [check command]
3. [Step 3] -> verify: [check command]
```

Strong success criteria allow autonomous progress. Weak criteria require constant intervention.

---

## The Ponytail Simplicity Ladder

Climb this ladder for every implementation decision. Stop at the first rung that holds.

1. **Does this need to exist at all?** Reject speculative requirements immediately (YAGNI).
2. **Does the codebase already have it?** Reuse existing internal helpers, utility functions, and types.
3. **Does the standard library do it?** Choose stdlib modules over external dependencies.
4. **Does the native platform cover it?** Prefer built-in language or runtime primitives over libraries.
5. **Does an installed dependency solve it?** Use packages already in the lockfile. Avoid adding new packages.
6. **Can it be a clean one-liner?** Use a concise expression if readability remains high.
7. **Only then:** Write the minimum necessary new code.

---

## Anti-Patterns and Prohibitions

| Prohibited Anti-Pattern | Why It Fails | Required Correction |
| --- | --- | --- |
| Silent assumption picking | Causes wasted work when guesses prove wrong | List assumptions explicitly before coding |
| Single-implementation interfaces | Adds cognitive overhead and indirection | Write a plain concrete class or function |
| Adjacent code reformatting | Pollutes git history and breaks git blame | Revert all untouched line edits from the diff |
| Unverified completion claims | Releases broken code into production | Run the test suite and cite terminal output |
| Premature generalized framework | Wastes time building unneeded features | Implement only the requested concrete case |
| Deleting existing dead code | Introduces accidental regression risks | Note dead code in notes without deleting it |

---

## Workflow Execution Steps

| Step | Action | Freedom | Why |
| ---: | --- | --- | --- |
| 1 | Analyze prompt and list explicit assumptions | low | Prevents misunderstandings |
| 2 | Evaluate against Ponytail ladder | low | Prevents over-engineering |
| 3 | Apply surgical edits strictly to target lines | low | Prevents diff bloat |
| 4 | Clean up newly orphaned symbols | low | Prevents code decay |
| 5 | Run executable verification command | low | Proves functional correctness |

---

## Verification and Quality Gate

Verify every deliverable against this checklist before submitting.

- [ ] Every modified line traces directly to the user's prompt.
- [ ] No adjacent formatting or comment changes exist in the git diff.
- [ ] No unrequested configuration options or abstractions were added.
- [ ] Newly orphaned imports and variables have been removed.
- [ ] An executable test or check script was executed and passed.
- [ ] Output includes terminal verification evidence.

## Progressive Disclosure

For deeper reference and automation tooling:
- **`references/heuristics.md`**: In-depth rules for simplicity and overcomplication traps.
- **`references/surgical-diffs.md`**: Diff containment protocols and AST blast radius rules.
- **`references/verification-loops.md`**: Goal formulation schemas and test patterns.
- **`scripts/verify_surgical_diff.py`**: Automated diff analyzer to check for scope sprawl.
