# Technical plan: Weekly menu order

> Stack inherited from `memory/constitution.md`: Django 5.2 + DRF (JSON API only, no
> server-rendered product UI), PostgreSQL in prod, `pytest-django`; React + TypeScript
>
> + Vite SPA tested with Jest + React Testing Library. This plan states decisions only
> — no source code.

## Approach

The backend derives *everything authoritative* server-side. The client never tells the
server which menu it is ordering against: the server resolves the **current weekly
menu** itself, so a stale or swapped menu can never be ordered from (covers the
"newer menu became active" and "dish removed before submit" edge cases for free).

Two endpoints carry the feature:

1. **GET current weekly menu** — returns the active menu's dishes, the client's package
   and its item bounds, and the client's existing order for that menu (if any). This
   single call gives the SPA everything it needs to render the browse view, the empty
   state, the "no package" state, and the already-ordered read-only state.
2. **POST order** — accepts a list of `{dish, quantity}`, validates against the current
   menu and the client's package, and creates exactly one `Order` in status
   **Submitted**.

The React SPA holds selection state locally (a `dish → quantity` map), shows the live
running total, and enforces the package maximum *for UX*, but the **server re-validates
every rule** — the SPA is never trusted (constitution §4).

Package rules are fixed and small, so they live as a code-level constant/service
mapping, not a database table.

## Architecture & components

### Backend (Django apps under `backend/`)

| Component | Responsibility |
|-----------|----------------|
| `accounts.Client` | Links an auth user to their meal `package`. (Assignment/management is out of scope — see spec; created via admin/factory for this slice.) |
| `accounts.packages` (module) | Fixed package definitions and their `(min, max)` item bounds. Single source of truth for counts. |
| `menu.WeeklyMenu` + `menu.Dish` | The published menu and its dishes. Authoring/publishing is out of scope; records exist via admin/factory. |
| `menu.services.current_weekly_menu()` | Resolves "the current week's menu" = most recently published, active menu (or `None`). |
| `orders.Order` + `orders.OrderItem` | The submitted order and its per-dish quantities. |
| `orders.services.place_order(client, items)` | Transactional creation + all server-side validation (single choke point). |
| DRF views/serializers | Thin HTTP layer over the two services; `IsAuthenticated`. |

### Frontend (React SPA under `frontend/`)

| Component | Responsibility |
|-----------|----------------|
| `api/weeklyMenu.ts` | `getCurrentWeeklyMenu()`, `submitOrder(items)` — the only place that talks to the API (constitution §2). |
| `WeeklyMenuPage` | Orchestrates fetch → render one of: menu+selector / empty state / no-package state / existing-order (read-only). |
| `DishSelector` | Add/remove/quantity controls; shows running total; blocks add at package max with the "limit met — remove one" message. |
| `OrderSummary` | Read-only view of a submitted order + confirmation. |

## Data model

