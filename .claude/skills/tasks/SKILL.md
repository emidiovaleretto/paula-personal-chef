---
name: tasks
description: Break the active feature's plan.md into an ordered, dependency-aware, testable task list (tasks.md). Test-first ordering. No code.
argument-hint: [optional feature folder, defaults to the most recent]
---

# /tasks

Generate `tasks.md` from a feature's `plan.md`.

## Steps
1. Resolve the target feature folder; read `plan.md` and `spec.md`.
2. Load `.claude/skills/tasks/template.md`.
3. Decompose the plan into small tasks (`T001`, `T002`, ...). Each task is independently
   verifiable and references the acceptance criterion or plan section it satisfies.
4. Order by dependency; put the test task before the implementation task for each
   criterion. Mark tasks that can run in parallel with `[P]`.
5. Save as `specs/NNN-*/tasks.md`.

## Definition of done
- Every acceptance criterion has at least one task.
- Following the tasks top-to-bottom is a valid build order.
