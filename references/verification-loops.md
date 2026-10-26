# Goal-Driven Execution and Verification Loops

This document details the transformation of user prompts into deterministic verification loops.

## Goal Formulation Standard

Never execute code changes under vague directions like "make it work" or "fix the issue".

Transform prompts into observable criteria before touching source code.

### 1. Bug Fixes
- **Naive Request.** "Fix crash when user email is missing."
- **Verifiable Formulation.** "Write a test that reproduces the crash with an empty email payload. Verify the test fails. Apply the fix. Verify the test passes."

### 2. Validations
- **Naive Request.** "Add phone number validation."
- **Verifiable Formulation.** "Define three invalid phone formats and two valid phone formats. Verify invalid formats return expected errors and valid formats succeed."

### 3. Refactoring
- **Naive Request.** "Clean up the database query module."
- **Verifiable Formulation.** "Run all existing query tests to verify baseline green status. Apply structural refactoring. Re-run tests to prove zero behavioral drift."

## Multi-Step Verification Plan

For tasks requiring more than one step, formulate a concise three-phase verification sequence:

```text
1. [Phase 1: Reproduction / Baseline]
   verify: [exact command and expected output]
2. [Phase 2: Surgical Modification]
   verify: [exact command and expected output]
3. [Phase 3: Regression and Blast Radius Audit]
   verify: [exact test command and diff check]
```

## Red-Green Falsification Requirement

A test only proves a fix when it was shown to fail before the fix was introduced.

1. Write the test asserting the expected behavior.
2. Run the test against the unmodified code. Confirm failure.
3. Apply the minimal surgical change.
4. Run the test again. Confirm pass.
5. Run the wider test suite to confirm absence of regressions.
