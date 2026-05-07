# R2 Autodeploy and Prune

This repo is configured so pushes to `main` can build, upload fresh app assets to R2, prune old deployments, and deploy the Worker.

## R2 Layout

```txt
leadership-legacy/
  live/
    index.html
    dashboard.html
    assets/...
    manifest.json

  deployments/
    <git-sha>/
      index.html
      dashboard.html
      assets/...
      manifest.json

    _latest.json
```

## What Gets Uploaded

The script uploads every file from:

```txt
dist/
```

to both:

```txt
r2://leadership-legacy/deployments/<git-sha>/
r2://leadership-legacy/live/
```

## Pruning

By default, pruning keeps the latest 3 deployment snapshots:

```txt
R2_KEEP_DEPLOYMENTS=3
```

It deletes older objects under:

```txt
deployments/<old-sha>/
```

It does not delete:

```txt
live/
deployments/_latest.json
cms/
assets/
docs/
analytics/
```

## Local Commands

Build and upload:

```bash
npm run build
npm run r2:publish
```

Prune old deployment snapshots:

```bash
npm run r2:prune
```

Full deploy:

```bash
npm run deploy:full
```

## GitHub Secrets Required

Add these to GitHub repo secrets:

```txt
CLOUDFLARE_API_TOKEN
CLOUDFLARE_ACCOUNT_ID
```

The token needs permission for:

```txt
Workers Scripts: Edit
Account R2 Storage: Edit
Account Settings: Read
```

Depending on the Cloudflare token UI, you may also need:

```txt
Workers Routes: Edit
D1: Edit
```

## Important

`dist/` remains gitignored. Built assets live in R2 and Worker Assets, not Git.

`node_modules/` remains gitignored.

Source of truth remains:

```txt
src/
public/
docs/
scripts/
sql/
package.json
wrangler config
```
