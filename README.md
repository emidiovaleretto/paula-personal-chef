# SDD Boilerplate

A starter template for building software with **Spec-Driven Development** using
Claude Code. Copy this folder to start a new project.

## Why
Instead of prompting an AI ad-hoc ("vibe coding"), you write a precise spec first.
The spec becomes a durable, reviewable contract; the AI derives the plan, tasks, and
code from it. This reduces rework, drift, and hallucinated requirements.

## The four artifacts
| File | Question it answers | Contains code? |
|------|---------------------|----------------|
| `memory/constitution.md` | What rules always apply? | No |
| `specs/NNN-*/spec.md` | What & why? | No |
| `specs/NNN-*/plan.md` | How (architecture)? | No |
| `specs/NNN-*/tasks.md` | In what order do we build it? | No |

Only `/implement` produces code, under `src/` (or your project's layout).

## Quick start
1. Run `/constitution` and fill in your stack + rules.
2. Run `/specify` with your first feature.
3. Run `/plan`, then `/tasks`, review, then `/implement`.

See `specs/001-user-login/` for a complete worked example (spec + plan + tasks).
