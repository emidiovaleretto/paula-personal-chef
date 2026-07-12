# Feature: User login

## Summary
Registered users need to authenticate with an email and password so they can access
their account. Unauthenticated users must be kept out of protected areas.

## User stories
- As a registered user, I want to log in with my email and password, so that I can
  access my account.
- As a user who typed the wrong password, I want a clear error, so that I know what
  went wrong without leaking whether the email exists.
- As a forgetful user, I want a "forgot password" link, so that I can recover access.

## Acceptance criteria
- [ ] Given valid credentials, when I submit the login form, then I am authenticated
  and redirected to the dashboard.
- [ ] Given an invalid email/password combination, when I submit, then I see a generic
  "invalid credentials" message and remain on the login page.
- [ ] Given 5 consecutive failed attempts for the same account, when I try again, then
  I am temporarily locked out for 15 minutes.
- [ ] Given I am already authenticated, when I visit the login page, then I am
  redirected to the dashboard.
- [ ] Passwords are never shown, logged, or returned by any response.

## Scope
### In scope
- Email + password login, logout, generic error handling, basic rate limiting.
### Out of scope (non-goals)
- Social / SSO login.
- Two-factor authentication.
- Account registration flow (assumed to already exist).

## Edge cases & error states
- Empty email or password → inline validation, no server call.
- Whitespace-only input → treated as empty.
- Locked-out account → show remaining lockout time.

## Open questions
- ~~[NEEDS CLARIFICATION: session cookie vs. token]~~ → Resolved in plan: session auth.
- ~~[NEEDS CLARIFICATION: is "remember me" required for v1?]~~ → Resolved in plan: out of v1.
