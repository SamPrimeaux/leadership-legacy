-- Leadership Legacy Digital — email template seeds (Resend-ready HTML)
-- Run: npx wrangler d1 execute leadership-legacy --remote --file=docs/email-system/002_seed_templates.sql
-- Variables use {{name}} syntax — replaced server-side before send.

-- ── Contact form → admin notification ───────────────────────────────────────
INSERT OR REPLACE INTO email_templates (
  id, tenant_id, provider, template_key, subject,
  body_text, body_html, status, created_at, updated_at
) VALUES (
  'tpl_contact_notify',
  'tenant_leadership_legacy',
  'resend',
  'contact_form_notify',
  'New contact request — Leadership Legacy Digital',
  'New contact from {{name}} ({{email}}). Subject: {{subject}}. Message: {{message}}',
  '<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>New Contact Request</title>
<style>
  body { margin:0; padding:0; background:#070b14; font-family: "DM Sans", Arial, sans-serif; color:#e8edf5; }
  .wrap { max-width:560px; margin:0 auto; padding:32px 24px; }
  .card { background:#0f1629; border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:28px; }
  .label { font-size:11px; color:#6b7a99; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:4px; }
  .value { font-size:15px; color:#e8edf5; margin-bottom:18px; }
  .msg { background:rgba(255,255,255,0.03); border-left:3px solid #3b82f6; padding:12px 16px; border-radius:4px; font-size:14px; color:#9aa8c7; line-height:1.6; }
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <p style="font-size:18px;font-weight:700;margin:0 0 24px">New contact request</p>
    <div class="label">Name</div><div class="value">{{name}}</div>
    <div class="label">Email</div><div class="value"><a href="mailto:{{email}}" style="color:#60a5fa">{{email}}</a></div>
    <div class="label">Subject</div><div class="value">{{subject}}</div>
    <div class="label">Message</div>
    <div class="msg">{{message}}</div>
  </div>
</div>
</body>
</html>',
  'active',
  datetime('now'), datetime('now')
);

-- ── Contact form → user confirmation ──────────────────────────────────────────
INSERT OR REPLACE INTO email_templates (
  id, tenant_id, provider, template_key, subject,
  body_text, body_html, status, created_at, updated_at
) VALUES (
  'tpl_lead_confirmation',
  'tenant_leadership_legacy',
  'resend',
  'lead_confirmation',
  'We received your message — Leadership Legacy Digital',
  'Hi {{first_name}}, thanks for reaching out. We received your message and will reply within 1-2 business days. — Connor McNeely, Leadership Legacy Digital',
  '<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Message Received</title>
<style>
  body { margin:0; padding:0; background:#070b14; font-family: "DM Sans", Arial, sans-serif; color:#e8edf5; }
  .wrap { max-width:560px; margin:0 auto; padding:40px 24px; }
  .card { background:#0f1629; border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:36px 32px; }
  .eyebrow { font-size:11px; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#3b82f6; margin-bottom:12px; }
  h1 { font-size:24px; font-weight:800; color:#e8edf5; margin:0 0 16px; line-height:1.2; }
  p { font-size:15px; line-height:1.7; color:#9aa8c7; margin:0 0 20px; }
  .highlight { color:#e8edf5; font-weight:600; }
  .footer { font-size:12px; color:#6b7a99; text-align:center; margin-top:28px; }
  .footer a { color:#60a5fa; text-decoration:none; }
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <div class="eyebrow">Contact</div>
    <h1>Thanks, {{first_name}} — we got your message.</h1>
    <p>Leadership Legacy Digital builds <span class="highlight">engineering-grade AI systems</span> for technical businesses. Connor will review your note personally.</p>
    <p>Expect a reply within <span class="highlight">1–2 business days</span>.</p>
  </div>
  <div class="footer">
    Leadership Legacy Digital &nbsp;·&nbsp; Connor McNeely<br/>
    <a href="mailto:connordmcneely@leadershiplegacydigital.com">connordmcneely@leadershiplegacydigital.com</a>
  </div>
</div>
</body>
</html>',
  'active',
  datetime('now'), datetime('now')
);

-- ── New lead welcome ──────────────────────────────────────────────────────────
INSERT OR REPLACE INTO email_templates (
  id, tenant_id, provider, template_key, subject,
  body_text, body_html, status, created_at, updated_at
) VALUES (
  'tpl_lead_welcome',
  'tenant_leadership_legacy',
  'resend',
  'lead_welcome',
  'Welcome — Leadership Legacy Digital',
  'Hi {{first_name}}, thanks for connecting with Leadership Legacy Digital. We help technical businesses ship AI systems, automation, and full-stack applications. Reply anytime if you have questions.',
  '<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Welcome</title>
<style>
  body { margin:0; padding:0; background:#070b14; font-family: "DM Sans", Arial, sans-serif; color:#e8edf5; }
  .wrap { max-width:560px; margin:0 auto; padding:40px 24px; }
  .card { background:#0f1629; border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:36px 32px; }
  .eyebrow { font-size:11px; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#22d3ee; margin-bottom:12px; }
  h1 { font-size:24px; font-weight:800; margin:0 0 16px; }
  p { font-size:15px; line-height:1.7; color:#9aa8c7; margin:0 0 20px; }
  .btn { display:inline-block; background:#3b82f6; color:#fff; font-size:14px; font-weight:700; padding:14px 28px; border-radius:100px; text-decoration:none; margin:8px 0 24px; }
  .footer { font-size:12px; color:#6b7a99; text-align:center; margin-top:28px; }
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <div class="eyebrow">Leadership Legacy Digital</div>
    <h1>Welcome, {{first_name}}.</h1>
    <p>Thanks for connecting. We build AI systems, automation workflows, and production software for technical businesses.</p>
    <a class="btn" href="https://leadership-legacy.meauxbility.workers.dev/services">Explore services</a>
  </div>
  <div class="footer">Connor McNeely · Mechanical Engineer × AI Developer</div>
</div>
</body>
</html>',
  'active',
  datetime('now'), datetime('now')
);

-- ── Admin invite (future auth) ────────────────────────────────────────────────
INSERT OR REPLACE INTO email_templates (
  id, tenant_id, provider, template_key, subject,
  body_text, body_html, status, created_at, updated_at
) VALUES (
  'tpl_admin_invite',
  'tenant_leadership_legacy',
  'resend',
  'admin_invite',
  'You''re invited to the Leadership Legacy dashboard',
  'Hi {{first_name}}, you have been invited to the Leadership Legacy Digital dashboard. Accept here: {{invite_url}}',
  '<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8" /><title>Dashboard Invite</title></head>
<body style="margin:0;background:#070b14;font-family:Arial,sans-serif;color:#e8edf5;">
<div style="max-width:560px;margin:0 auto;padding:40px 24px;">
  <div style="background:#0f1629;border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:32px;">
    <h1 style="font-size:22px;margin:0 0 12px;">Dashboard invite</h1>
    <p style="color:#9aa8c7;line-height:1.6;">Hi {{first_name}}, click below to access the Leadership Legacy dashboard.</p>
    <a href="{{invite_url}}" style="display:inline-block;background:#3b82f6;color:#fff;padding:12px 24px;border-radius:999px;text-decoration:none;font-weight:700;">Accept invite</a>
  </div>
</div>
</body>
</html>',
  'active',
  datetime('now'), datetime('now')
);
