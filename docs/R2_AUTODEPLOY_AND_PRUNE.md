# R2 Autodeploy and Prune

The previous prune implementation attempted to call:

```bash
npx wrangler r2 object list leadership-legacy --prefix deployments/ --remote --json
```

Wrangler v4.88.0 does not support that `object list` command shape.

The fixed prune flow now uses the deployed Worker API:

```txt
GET /api/r2/list?prefix=deployments/
```

Then it deletes old deployment objects using the supported command:

```bash
npx wrangler r2 object delete leadership-legacy/<key> --remote
```

## R2 Layout

```txt
leadership-legacy/
  live/
    index.html
    dashboard.html
    assets/
    manifest.json

  deployments/
    <git-sha>/
      index.html
      dashboard.html
      assets/
      manifest.json

    _latest.json
```

## Commands

Publish fresh build:

```bash
npm run build
npm run r2:publish
```

Prune old deployment snapshots:

```bash
npm run r2:prune
```

Full local deployment:

```bash
npm run deploy:full
```

## Safety

Pruning deletes only old objects under:

```txt
deployments/<old-sha>/
```

It does not delete:

```txt
live/
cms/
assets/
docs/
analytics/
```
