# AI Providers Setup Playbook

## Goal

Connor should understand how OpenAI, Anthropic, Gemini, Workers AI, and local Llama/Ollama fit together.

## Provider Roles

| Provider | Best Use |
|---|---|
| OpenAI | Default code generation, agent actions, structured outputs, image generation |
| Anthropic | Review, architecture, long-form critique, second-opinion reasoning |
| Gemini | Long-context comparison, Google ecosystem workflows, multimodal alternate |
| Workers AI | Cloudflare-native embeddings, utility inference, fallback |
| Local Llama/Ollama | Local low-cost experiments and private drafts |

## OpenAI

Current note:

```txt
Sam installed an OpenAI key temporarily.
Connor should replace it with his own.
```

Add/replace secret:

```bash
npx wrangler secret put OPENAI_API_KEY
npm run deploy
```

Recommended model lanes:

```txt
gpt-5.4-nano       cheap fast router
gpt-5.4-mini       default dashboard/code model
gpt-5.4            deeper architecture/reasoning
gpt-image-1-mini   budget image generation
gpt-image-1.5      higher quality image generation
```

Blocked by project policy:

```txt
gpt-5.5
gpt-5.5-pro
gpt-5.4-pro
```

## Anthropic

Add secret:

```bash
npx wrangler secret put ANTHROPIC_API_KEY
npm run deploy
```

Use Anthropic for:

```txt
code review
architecture review
risk analysis
prompt critique
second-opinion evaluation
```

## Gemini

Add secret:

```bash
npx wrangler secret put GEMINI_API_KEY
npm run deploy
```

Use Gemini for:

```txt
long-context document comparison
multimodal experiments
alternate provider testing
cost/quality benchmarking
```

## Workers AI

Add binding in `wrangler.jsonc`:

```json
"ai": {
  "binding": "AI"
}
```

Use Workers AI for:

```txt
embeddings
classification
fallback summaries
cheap internal utilities
```

## Local Llama/Ollama

Local setup:

```bash
ollama list
ollama run llama3.1
```

Suggested local env:

```txt
LOCAL_LLM_BASE_URL=http://localhost:11434
LOCAL_LLM_MODEL=llama3.1
```

## Routing Policy

Use deterministic safety first, then Thompson Sampling for provider/model selection inside safe lanes.

Deterministic gates:

```txt
blocked model check
secret availability
task risk
max cost
required modality
tool support
context length
latency budget
```

Thompson Sampling learns from:

```txt
success/failure
human rating
latency
cost
tool-call reliability
test pass/fail
output quality
```

## Progress Checks

- [ ] OpenAI secret added.
- [ ] Anthropic secret added.
- [ ] Gemini secret added if available.
- [ ] Workers AI binding added.
- [ ] Provider status route shows configured providers.
- [ ] Dashboard can call OpenAI through Worker.
- [ ] Anthropic review endpoint planned.
- [ ] Gemini comparison endpoint planned.
- [ ] Cost logging table is ready.
- [ ] Blocked model policy enforced.
