# Project Constitution

> Non-negotiable principles. Every spec, plan, and task must comply. When a request
> conflicts with this document, stop and raise it before proceeding.
>
> These are sensible defaults for a Django project. Adjust per project (e.g. drop DRF
> for a server-rendered app, or swap the deploy target).

## 1. Tech stack

- Language: Python 3.12+.
- Framework: Django 5.2 LTS (or 6.0 for latest). Prefer Django's built-in features
  before third-party packages (auth, sessions, tasks, CSP all ship built-in).
- API layer (when the project exposes an API): Django REST Framework.
- Settings structure: any project that will be deployed uses a settings package split by environment (`settings/base.py`, `settings/development.py`, `settings/production.py`). `production.py` always sets `DEBUG = False` and reads secrets from environment variables; environment-specific concerns (database driver options, timeouts, allowed hosts) live in the matching file, never hard-coded. A throwaway prototype that will not be deployed may use a single `settings.py`.
- Development database: independent of the above — the local/dev database is the
  developer's choice (SQLite for simplicity, or PostgreSQL via Docker to mirror
  production). Production always uses PostgreSQL, regardless of the dev choice.
- Secrets: read from environment variables (e.g. `django-environ`);
  never commit a `.env`.
- Deployment: Railway, or any other platform that supports Docker and PostgreSQL. The deploy target is not a concern of the constitution, but the plan should specify it.

## 2. Project layout & code quality

- Standard Django layout: one app per bounded domain; keep apps small and cohesive.
- Fat models / thin views; push non-trivial logic into model methods or a `services`
  module, not into views or serializers.
- Formatter + linter: `ruff` (format + lint). Code must be clean before a task is done.
- Type hints on public functions and service-layer code.
- No business logic in templates; no raw SQL unless justified in the plan.

## 3. Testing

- `pytest` + `pytest-django` (Django's test client / DRF's `APIClient`).
- Every acceptance criterion maps to at least one automated test.
- Prefer writing the test before the implementation for that criterion.
- Use factories (e.g. `factory_boy`) over static fixtures for test data.

## 4. Security baseline

- Passwords hashed by Django's auth system; Argon2 as the preferred hasher.
- Keep `DEBUG = False` outside local; `SECRET_KEY` and `ALLOWED_HOSTS` from env.
- Validate/sanitize all external input at the serializer/form boundary.
- Never store credentials or personal data in plaintext; never log secrets.
- Respect Django's CSRF, session, and (6.0+) CSP protections — don't disable them.

## 5. Process

- No implementation without an approved `spec.md` and `plan.md`.
- Every feature lives in its own `specs/NNN-feature-name/` folder.
- Migrations are reviewed like code and never edited after being applied in shared envs.
- Ambiguity is recorded as `[NEEDS CLARIFICATION: ...]`, never silently assumed.
