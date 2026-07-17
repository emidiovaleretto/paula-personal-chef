# Platform setup (Constitution §6 + §1 "Shared")

> **Not a product feature.** This is the one-time (and occasionally-revisited) platform
> and runtime setup that the deployment must satisfy *regardless of which feature is
> shipping*. It is tracked here, decoupled from any `specs/NNN-<feature>/` slice, so
> runtime/infra concerns are never baked into a feature's task list.
>
> Source of truth: `memory/constitution.md` §6 (Deployment & runtime) and §1 (Shared).
> Each task cites the invariant it satisfies. Numbered `P0xx` to keep them distinct from
> feature tasks (`T0xx`).
>
> Some items are **not yet applicable** and are marked `(N/A until …)` — they are listed
> so the trigger is known, not so they are done now.

## Deploy target & topology

- [ ] P001 Choose and record the deploy platform (Railway, or any Docker + PostgreSQL host) and how the SPA is served in production: **same-origin** vs **separate static host / CDN**. This decision drives CORS, CSRF, and static-serving choices. — (§1 Shared)
- [ ] P002 Document the resulting production topology (backend service, managed DB, SPA host/CDN, custom domain) in this folder so features can assume it. — (§1 Shared)

## Database (external, managed)

- [ ] P003 Provision PostgreSQL as an **external managed service**; app reads it via runtime `DATABASE_URL`. No file-based DB (e.g. SQLite) in any deployed environment. — (§6 "database is an external managed service")
- [ ] P004 Confirm `DATABASE_URL` (and other secrets) **fail loudly when missing** — no hardcoded fallback. — (§1 Secrets, §6)

## Migrations as a release step

- [ ] P005 Run database migrations as a **release / pre-deploy step** against the live DB (needs runtime `DATABASE_URL`), **separate from the image build**. Never run migrations at build time (throwaway env, no live DB). — (§6 "migrations run as a release/pre-deploy step")

## Static files

- [ ] P006 Collect Django static (admin + DRF browsable API assets) **at build time**, baked into the image — never generated in a pre-deploy/release step. — (§6 "static files collected at build time")
- [ ] P007 Serve production static via a dedicated mechanism (**WhiteNoise**, CDN, or static host per P001) — **not** the framework dev server. — (§6 static serving)
- [ ] P008 Build the Vite SPA (`frontend/`) as a production bundle and serve it per the P001 decision (static host/CDN, or same-origin behind the chosen static mechanism). — (§1 Shared, §6)

## Domains, hosts & resilience

- [ ] P009 Configure custom domain(s) with `ALLOWED_HOSTS` / CSRF trusted origins / CORS origins **from env per environment**, wildcard **never** used in production. — (§4, §6, §1 Frontend CORS)
- [ ] P010 Ensure the production domain keeps serving even if a single env var is misconfigured — the app's ability to respond must **not** depend on one manually-set variable. — (§6 "custom domains … keeps serving if an env var is misconfigured")

## User-uploaded media  *(N/A until a feature introduces uploads)*

- [ ] P011 `(N/A until dishes/profiles gain images or any file upload)` Route **all** user-uploaded media to external object storage (S3-compatible, Cloudinary, …), configured per environment — **never** the local container filesystem (wiped every deploy). Add this before shipping any upload feature. — (§6 "user-uploaded media goes to external object storage")

## Secrets & config

### Backend

- [ ] P012 Ensure all secrets (DB, email, object storage, etc.) are **never** hardcoded in the codebase or config files, **never** committed to the repo, and **never** logged or exposed in error messages. — (§1 Secrets)

### Frontend

- [ ] P013 Ensure no secrets (DB, email, object storage, etc.) are ever exposed in the SPA bundle or any public-facing code. Anything sensitive must stay in the backend. Frontend should only consume non-sensitive configuration values and/or what is safe to expose. — (§1 Secrets)

## Detecting misconfiguration

- [ ] P014 Ensure a pre-commit or pre-push hook runs a **configuration sanity check** that fails loudly if any required env var is missing or misconfigured or a secret is exposed. — (§1 Shared)

## HTTPS / TLS termination
- [ ] P015 Configure the **HTTPS-redirect pair together** in `production.py` once the deploy platform/proxy is known (P001): `SECURE_SSL_REDIRECT = True` **and** its companion `SECURE_PROXY_SSL_HEADER` (e.g. `("HTTP_X_FORWARDED_PROTO", "https")` for a standard TLS-terminating proxy). They **must ship as a pair** — `SECURE_SSL_REDIRECT` alone behind a TLS-terminating proxy causes an infinite redirect loop. Only set `SECURE_PROXY_SSL_HEADER` when the proxy is guaranteed to set/overwrite that header (trusting a client-supplied header otherwise is a spoofing vector). — (§6, §4)

## Notes

- The `001-weekly-menu-order` feature deliberately does **not** cover any of the above:
  `Dish` has no media, and deployment/runtime is platform-level, not feature-level.
- Revisit this checklist whenever the deploy platform changes or a feature introduces
  file uploads, a new external service, or a new public domain.
