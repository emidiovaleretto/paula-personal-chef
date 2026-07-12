# Feature: Weekly menu order

## Summary

Each week the chef publishes a menu of available dishes. A logged-in client needs to
browse the current week's published menu, choose the dishes they want (up to the limit
allowed by their meal package), and submit a single order to the chef. This gives the
chef a clear, per-client shopping/prep list for the week and gives the client a simple,
self-service way to make their weekly selections. A client may hold only **one** order
per weekly menu, so the act of ordering is deliberate and unambiguous.

## User stories

- As a logged-in client, I want to see the current week's published menu, so that I
  know which dishes I can choose from this week.
- As a client with a meal package, I want to select dishes up to my package's limit,
  so that I get exactly what my plan entitles me to.
- As a client, I want to submit my selections as a single order to the chef, so that
  the chef knows what to prepare for me this week.
- As a client, I want to be prevented from placing a second order for the same weekly
  menu, so that my order stays unambiguous and the chef isn't sent conflicting requests.
- As a client, I want to see the order I already submitted, so that I can confirm what
  I asked for.

## Acceptance criteria

- [ ] Given I am logged in and a menu is published for the current week, when I open
  the weekly menu, then I see the list of dishes available for that week and my
  package's selection limit.
- [ ] Given I am logged in and **no** menu is published for the current week, when I
  open the weekly menu, then I see a clear "no menu available this week" state and
  cannot place an order.
- [ ] Given I am viewing the current week's menu, when I select dishes up to my
  package limit, then my running selection count is shown and I can submit.
- [ ] Given I have selected the maximum number of dishes allowed by my package, when I
  try to add another dish, then I am prevented from exceeding the limit and told why.
- [ ] Given I have a valid selection within my limit, when I submit, then an order is
  created for me against the current weekly menu and I see a confirmation of what I ordered.
- [ ] Given I have already submitted an order for the current weekly menu, when I view
  the menu again, then I see my existing order and I am **not** offered a way to create
  a second order for that menu.
- [ ] Given I submit a selection that references a dish not on the current published
  menu, when the order is processed, then the order is rejected with a clear error.
- [ ] Given I am not logged in, when I try to view the weekly menu or place an order,
  then I am denied access.

## Scope

### In scope

- Viewing the current week's published menu (dishes and the client's package limit).
- Selecting dishes up to the meal-package limit and seeing the running count.
- Submitting exactly one order per client per weekly menu.
- Viewing the order the client already submitted for the current weekly menu.
- Enforcing: login required, dishes must belong to the current published menu, one
  order per weekly menu, selection within the package limit.

### Out of scope (non-goals)

- The chef's authoring/publishing of the weekly menu (assumed to already exist or a
  separate feature).
- Assigning or managing which meal package a client has (assumed to already exist).
- Payment, billing, or invoicing for the order.
- Chef-side order management (accept/decline/fulfil), notifications, or prep lists.
- Delivery/scheduling logistics.
- Ratings, favourites, or reordering from a previous week.

## Edge cases & error states

- No published menu for the current week → informative empty state, ordering blocked.
- Client has no meal package assigned → [NEEDS CLARIFICATION: can they order at all,
  and if so under what limit? Or are they blocked with a message?]
- Client submits an empty selection (zero dishes) → [NEEDS CLARIFICATION: is a zero-dish
  order allowed, or is at least one dish required?]
- Selection exceeds the package limit → submission rejected / add blocked with reason.
- A dish is removed from the menu between viewing and submitting → order rejected for
  the stale dish with a clear message.
- Client attempts a second order for the same weekly menu → blocked, existing order shown.
- The week rolls over (a new menu is published) while the client is mid-selection →
  [NEEDS CLARIFICATION: what happens to an in-progress selection against the old menu?]

## Open questions

- [NEEDS CLARIFICATION: What exactly is the "meal-package limit" counting? A total
  number of dishes for the week, a number of meals/servings, or a per-category quota?]
- [NEEDS CLARIFICATION: Can a client select the same dish more than once (quantities),
  or is each dish a single yes/no choice?]
- [NEEDS CLARIFICATION: After submitting, can the client edit or cancel their order
  before some cut-off, or is the order final once submitted? (Current spec assumes
  final — one immutable order per weekly menu.)]
- [NEEDS CLARIFICATION: Is there an ordering deadline/cut-off within the week after
  which the current menu can no longer be ordered from?]
- [NEEDS CLARIFICATION: How is "the current week" determined — which day does a menu
  week start, and in whose timezone?]
- [NEEDS CLARIFICATION: Do dishes have limited quantities/capacity (can a dish sell
  out across clients), or is availability unlimited within the week?]