| Entity | Fields | Notes |
|--------|--------|-------|
| `accounts.Client` | `user` (1–1 → auth user), `package` (choices: `EXPRESS`/`STANDARD`/`FULL_WEEK`, **optional**) | `empty` package = safety-rule "no package" case. Normally set at client creation (out of scope). |
| `menu.WeeklyMenu` | `week_start` (date), `is_published` (bool), `published_at` (datetime, nullable), `is_active` (bool) | "Current" = `is_published & is_active`, latest `published_at`. `week_start` set by chef at publish (Europe/Dublin). |
| `menu.Dish` | `weekly_menu` (FK), `name`, `description` | A dish belongs to exactly one weekly menu. Unlimited availability (no stock field — cook-to-order). |
| `orders.Order` | `client` (FK), `weekly_menu` (FK), `status` (choices, default `SUBMITTED`), `created_at` | **`unique_together(client, weekly_menu)`** enforces one order per menu. Only `SUBMITTED` used this slice; field sized for future `CONFIRMED`. |
| `orders.OrderItem` | `order` (FK), `dish` (FK → must belong to the order's menu), `quantity` (PositiveSmallInteger ≥ 1) | Same dish appears at most once per order; multiples expressed via `quantity`. |

Package bounds (code constant, not a table):
`EXPRESS → (4, 5)`, `STANDARD → (7, 7)`, `FULL_WEEK → (11, 11)`.
Validation rule is uniform: `min ≤ total_items ≤ max` (exact packages have `min == max`).

## Interfaces / contracts

### `GET /api/weekly-menu/current/`

+ **Auth:** required → `401` if unauthenticated.
+ **Input:** none (menu resolved server-side).
+ **Output `200`:**

  ```
  {
    menu: { id, week_start, dishes: [{ id, name, description }] } | null,
    package: { code, label, min_items, max_items } | null,
    existing_order: { id, status, created_at,
                      items: [{ dish_id, dish_name, quantity }],
                      total_items } | null
  }
  ```

  + `menu: null` → "no menu available this week" empty state.
  + `package: null` → client has no package → SPA shows "contact the chef" (ordering disabled).
  + `existing_order` present → SPA renders read-only summary, hides the selector.

### `POST /api/orders/`

+ **Auth:** required → `401`.
+ **Input:** `{ items: [{ dish_id, quantity }] }` (menu is *not* accepted from the client).
+ **Output `201`:** the created order (same shape as `existing_order` above), `status = "Submitted"`.
+ **Errors (JSON body with a clear message):**

  | Status | Condition |
  |--------|-----------|
  | `401` | Not authenticated. |
  | `403` | Client has no package assigned → "contact the chef". |
  | `409` | Client already has an order for the current menu → returns the existing order. |
  | `400` | No current menu published; total items outside package bounds (incl. empty selection); any `dish_id` not on the current menu; `quantity ≤ 0`. |

All order creation flows through `orders.services.place_order(...)` inside a DB
transaction so a rejected order leaves nothing behind.

## Validation & rules

+ **Login required** on both endpoints (`IsAuthenticated`).
+ **Menu authority:** the current menu is resolved server-side; every submitted
  `dish_id` must belong to *that* menu, else `400` (covers stale/removed dishes).
+ **One order per menu:** DB `unique_together(client, weekly_menu)` + a pre-check in the
  service returning `409` with the existing order (no duplicate creation on race).
+ **Package bounds:** `total = Σ quantity`; require `min ≤ total ≤ max` for the client's
  package. Empty/zero selection fails the lower bound → `400`.
+ **Quantities:** each `quantity ≥ 1`; a dish may appear once per payload (quantities
  express repeats). Duplicate `dish_id` entries are rejected or summed → **rejected** for
  simplicity and predictability.
+ **No package → cannot order** (`403`); surfaced on GET as `package: null`.
+ **Menu rollover:** because the menu is resolved per-request, a selection built against
  an old menu simply fails validation against the new current menu; the SPA re-fetches
  and shows the new menu (matches spec's "discard and show new menu").

## Security considerations

+ **Auth mechanism:** Django **session authentication** (built-in, per constitution's
  "prefer built-ins") with the SPA sending credentials; **CSRF enforced** on the POST
  (session cookie + `X-CSRFToken`). CORS allows only the configured frontend origin(s)
  per environment, with credentials — never wildcard in prod. (Login itself is a
  separate feature; this plan only consumes `request.user`.)
+ **Ownership:** a client can only read/create *their own* order; `existing_order` and
  `place_order` are always scoped to `request.user`'s `Client`. No order id is ever
  taken from the client to fetch someone else's order.
+ **Input validation** at the serializer boundary (dish ids, quantities, shapes);
  services never trust pre-validated-by-SPA data.
+ **No secrets in the SPA bundle**; no personal data logged. Env config fails loudly if
  missing (constitution §1).
+ Prices/payment are out of scope, so no money handling surface here.

## Constitution check

+ [ ] Backend is JSON API only; all UI in the React SPA. ✔ (two JSON endpoints, no templates)
+ [ ] Django built-ins preferred (auth/session/CSRF); third-party only if justified. ✔ (`django-cors-headers` is the one justified add for the split-origin SPA)
+ [ ] Fat models/services, thin views; validation in serializers/services, not views. ✔
+ [ ] TypeScript SPA, API calls isolated in an `api/` layer, small presentational components. ✔
+ [ ] Every acceptance criterion has a test (backend `APIClient` and/or Jest + RTL). ✔ (mapped in `tasks.md`)
+ [ ] Argon2/secrets-from-env/CSRF/session protections respected; SPA never trusted. ✔
+ [ ] PostgreSQL in prod; migrations reviewed; one app per bounded domain. ✔

## Acceptance-criteria coverage (spec → plan)

| Spec AC | Covered by |
|---------|-----------|
| See menu + package + required count | GET `weekly-menu/current` response |
| No menu → empty state, cannot order | `menu: null`; POST returns `400` no-menu |
| Running total as items added/removed | SPA `DishSelector` local state |
| Blocked at package max with message | SPA max-block + server `400` on `total > max` |
| Valid count → order Submitted + confirmation | POST `201`, `status = Submitted`, `OrderSummary` |
| Count not satisfied → submit blocked, told required count | server `400` (bounds), message states required count |
| Already ordered → shows existing, no 2nd order | `existing_order` in GET; POST `409`; `unique_together` |
| Dish not on current menu → rejected | server-side menu resolution + per-dish `400` |
| Not logged in → denied | `IsAuthenticated` → `401` on both endpoints |
| No-package client → blocked, contact chef | `package: null` on GET; POST `403` |
