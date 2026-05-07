# Dashboard Auth

The dashboard now has a sign in / sign up concept screen with:

```txt
email field
password field
confirm password field for sign up
name field for sign up
no visible draft password
no exposed API keys
```

## Current State

This is still a concept/demo auth gate. It uses browser session storage after a successful local draft credential check.

The draft password is not shown in the UI.

## Production Upgrade Path

Replace the current component with one of:

```txt
Cloudflare Access
Supabase Auth
Worker-backed session cookies
Google OAuth
GitHub OAuth
Magic link via Resend
```

## Recommended Production Auth Flow

```txt
POST /api/auth/signin
POST /api/auth/signup
POST /api/auth/signout
GET  /api/auth/session
```

Server should:

```txt
hash passwords
use secure HttpOnly cookies
rotate sessions
enforce roles
log admin activity
rate-limit login attempts
never expose secrets to the browser
```

## Important

Do not ship the concept password gate as final production security.
