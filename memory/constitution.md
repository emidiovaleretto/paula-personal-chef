# Project Constitution

> Non-negotiable principles. Every spec, plan, and task must comply. When a request
> conflicts with this document, stop and raise it before proceeding.
>
> **paula-personal-chef** is a Django REST API backend with a separate React SPA
> frontend. The two are developed in one repository but are distinct applications
> that communicate over a JSON API.

## 1. Tech stack

### Backend (API)

- Language: Python 3.12+.
- Framework: Django 5.2 LTS (or 6.0 for latest). Prefer Django's built-in features
  before third-party packages (auth, sessions, tasks all ship built-in).
- API layer: Django REST Framework. The backend exposes a JSON API only — it does
  **not** render HTML pages for the product UI. All product UI lives in the frontend.
- Settings structure: any project that will be deployed uses a settings package split by environment (`settings/base.py`, `settings/development.py`, `settings/production.py`). `production.py` always sets `DEBUG = False` and reads secrets from environment variables; environment-specific concerns (database driver options, timeouts, allowed hosts, CORS origins) live in the matching file, never hard-coded. A throwaway prototype that will not be deployed may use a single `settings.py`.
- Development database: independent of the above — the local/dev database is the
  developer's choice (SQLite for simplicity, or PostgreSQL via Docker to mirror
  production). Production always uses PostgreSQL, regardless of the dev choice.
- Secrets: read from environment variables (e.g. `django-environ`); never commit
  a `.env`. Secrets and config read from environment must **fail loudly when
  missing** — never fall back to a hardcoded default value. A missing secret should
  stop the app or the affected feature, not silently substitute a baked-in value.
  Hardcoded fallbacks are how secrets and personal data leak into the repo.

### Frontend (SPA)

- Language: TypeScript. Plain JavaScript source files are not allowed for product code.
- Framework: React (function components + hooks) built with Vite.
- The frontend consumes the backend API and holds no business logic that belongs on
  the server — it is a presentation client. Server-authoritative rules (pricing,
  permissions, validation of record-of-truth data) live in the backend.
- Cross-origin requests: the allowed frontend origin(s) are configured explicitly per
  environment (CORS), never wildcarded in production.

### Shared

- Deployment: Railway, or any other platform that supports Docker and PostgreSQL. The deploy target is not a concern of the constitution, but the plan should specify it and how the SPA is served (static host / CDN vs. same origin).
- The API contract is the boundary between the two apps: a plan that changes request
  or response shapes must state the contract change explicitly.

## 2. Project layout & code quality

### Backend

- Standard Django layout under `backend/` (or the repo's designated backend root):
  one app per bounded domain; keep apps small and cohesive.
- Fat models / thin views; push non-trivial logic into model methods or a `services`
  module, not into views or serializers.
- Formatter + linter: `ruff` (format + lint). Code must be clean before a task is done.
- Type hints on public functions and service-layer code.
- No raw SQL unless justified in the plan. Validation belongs in serializers, not views.

### Frontend

- React SPA under `frontend/` (or the repo's designated frontend root).
- Linter + formatter: ESLint + Prettier. Code must be clean before a task is done.
- Keep API calls in a dedicated data/service layer (e.g. an `api/` module or hooks),
  not scattered inline in components.
- Components stay presentational and small; no duplicated server-side business logic.

## 3. Testing

### Backend

- `pytest` + `pytest-django` (Django's test client / DRF's `APIClient`).
- Use factories (e.g. `factory_boy`) over static fixtures for test data.

### Frontend

- Jest + React Testing Library for component and unit tests.

### Both

- Every acceptance criterion maps to at least one automated test (backend, frontend,
  or both, wherever the behaviour lives).
- Prefer writing the test before the implementation for that criterion.

## 4. Security baseline

- Passwords hashed by Django's auth system; Argon2 as the preferred hasher.
- Keep `DEBUG = False` outside local; `SECRET_KEY`, `ALLOWED_HOSTS`, and CORS origins from env.
- Validate/sanitize all external input at the serializer boundary; never trust the SPA.
- Never store credentials or personal data in plaintext; never log secrets.
- Respect Django's CSRF and session protections — don't disable them. The SPA
  authentication mechanism (session cookie vs. token) is decided per feature in the
  plan, and the chosen mechanism's protections (CSRF for cookies, secure token
  storage for tokens) must be honored, not bypassed.
- Never expose secrets or API keys in frontend bundle code — the SPA is public.

## 5. Process

- No implementation without an approved `spec.md` and `plan.md`.
- Every feature lives in its own `specs/NNN-feature-name/` folder.
- Migrations are reviewed like code and never edited after being applied in shared envs.
- Ambiguity is recorded as `[NEEDS CLARIFICATION: ...]`, never silently assumed.

## 6. Deployment & runtime

The deploy platform is chosen in the plan (see §1 Shared), but these runtime
invariants hold regardless of platform:

- **The container filesystem is ephemeral.** Never assume anything written to
  disk at runtime survives a redeploy. Two consequences are non-negotiable:
  - **User-uploaded media** (images, files) goes to external object storage
    (S3-compatible, Cloudinary, etc.) configured per environment — never to the
    local filesystem, which is wiped on every deploy.
  - **The database** is an external managed service (PostgreSQL per §1), never a
    file-based DB on the app container in any deployed environment.
- **Static files are collected at build time**, baked into the image — never
  generated in a pre-deploy/release step, which runs in a throwaway environment
  that is discarded before the running container starts. Static serving in
  production is handled by a dedicated mechanism (WhiteNoise, CDN, or static host
  per the plan), not by the app framework's dev server.
- Database migrations run as a release/pre-deploy step against the live database
  (which needs the runtime `DATABASE_URL`), separate from the image build.
- Custom domains and their allowed hosts / trusted origins are configured so the
  app keeps serving if an environment variable is misconfigured — the production
  domain should not depend on a single manually-set env var to respond at all.
