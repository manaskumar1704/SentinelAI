# Backend Auth Directive

## Purpose

Handle authentication via Clerk JWT verification.

## Inputs

- `Authorization: Bearer <token>` header from frontend

## Process

1. Extract JWT from Bearer header
2. Decode JWT (development: unverified, production: verify with JWKS)
3. Extract `sub` claim as `user_id`
4. Return `ClerkUser` object with user data

## Tools/Scripts

- `middleware/auth.py` - `get_current_user` dependency

## Outputs

- Authenticated `ClerkUser` object
- 401 Unauthorized if token missing/invalid

## Edge Cases

- Expired tokens → 401
- Missing header → 401
- Invalid JWT format → 401

## Notes

- Frontend handles signup/login UI via Clerk
- Backend only verifies tokens, never creates sessions
