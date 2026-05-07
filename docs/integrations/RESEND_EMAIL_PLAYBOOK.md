# Resend Email Setup Playbook

## Goal

Resend handles transactional email.

Use it for:

```txt
contact form notifications
lead confirmations
admin invites
password reset or magic link later
publish/deploy notifications
project status updates
```

## Setup

1. Create Resend account.
2. Add sending domain.
3. Verify DNS records.
4. Create API key.
5. Add Cloudflare secret:

```bash
npx wrangler secret put RESEND_API_KEY
```

## Recommended Sender Addresses

```txt
hello@leadershiplegacydigital.com
no-reply@leadershiplegacydigital.com
admin@leadershiplegacydigital.com
```

## Required Routes

```txt
POST /api/forms/contact
POST /api/leads/:id/notify
POST /api/auth/password-reset
POST /api/admin/invite
```

## Email Safety

```txt
validate form input
rate limit submissions
log send attempts
never expose API key
avoid sending secrets over email
require approval before agent sends outbound emails
```

## Progress Checks

- [ ] Domain added to Resend.
- [ ] DNS verified.
- [ ] API key stored in Cloudflare.
- [ ] Contact form email route built.
- [ ] Lead confirmation template created.
- [ ] Send logs saved to D1 or Supabase.
