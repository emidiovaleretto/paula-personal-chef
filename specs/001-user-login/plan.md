# Technical plan: User login

> Stack inherited from `memory/constitution.md`: Python 3.12+, Django 5.2 LTS,
> PostgreSQL, `pytest-django`. This plan describes decisions only — no source code.

## Decisions (resolving the spec's open questions)
- **Session vs token:** use Django's built-in **session authentication** (server-side
  sessions + the session cookie). This project is server-rendered; no SPA/token need
  in v1. (If a later feature exposes a JSON API, revisit with DRF's auth.)
- **"Remember me":** out of scope for v1. Sessions use Django's default expiry.

## Approach
Reuse Django's `django.contrib.auth` rather than hand-rolling auth. Authenticate with
`authenticate()` + `login()`, hash passwords via the configured Argon2 hasher, and use
a battle-tested package for the failed-attempt lockout instead of a custom counter.

## Architecture & components
- **Custom user model** (`accounts.User`) with `email` as the `USERNAME_FIELD`
  (set from the very first migration — switching later is painful).
- **Auth backend:** Django's `ModelBackend` (email-based), plus `axes` backend for lockout.
- **Login view:** Django's built-in `LoginView` with a custom `AuthenticationForm`
  subclass that authenticates by email.
- **Lockout:** `django-axes` — configured for 5 failures per account / 15-minute cool-off.
- **Templates:** `login.html`, plus a "locked out" state; "forgot password" link points
  to Django's built-in `PasswordReset*` views (flow itself is a separate feature).

## Data model
| Entity | Key fields | Notes |
|--------|-----------|-------|
| `accounts.User` | `email` (unique, USERNAME_FIELD), `password`, `is_active` | extends `AbstractBaseUser`; password stored hashed by Django |
| `AccessAttempt` (django-axes) | username, failures, attempt_time | managed by the package; drives lockout |

## Interfaces / contracts
- `GET /accounts/login/` → renders the login form (redirects to dashboard if already authed).
- `POST /accounts/login/` → valid creds: start session + redirect to `LOGIN_REDIRECT_URL`;
  invalid: re-render form with a **generic** error; locked out: render lockout response.
- `POST /accounts/logout/` → Django's `LogoutView`, clears the session.

## Settings touched
- `AUTH_USER_MODEL = "accounts.User"`
- `PASSWORD_HASHERS` with `Argon2PasswordHasher` first
- `AUTHENTICATION_BACKENDS` includes `axes.backends.AxesStandaloneBackend`
- `AXES_FAILURE_LIMIT = 5`, `AXES_COOLOFF_TIME = 0.25` (hours), `AXES_LOCKOUT_PARAMETERS`
- `LOGIN_REDIRECT_URL`, `LOGIN_URL`

## Validation & rules
- Empty/whitespace-only email or password → form validation error, no auth attempt.
- Identical generic message for "unknown email" and "wrong password" (no user enumeration).
- Redirect authenticated users away from the login page (view-level guard).

## Security considerations
- Argon2 hashing (per constitution); rely on Django's CSRF + secure session cookies.
- Lockout via django-axes: 5 failures / account → 15 min. Never reveal whether the email exists.
- No password value in logs, error messages, or template context.

## Constitution check
- [ ] Uses Django built-ins before third-party packages (auth, sessions). ✔ (axes only for lockout)
- [ ] Argon2 hasher, secrets from env, CSRF/session protections intact.
- [ ] Every acceptance criterion has a corresponding test in `tasks.md`.
