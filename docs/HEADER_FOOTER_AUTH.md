# Header, Footer, Theme, and Dashboard Auth

## Public Header

The public app now has a branded glassmorphic header with:

- Leadership Legacy / Connor McNeely brand lockup
- Desktop dropdown navigation
- Light/dark theme toggle
- Header CTA
- Mobile hamburger
- 50vw-style slide-out drawer navigation on tablet/mobile

## Public Footer

The footer now has:

- Large conversion band
- Brand summary
- Site navigation
- Build lane navigation
- Dashboard/legal links
- Glassmorphic premium style

## Theme

Theme is stored in:

```txt
localStorage["ll-theme"]
```

It toggles:

```txt
html[data-theme="dark"]
html[data-theme="light"]
```

## Dashboard Password Gate

The dashboard concept is protected by a client-side draft password:

```txt
1234
```

This is only for concept/demo protection. Production should replace this with real auth:

- Cloudflare Access
- Supabase Auth
- GitHub OAuth
- Magic link
- Session cookies
- Server-side role checks
