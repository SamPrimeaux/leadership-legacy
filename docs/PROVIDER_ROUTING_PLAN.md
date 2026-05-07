# Provider Routing Plan

Leadership Legacy should use a model/provider router instead of hardcoding one model.

## Providers

```txt
OpenAI
Anthropic
Gemini
Workers AI
Local Llama/Ollama
```

## OpenAI

```txt
gpt-5.4-nano       cheap router
gpt-5.4-mini       default workhorse
gpt-5.4            senior reasoning
gpt-image-1-mini   budget image generation
gpt-image-1.5      standard image generation
```

Blocked:

```txt
gpt-5.5
gpt-5.5-pro
gpt-5.4-pro
```

## Anthropic

```txt
Claude Sonnet     senior review / architecture
Claude Haiku      cheap summaries / validation
```

## Gemini

```txt
Gemini Pro        alternate long-context reasoning
Gemini Flash      cheaper/faster fallback
```

## Workers AI

```txt
embeddings
classification
fallback
utility inference
```

## Local Llama/Ollama

```txt
offline/local draft work
cheap local summaries
local coding experiments
```

## Routing Strategy

Recommended:

```txt
deterministic guardrails
then Thompson Sampling inside safe model pool
then log all outcomes
```

D1 config tables:

```txt
cms_ai_providers
cms_ai_models
cms_ai_routing_policy
cms_ai_routing_arms
```

Supabase telemetry tables:

```txt
ll_model_cost_snapshots
ll_routing_arms
ll_routing_decisions
ll_prompt_runs
ll_stream_events
ll_tool_call_events
ll_error_events
ll_eval_runs
```
