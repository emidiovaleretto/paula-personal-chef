# Project memory

This repository follows **Spec-Driven Development (SDD)**. The specification is the
source of truth; code is derived from it and re-generatable.

## Workflow (run in order)
1. `/constitution` — set or update the project's non-negotiable principles.
2. `/specify <feature idea>` — create a spec (WHAT & WHY) under `specs/NNN-*/spec.md`.
3. `/plan` — turn the active spec into a technical plan (HOW).
4. `/tasks` — break the plan into an ordered, testable task list.
5. Review the spec/plan (optionally with the `spec-reviewer` subagent).
6. `/implement` — build the code, one task at a time, checking each off.

## Ground rules
- Never write implementation code before an approved `spec.md` and `plan.md` exist.
- `memory/constitution.md` overrides everything. If a spec conflicts with it, stop and flag it.
- One feature = one folder `specs/NNN-feature-name/` containing `spec.md`, `plan.md`, `tasks.md`.
- Mark unknowns as `[NEEDS CLARIFICATION: ...]` instead of guessing.

## Active tech stack
See `memory/constitution.md` (§ Tech stack). Update it per project.
