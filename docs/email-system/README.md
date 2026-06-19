# Email system SQL templates

Run these against your Leadership Legacy D1 database after adding the `DB` binding in `wrangler.jsonc`.

```bash
npx wrangler d1 execute leadership-legacy --remote --file=docs/email-system/001_schema.sql
npx wrangler d1 execute leadership-legacy --remote --file=docs/email-system/002_seed_templates.sql
```

Full install guide: [`../EMAIL_SYSTEM_TEMPLATE.md`](../EMAIL_SYSTEM_TEMPLATE.md)

Reference implementation: Companions of CPAS (`companionscpas` repo) — `/dashboard/email` on `companionsofcaddo.org`.
