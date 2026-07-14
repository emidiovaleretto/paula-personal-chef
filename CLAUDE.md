# Project memory

This repository follows **Spec-Driven Development (SDD)**. The specification is the
source of truth; code is derived from it and re-generatable.

## Workflow (run in order)

1. `/constitution` — set or update the project's non-negotiable principles.
2. `/specify <feature idea>` — create a spec (WHAT & WHY) under `specs/NNN-*/spec.md`.
3. `/plan` — turn the active spec into a technical plan (HOW).
4. `/tasks` — break the plan into an ordered, testable task list.
5. Review the spec/plan (optionally with the `spec-reviewer` subagent).
6. `/implement` — build the code one task at a time, checking each off, following
   the **Commit & PR flow** below.

## Commit & PR flow

**Issues → branch → PR → merge.** Keep it simple!

1. **Create an issue** for the feature or bug you're working on, using the issue template.
2. **Create a branch** for that feature or what you're working on.
3. **Work in small conventional commits** (`ci`, `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`).
4. **Open a PR** using the PR template and reference the issue in the body
   (`closes #N`).
5. **Merge** the PR. GitHub closes the linked issue automatically.

State and history live in git, Issues, and PRs — not in ad-hoc local task files or
status docs.

### Commit style

```text
type(scope): short imperative summary

Optional body explaining the why.

Optional footer with references, e.g. "closes #N", "fixes #N", "see #N".
```

- Subject in imperative mood — "add feature", not "added feature" (reads as "this
  commit will add…").
- Keep the subject line ≤ 72 characters.
- `scope` is optional; use it to name the area touched, e.g. `feat(orders):`.

### Safety rules

- Never force-push commits to `main`.
- No destructive git ops without explicit user confirmation.
- Never commit `.env` or secrets.

---

## Ground rules

- Never write implementation code before an approved `spec.md` and `plan.md` exist.
- `memory/constitution.md` overrides everything. If a spec conflicts with it, stop and flag it.
- One feature = one folder `specs/NNN-feature-name/` containing `spec.md`, `plan.md`, `tasks.md`.
- Mark unknowns as `[NEEDS CLARIFICATION: ...]` instead of guessing.

## Active tech stack

See `memory/constitution.md` (§ Tech stack). Update it per project.
