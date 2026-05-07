# AWS Setup Playbook

## Goal

AWS is optional for this platform, but Connor should understand where it could fit.

Cloudflare remains the primary runtime. AWS can be used for compatibility, backup, specialized services, or future client needs.

## Useful AWS Services

| AWS Service | Possible Use |
|---|---|
| S3 | Backup storage, client compatibility, artifact exports |
| IAM | Scoped service users and policies |
| Bedrock | Alternate model provider experiments |
| Lambda | Specialized server-side tasks if needed |
| CloudWatch | Logs if AWS services are used |
| SES | Email alternative to Resend |
| ECR/ECS | Containerized CAD or heavy processing later |

## First AWS Setup

1. Create AWS account.
2. Enable MFA.
3. Create IAM user or role for programmatic access.
4. Use least privilege.
5. Never commit AWS keys.

## Suggested IAM Permissions

Start narrow:

```txt
s3:ListBucket
s3:GetObject
s3:PutObject
s3:DeleteObject only if truly needed
```

## Cloudflare Secrets

```bash
npx wrangler secret put AWS_ACCESS_KEY_ID
npx wrangler secret put AWS_SECRET_ACCESS_KEY
npx wrangler secret put AWS_REGION
npx wrangler secret put AWS_S3_BUCKET
```

## When to Use AWS Instead of R2

Use R2 first for this app.

Use AWS S3 only when:

```txt
client already uses AWS
a third-party requires S3
data pipeline already lives in AWS
Bedrock workflow requires AWS account alignment
long-term backup strategy requires separate cloud
```

## AWS Safety Rules

```txt
use IAM least privilege
rotate keys
log access
avoid root keys
never put AWS keys in browser
do not duplicate assets without a reason
prefer R2 for Cloudflare-native workflows
```

## Progress Checks

- [ ] AWS account has MFA.
- [ ] IAM user/role created.
- [ ] Permissions are scoped.
- [ ] Keys stored only as secrets.
- [ ] S3 compatibility decision documented.
- [ ] Bedrock experiment decision documented.
