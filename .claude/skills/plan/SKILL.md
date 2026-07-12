---
name: plan
description: Turn the active feature's spec.md into a technical plan.md — the HOW. Introduces architecture and the concrete tech stack from the constitution. Still no source code.
argument-hint: [optional feature folder, defaults to the most recent]
---

# /plan

Produce `plan.md` for a feature.

## Steps
1. Resolve the target feature folder (from `$ARGUMENTS`, else the highest-numbered
   folder in `specs/`). Read its `spec.md` and `memory/constitution.md`.
2. Load `.claude/skills/plan/template.md` and fill it in.
3. Decide architecture, data model, interfaces/contracts, validation, and security —
   all consistent with the constitution's stack and rules.
4. Describe these as prose, tables, and pseudo-signatures. Do **not** write real
   implementation code here.
5. If the spec still has `[NEEDS CLARIFICATION]` items, resolve them with the user
   before planning around them.
6. Save as `specs/NNN-*/plan.md`.

## Definition of done
- Every acceptance criterion in the spec is addressed by something in the plan.
- No decision contradicts the constitution.
