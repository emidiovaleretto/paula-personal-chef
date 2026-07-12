---
name: implement
description: Execute a feature's tasks.md — write the actual code and tests, one task at a time, honoring spec.md, plan.md, and the constitution. This is the only skill that produces source code.
argument-hint: "optional feature folder, defaults to the most recent"
---

# /implement

Build the feature by working through its `tasks.md`.

## Steps
1. Resolve the target feature folder; read `tasks.md`, `plan.md`, `spec.md`, and
   `memory/constitution.md`.
2. Work strictly in task order. For each task:
   a. State which task you are doing.
   b. Make the smallest change that completes it.
   c. Run the relevant tests if a test runner is configured.
   d. Check the box in `tasks.md`.
3. Stop and ask if a task is blocked by an unresolved `[NEEDS CLARIFICATION]` or a
   conflict with the constitution.
4. When done, summarize what was built and which acceptance criteria are now met.

## Guardrails
- Do not add features not present in the spec.
- Do not skip the test tasks.
- When a task introduces a new Django app, verify it is registered in
  `INSTALLED_APPS` before writing code that depends on it (views, models, tests). An unregistered app fails silently: tests aren't discovered, migrations aren't made.
