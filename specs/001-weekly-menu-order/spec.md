# Feature: Weekly menu order

## Summary

Each week the chef publishes a menu of available dishes. A logged-in client needs to
browse the current week's published menu, choose the dishes they want (in the
quantities their meal package allows), and submit a single order to the chef. This
gives the chef a clear, per-client prep list for the week and gives the client a
simple, self-service way to make their weekly selections. A client may hold only
**one** order per weekly menu. This slice is the **happy path only**: browse → select
→ submit, ending in an order with status **Submitted**. Editing, confirmation, and
resubmission are explicitly deferred to a later feature.

## Meal packages

A client belongs to one of three fixed packages, which sets how many items (total
dishes/servings for the week) their order must contain:

| Package    | Required item count |
|------------|---------------------|
| Express    | 4 or 5 items        |
| Standard   | exactly 7 items     |
| Full Week  | exactly 11 items    |

The count is a **total across the whole order**. The client picks quantities freely —
the same dish may be chosen multiple times — as long as the total stays within the
package's allowance. "Item" means one serving of a dish; choosing a dish twice counts
as two items.

## User stories

- As a logged-in client, I want to see the current week's published menu, so that I
  know which dishes I can choose from this week.
- As a client with a meal package, I want to select dishes and quantities up to my
  package's item count, so that I get exactly what my plan entitles me to.
- As a client, I want to submit my selections as a single order to the chef, so that
  the chef knows what to prepare for me this week.
- As a client, I want to be prevented from placing a second order for the same weekly
  menu, so that my order stays unambiguous and the chef isn't sent conflicting requests.
- As a client, I want to see the order I already submitted, so that I can confirm what
  I asked for.

## Acceptance criteria

- [ ] Given I am logged in and a menu is published for the current week, when I open
  the weekly menu, then I see the list of dishes available for that week, my package,
  and my package's required item count.
- [ ] Given I am logged in and **no** menu is published for the current week, when I
  open the weekly menu, then I see a clear "no menu available this week" state and
  cannot place an order.
- [ ] Given I am viewing the current week's menu, when I add dishes (including the same
  dish more than once), then my running item total is shown and updates as I add or
  remove items.
- [ ] Given my running item total has reached my package's maximum, when I try to add
  another item, then the addition is blocked and I am shown a message that the limit is
  met and that I must remove an item before adding another.
- [ ] Given my selection totals a valid count for my package (Express 4 or 5; Standard
  exactly 7; Full Week exactly 11), when I submit, then an order with status
  **Submitted** is created for me against the current weekly menu, and I see a
  confirmation of exactly what I ordered.
- [ ] Given my selection total does **not** satisfy my package's required count, when I
  attempt to submit, then submission is blocked and I am told what count my package
  requires.
- [ ] Given I am composing my order, when I add optional free-text notes (allergies,
  dietary restrictions, or preferences) and submit, then the notes are saved with my
  order and shown back to me; submitting with no notes is equally valid.
- [ ] Given I have already submitted an order for the current weekly menu, when I view
  the menu again, then I see my existing submitted order and I am **not** offered a way
  to create a second order for that menu.
- [ ] Given I submit a selection that references a dish not on the current published
  menu, when the order is processed, then the order is rejected with a clear error.
- [ ] Given I am not logged in, when I try to view the weekly menu or place an order,
  then I am denied access.

## Scope

### In scope

- Viewing the current week's published menu (dishes, the client's package, and its
  required item count).
- Selecting dishes and quantities, with a live running item total.
- Blocking additions once the package maximum is reached, with an explanatory message.
- Submitting exactly one order per client per weekly menu, ending in status **Submitted**.
- Optionally attaching free-text **notes** to the order (allergies, dietary restrictions,
  or preferences for that specific order). Notes are optional — an order with no notes
  is perfectly valid.
- Enforcing on submit: the item total satisfies the package (Express 4–5, Standard 7,
  Full Week 11), all dishes belong to the current published menu, login is required,
  and only one order per weekly menu exists.
- Viewing the order the client already submitted for the current weekly menu.

### Out of scope (non-goals)

- **Editing or cancelling an order after submission**, the Submitted → Confirmed
  transition, and resubmission — all a separate feature.
- **Any weekly ordering deadline / cut-off**, and the 48-hour edit grace period — they
  belong to the order-editing feature, not this one.
- The chef's authoring/publishing of the weekly menu (assumed to already exist or a
  separate feature).
- Assigning or managing which meal package a client has (assumed to already exist).
- Payment, billing, or invoicing for the order.
- Chef-side order management (accept/decline/fulfil), notifications, or prep lists.
- Delivery/scheduling logistics.
- Ratings, favourites, or reordering from a previous week.

## Edge cases & error states

- No published menu for the current week → informative empty state, ordering blocked.
- Selection total below the package's required count → submission blocked with a
  message stating the required count (this also covers an empty/zero-item selection,
  which is never submittable).
- Adding an item beyond the package maximum → blocked with the "limit met, remove one
  to add another" message.
- A dish is removed from the menu between viewing and submitting → order rejected for
  the stale dish with a clear message.
- Client attempts a second order for the same weekly menu → blocked, existing submitted
  order shown.
- Client has no meal package assigned → blocked from ordering, shown a message to
  contact the chef. (The chef always assigns a package at client creation — a required
  field — so this should not occur in practice; this is the safety rule.)
- A newer menu becomes the active one while the client is mid-selection → the
  in-progress selection against the old menu is discarded and the client is shown the
  new current menu. (Rare; intentionally not over-engineered.)

## Resolved decisions

- Package limit counts total items (dishes/servings) for the week: Express 4–5,
  Standard exactly 7, Full Week exactly 11.
- The same dish may be selected multiple times; each serving counts as one item.
- At the package maximum, adding is blocked with a "limit met — remove one to add
  another" message.
- This slice is happy-path only and ends at order status **Submitted**; editing,
  confirmation, resubmission, and any weekly cut-off are out of scope (later feature).
- Timezone is **Europe/Dublin**. A menu's week is not a fixed weekday: the chef sets
  the week's start date when she publishes a weekly menu. "The current week's menu"
  means the **most recently published menu that is active**.
- No stock limits: the chef cooks to order, so dish availability is unlimited within
  the week — a dish never sells out.
- A client with no meal package is blocked from ordering and told to contact the chef
  (packages are assigned by the chef when the client is created — a required field).
- If a newer menu becomes active while a client is mid-selection, the in-progress
  selection against the old menu is discarded and the client sees the new current menu.
