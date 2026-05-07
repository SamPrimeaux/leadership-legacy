# Leadership Legacy R2 Bucket

Bucket:

```txt
leadership-legacy
```

Worker binding:

```txt
WEBSITE
```

Static assets binding:

```txt
ASSETS
```

## Important Difference

`ASSETS` serves the built Vite `dist/` files as Worker Static Assets.

`WEBSITE` is the R2 bucket used for CMS-managed assets, code snapshots, generated media, page snapshots, docs, exports, and dashboard-managed files.

## URLs

Public development URL:

```txt
https://pub-d426ded97b90451886c5cc7870ae9f17.r2.dev
```

S3 API endpoint:

```txt
https://ede6590ac0d2fb7daf155b35653457b2.r2.cloudflarestorage.com/leadership-legacy
```

Catalog URI:

```txt
https://catalog.cloudflarestorage.com/ede6590ac0d2fb7daf155b35653457b2/leadership-legacy
```

Warehouse name:

```txt
ede6590ac0d2fb7daf155b35653457b2_leadership-legacy
```

## Recommended R2 Prefixes

```txt
assets/
assets/images/generated/
assets/brand/
assets/models/
downloads/
cms/pages/
cms/sections/
cms/themes/
cms/navigation/
snapshots/
snapshots/code/
snapshots/pages/
analytics/
exports/dashboard/
docs/
tmp/
```

## Production Note

The `r2.dev` URL is useful for development but should not be the final production asset URL. For production, connect a custom domain such as:

```txt
assets.leadershiplegacydigital.com
```

or another domain controlled by the project.
