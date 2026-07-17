# Tasks: Weekly menu order

> Format: `- [ ] T00X [P?] <verb + object> — (covers: AC-n / plan §x)`
> `[P]` = can run in parallel with other `[P]` tasks in the same group (no shared files).
> AC numbers refer to the spec's acceptance-criteria list (top-to-bottom = AC-1 … AC-10).

## Setup

- [x] T001 Ensure backend project skeleton exists: Django + DRF + `django-cors-headers`, `settings/{base,development,production}` split, `pytest`/`pytest-django`/`factory_boy` configured. — (plan §Architecture, Constitution §1/§3)
- [x] T002 Create the three Django apps `accounts`, `menu`, `orders` (empty). — (plan §Architecture)
- [x] T003 [P] Scaffold the Vite + React + TypeScript SPA under `frontend/` with Jest + React Testing Library + ESLint/Prettier configured and a passing smoke test. — (Constitution §1/§2/§3)
- [x] T004 [P] Configure session auth + CSRF + CORS (credentials, configured frontend origin from env only). — (plan §Security)

## Data model & migrations

- [x] T005 Define `accounts.Client` (`user` 1–1, optional `package` choices EXPRESS/STANDARD/FULL_WEEK) + `accounts/packages.py` bounds constant `{EXPRESS:(4,5),STANDARD:(7,7),FULL_WEEK:(11,11)}`; migration. — (plan §Data model)
- [x] T006 [P] Define `menu.WeeklyMenu` (`week_start`, `is_published`, `published_at`, `is_active`) and `menu.Dish` (`weekly_menu` FK, `name`, `description`); migration. — (plan §Data model)
- [x] T007 [P] Define `orders.Order` (`client` FK, `weekly_menu` FK, `status` default `SUBMITTED`, `notes` optional, `created_at`, `UniqueConstraint(client, weekly_menu)`) and `orders.OrderItem` (`order` FK, `dish` FK, `quantity` PositiveSmallInteger ≥ 1, `UniqueConstraint(order, dish)`); migration. — (plan §Data model, AC-7)
- [x] T008 [P] Factories (`factory_boy`) for Client, WeeklyMenu, Dish, Order, OrderItem for use in tests. — (Constitution §3)

## Tests — backend service & menu resolution (write first)

- [ ] T009 [P] Test `menu.services.current_weekly_menu()`: returns the most-recently-published active menu; returns `None` when none published/active; ignores inactive/unpublished. — (AC-1, AC-2, plan §Validation "Menu authority")
- [ ] T010 [P] Test `orders.services.place_order`: valid selection within bounds creates one `Order` status `SUBMITTED` with correct items/total. — (AC-5)
- [ ] T011 [P] Test `place_order` rejects total below/above package bounds incl. empty selection (Express 4–5, Standard 7, Full Week 11). — (AC-4, AC-6, edge: below-count)
- [ ] T012 [P] Test `place_order` rejects any `dish_id` not on the current menu, and `quantity ≤ 1` / duplicate `dish_id`. — (AC-8, plan §Validation "Quantities")
- [ ] T013 [P] Test one-order-per-menu: second `place_order` for same (client, menu) is refused and surfaces the existing order; no duplicate row. — (AC-7)
- [ ] T014 [P] Test `place_order` with a client having `package = null` is refused (no-package rule). — (AC-10, edge: no package)
- [ ] T015 [P] Test `place_order` when no current menu exists is refused. — (AC-2)

## Implementation — backend services

- [ ] T016 Implement `menu.services.current_weekly_menu()`. — (makes T009 pass)
- [ ] T017 Implement `orders.services.place_order(client, items)` (transactional; all bounds/menu/quantity/no-package/one-per-menu validation). — (makes T010–T015 pass)

## Tests — backend API (write first)

- [ ] T018 [P] `GET /api/weekly-menu/current/`: `401` when unauthenticated; `200` shape (menu/package/existing_order) when a menu + package exist. — (AC-1, AC-9)
- [ ] T019 [P] `GET` returns `menu: null` when no current menu, and `package: null` when the client has no package. — (AC-2, AC-10)
- [ ] T020 [P] `GET` returns populated `existing_order` when the client already ordered this menu. — (AC-7)
- [ ] T021 [P] `POST /api/orders/`: `401` unauth; `201` + status `Submitted` on valid order. — (AC-5, AC-9)
- [ ] T022 [P] `POST` error mapping: `403` no package, `409` already ordered (returns existing), `400` no-menu / bounds / stale dish / bad quantity. — (AC-2, AC-4, AC-6, AC-7, AC-8, AC-10)

## Implementation — backend API

- [ ] T023 Serializers for menu/package/order (request `{items:[{dish_id,quantity}]}` and response shapes per plan §Interfaces). — (AC-1, AC-5)
- [ ] T024 `GET /api/weekly-menu/current/` view (`IsAuthenticated`, thin over `current_weekly_menu` + client package + existing order). — (makes T018–T020 pass)
- [ ] T025 `POST /api/orders/` view (`IsAuthenticated`, CSRF, thin over `place_order`, error→status mapping). — (makes T021–T022 pass)
- [ ] T026 Wire URLs under `/api/` and register `IsAuthenticated`/CSRF defaults. — (AC-9)

## Tests — frontend (write first)

- [ ] T027 [P] `api/weeklyMenu.ts` unit test: `getCurrentWeeklyMenu()` / `submitOrder(items)` call correct endpoints, send credentials + CSRF, parse responses. — (plan §Frontend, Constitution §2)
- [ ] T028 [P] `WeeklyMenuPage` renders the four states: menu+selector / empty ("no menu") / no-package ("contact the chef") / existing-order read-only. — (AC-1, AC-2, AC-7, AC-10)
- [ ] T029 [P] `DishSelector`: running total updates on add/remove incl. same dish twice; at package max, add is blocked with the "limit met — remove one" message. — (AC-3, AC-4)
- [ ] T030 [P] Submit flow: below required count → submit disabled/blocked with required-count message; valid count → calls `submitOrder`, shows confirmation. — (AC-5, AC-6)

## Implementation — frontend

- [ ] T031 Implement `api/weeklyMenu.ts` (the only API caller). — (makes T027 pass)
- [ ] T032 Implement `DishSelector` (local `dish→quantity` state, running total, max-block message). — (makes T029 pass, AC-3, AC-4)
- [ ] T033 Implement `OrderSummary` (read-only submitted order + confirmation). — (AC-5, AC-7)
- [ ] T034 Implement `WeeklyMenuPage` orchestration + submit wiring across the four states. — (makes T028, T030 pass)

## Polish

- [ ] T035 [P] Run `ruff` (backend) and ESLint/Prettier (frontend); fix all lint/format. — (Constitution §2)
- [ ] T036 [P] Django admin (or a management command / seed factory) to create a WeeklyMenu + Dishes + assign a Client package, so the flow is manually exercisable. — (plan: authoring out of scope but needed for manual verification)
- [ ] T037 Manual end-to-end verification of the happy path (browse → select → submit → Submitted) plus each blocked state; note results. — (all ACs)
