---
name: specify
description: Turn a natural-language feature idea into a structured spec.md — the WHAT and WHY. Use at the start of every new feature. No tech choices, no code.
argument-hint: [feature description]
---

# /specify

Create a new feature specification from `$ARGUMENTS`.

## Steps
1. Determine the next feature number (`NNN`) by scanning `specs/`. Create the folder
   `specs/NNN-short-slug/`.
2. Load `.claude/skills/specify/template.md` and fill it in from the user's idea.
3. Focus strictly on **what** and **why**: user stories, acceptance criteria, scope,
   explicit non-goals, and edge cases. Do **not** mention frameworks, libraries,
   database schemas, or code.
4. For anything underspecified, insert `[NEEDS CLARIFICATION: your question]` rather
   than assuming.
5. Save as `specs/NNN-short-slug/spec.md` and list every `[NEEDS CLARIFICATION]` back
   to the user before finishing.

## Definition of done
- Every acceptance criterion is observable and testable.
- A non-technical stakeholder could read and validate it.
