---
name: constitution
description: Create or update memory/constitution.md — the project's non-negotiable principles (stack, quality, testing, security, process). Use once at project start and whenever a rule changes.
argument-hint: [what to add or change]
---

# /constitution

Maintain `memory/constitution.md` as the single source of truth for project rules.

## Steps
1. Read the current `memory/constitution.md` if it exists.
2. Apply the change described in `$ARGUMENTS` (or, if empty, interview the user
   section by section: stack, code quality, testing, security, process).
3. Keep principles concrete and testable ("functions under 50 lines"), not vague
   ("write clean code").
4. Write the updated file. Show a diff-style summary of what changed and why.

## Guardrails
- Do not add rules the user did not agree to.
- Flag any existing spec/plan that would now violate an updated principle.
