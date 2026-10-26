# Engineering Heuristics and Simplicity Doctrine

This reference provides concrete decision rubrics to identify overcomplication and enforce minimal design.

## The Ponytail Simplicity Hierarchy

When implementing logic, evaluate solutions in strict order.

```text
[Step 1] Question Necessity (YAGNI)
   ↓
[Step 2] Existing Codebase Helpers
   ↓
[Step 3] Standard Library Functions
   ↓
[Step 4] Platform / Runtime Features
   ↓
[Step 5] Already Installed Dependencies
   ↓
[Step 6] Concise One-Liner
   ↓
[Step 7] Minimal Custom Logic
```

Never skip a higher rung when it satisfies the requirements.

## Overcomplication Detection Rubric

Review your proposed implementation against these red flags.

### 1. Speculative Configurability
- Adding function parameters that only have one sensible value.
- Introducing configuration files or environment variables for internal constants.
- Providing generic options that no current requirement needs.

**Rule.** Hardcode the constant directly. Expose a configuration parameter only when two distinct callers require different values today.

### 2. Premature Abstraction
- Defining an interface or protocol with only one implementing class.
- Creating abstract factory classes for single object instantiation.
- Wrapping a simple third-party or stdlib call in an internal wrapper class that merely forwards arguments.

**Rule.** Use concrete functions and plain data structures until multiple concrete implementations exist.

### 3. Ghost Error Handling
- Catching exceptions that cannot physically be thrown by the invoked code.
- Adding complex retry loops for synchronous in-memory calculations.
- Checking for null or undefined on variables guaranteed non-null by internal type systems.

**Rule.** Validate strictly at the system boundaries. Trust internal verified types.

### 4. Excessive File Proliferation
- Splitting a 30-line cohesive logic flow across four separate files.
- Creating standalone files for single-line type aliases.

**Rule.** Co-locate closely related logic. Extract to a separate module only when multiple independent packages import it.

## The Senior Engineer Question

Before presenting a solution, evaluate this question:
"Would a senior engineer consider this implementation over-engineered?"

If the answer is yes, reduce the code immediately:
- Collapse one-caller functions back into the main flow.
- Replace hand-rolled algorithms with standard library utilities.
- Delete unused flags, enums, and speculative error branches.
