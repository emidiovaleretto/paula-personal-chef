# Tasks: User login

> Format: `- [ ] T00X [P?] <verb + object> — (covers: AC-n / plan §x)`

## Setup
- [ ] T001 Confirm User model exists with email + password_hash — (plan §Data model)

## Tests
- [ ] T002 [P] Test: valid credentials authenticate and redirect — (covers AC-1)
- [ ] T003 [P] Test: invalid credentials show generic error — (covers AC-2)
- [ ] T004 [P] Test: 5 failures trigger a 15-min lockout — (covers AC-3)
- [ ] T005 [P] Test: authenticated user visiting /login is redirected — (covers AC-4)
- [ ] T006 [P] Test: no response or log exposes the password — (covers AC-5)

## Implementation
- [ ] T007 Input validation for the login form — (plan §Validation)
- [ ] T008 Auth service: verify email + password hash — (plan §Architecture)
- [ ] T009 Session/token issuance on success — (plan §Architecture)
- [ ] T010 Rate limiter + lockout policy — (plan §Security)
- [ ] T011 Redirect-if-authenticated guard on /login — (covers AC-4)

## Polish
- [ ] T012 Manual walkthrough of all acceptance criteria + short docs note.
