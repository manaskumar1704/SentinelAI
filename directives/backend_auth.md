# Backend Auth Directive

## Purpose

Handle authentication via Supabase JWT verification.

## Inputs

- `Authorization: Bearer <token>` header from frontend
- Token issued by Supabase Auth

## Process

1. Extract JWT from Bearer header
2. Decode JWT using `supabase_jwt_secret` (HS256 algorithm)
3. Validate audience claim is "authenticated"
4. Extract `sub` claim as `user_id`
5. Extract `email` and `user_metadata` for user context
6. Return `ClerkUser` object (class name kept for compatibility)

## Tools/Scripts

- `middleware/auth.py` - `get_current_user` dependency
- `config.py` - `supabase_jwt_secret` configuration

## Outputs

- Authenticated user object with `user_id`, `email`, `full_name`
- 401 Unauthorized if token missing/invalid/expired

## Edge Cases

- Expired tokens → 401 with "Token has expired"
- Missing header → 401 with "Missing authentication token"
- Invalid JWT format → 401 with error details
- Wrong audience → 401 with "Invalid token audience"
- Missing JWT secret in config → 500 Internal Server Error

## Environment Variables

```
SUPABASE_JWT_SECRET=your-jwt-secret
```

## Notes

- Frontend handles signup/login UI via Supabase Auth
- Backend only verifies tokens, never creates sessions
- The `ClerkUser` class name is legacy; internally it represents any authenticated user
- Supabase JWT uses HS256 symmetric signature (not RS256 like Clerk)
