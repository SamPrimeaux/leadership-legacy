# Leadership Legacy Integration Rubric

This rubric scores whether Connor and the platform are ready for production-grade tool usage.

## Scoring

```txt
0 = Not present
1 = Started but not usable
2 = Partially usable with manual work
3 = Usable for internal testing
4 = Production-ready with guardrails
5 = Production-ready, monitored, documented, and tested
```

## Category A: Integration Setup

| Score | Definition |
|---:|---|
| 0 | No account/API/resource exists |
| 1 | Account exists but not connected |
| 2 | Secret/resource added but not verified |
| 3 | Integration works manually |
| 4 | Integration works through dashboard/API with safe errors |
| 5 | Integration is tested, logged, monitored, and documented |

Applies to:

```txt
GitHub
Google Drive
Gmail
OpenAI
Anthropic
Gemini
Resend
Supabase
D1
R2
KV
Durable Objects
Workers AI
AWS
```

## Category B: Secret Safety

| Score | Definition |
|---:|---|
| 0 | Secrets are exposed or committed |
| 1 | Secrets are manually copied around |
| 2 | Secrets are stored server-side but undocumented |
| 3 | Secrets are stored correctly in Worker/provider dashboards |
| 4 | Secret usage is audited and never returned to browser |
| 5 | Rotation, least privilege, and incident plan exist |

Required standard before production:

```txt
4 minimum
```

## Category C: Dashboard Usability

| Score | Definition |
|---:|---|
| 0 | Dashboard does not load |
| 1 | Dashboard loads but is confusing or broken |
| 2 | Dashboard has basic navigation |
| 3 | Dashboard supports real internal workflows |
| 4 | Dashboard is clear, fast, and role-aware |
| 5 | Dashboard is polished, tested, documented, and production-ready |

Required standard before client-facing demo:

```txt
3 minimum
```

Required standard before real production:

```txt
4 minimum
```

## Category D: AI Tooling

| Score | Definition |
|---:|---|
| 0 | No AI provider works |
| 1 | One provider works manually |
| 2 | One provider works through API |
| 3 | Multiple providers are configured |
| 4 | Provider routing, cost logs, and fallbacks work |
| 5 | Evals, cost controls, human ratings, and automatic routing optimization work |

Required standard before serious use:

```txt
3 minimum
```

Required standard before automated workflows:

```txt
4 minimum
```

## Category E: Tool Execution Safety

| Score | Definition |
|---:|---|
| 0 | Tools execute without controls |
| 1 | Tools are hardcoded and unlogged |
| 2 | Tools are logged but not permissioned |
| 3 | Tools have input validation and basic logging |
| 4 | Tools have risk levels, approval gates, and audit logs |
| 5 | Tools are fully governed, tested, monitored, and reversible |

Any destructive tool requires:

```txt
4 minimum
```

Destructive examples:

```txt
delete file
send email
deploy production
write to main branch
rotate secret
change DNS
execute terminal command
delete R2 object
delete database row
```

## Category F: Testing

| Score | Definition |
|---:|---|
| 0 | No tests |
| 1 | Manual testing only |
| 2 | Build passes |
| 3 | Playwright smoke tests pass |
| 4 | Core dashboard/API workflows are tested |
| 5 | CI, traces, screenshots, evals, and deployment gates are active |

Required standard before production:

```txt
4 minimum
```

## Category G: Connor Readiness

| Score | Definition |
|---:|---|
| 0 | Connor has no access or understanding |
| 1 | Connor can view the app |
| 2 | Connor can run basic commands with help |
| 3 | Connor can run, test, and deploy with a guide |
| 4 | Connor can diagnose common issues |
| 5 | Connor can independently operate and improve the platform |

Required standard before handoff:

```txt
3 minimum
```

Strong handoff target:

```txt
4 minimum
```

## Final Readiness Matrix

| Area | Target Score | Actual Score | Pass |
|---|---:|---:|---|
| Integration setup | 4 |  | [ ] |
| Secret safety | 4 |  | [ ] |
| Dashboard usability | 4 |  | [ ] |
| AI tooling | 4 |  | [ ] |
| Tool execution safety | 4 |  | [ ] |
| Testing | 4 |  | [ ] |
| Connor readiness | 3 |  | [ ] |

## Production Decision

Production-ready only if:

```txt
no category below target
no exposed secrets
no destructive tools without approval
build passes
Playwright passes
health endpoints pass
dashboard auth is production-grade
```
