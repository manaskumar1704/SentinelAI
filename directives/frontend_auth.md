# Frontend Auth Directive

## Purpose

Handle user authentication in the Next.js frontend using Supabase Auth.

## Architecture

```
Frontend (Supabase Auth) → JWT Token → Backend (Supabase JWT Verification)
```

## Process

### Sign Up

1. User visits `/auth/signup`
2. Submits email and password
3. Supabase creates user and sends confirmation email
4. User confirms email → session established
5. Redirect to `/onboarding`

### Sign In

1. User visits `/auth/login`
2. Submits credentials
3. Supabase verifies and returns session with JWT
4. Session stored in cookies via SSR utilities
5. Redirect to `/dashboard` (or `/onboarding` if not completed)

### Session Management

1. Middleware refreshes session on each request
2. Client components use `supabase.auth.getSession()` for token
3. Server components use server-side Supabase client

### Sign Out

1. User clicks sign out in navbar
2. Call `supabase.auth.signOut()`
3. Session cleared, redirect to `/`

## Files/Structure

```
src/
├── lib/supabase/
│   ├── client.ts       # Browser-side client
│   ├── server.ts       # Server-side client
│   └── middleware.ts   # Session refresh utilities
├── middleware.ts       # Next.js middleware (route protection + session refresh)
├── app/
│   ├── auth/
│   │   ├── login/page.tsx    # Sign in form
│   │   ├── signup/page.tsx   # Registration form
│   │   └── callback/route.ts # OAuth/email callback handler
│   └── ...protected pages
└── components/
    └── Navbar.tsx      # Avatar with sign out
```

## API Token Usage

When making authenticated API calls:

```typescript
const supabase = createClient()
const { data: { session } } = await supabase.auth.getSession()

const response = await fetch('/api/endpoint', {
  headers: {
    Authorization: `Bearer ${session?.access_token}`
  }
})
```

## Protected Routes

Middleware protects these paths (redirect to `/` if unauthenticated):

- `/dashboard`
- `/onboarding`
- `/counsellor`
- `/universities`
- `/profile`
- `/guidance`

## Environment Variables

```
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx...
```

## Edge Cases

- Expired session → Middleware refreshes automatically
- Invalid session → Redirect to sign-in
- Onboarding incomplete → Redirect from dashboard to onboarding
- Email not confirmed → Show message, prevent access

## Design Notes

- Auth pages should match Nano Banana design system
- Use glassmorphism cards for forms
- Smooth transitions between auth states
- Loading states during auth operations
