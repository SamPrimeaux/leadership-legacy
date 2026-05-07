export const aiProviders = [
  {
    key: "openai",
    displayName: "OpenAI",
    secretName: "OPENAI_API_KEY",
    status: "needs secret",
    useCases: ["routing", "chat", "coding", "image generation", "evals"],
    models: [
      {
        key: "gpt-5.4-nano",
        lane: "cheap_fast_router",
        enabled: true,
        notes: "Routing, classification, short summaries, metadata extraction."
      },
      {
        key: "gpt-5.4-mini",
        lane: "default_workhorse",
        enabled: true,
        notes: "Normal coding, CMS tasks, tool calls, dashboard help."
      },
      {
        key: "gpt-5.4",
        lane: "senior_reasoning",
        enabled: true,
        notes: "Architecture, schema design, security-sensitive reviews."
      },
      {
        key: "gpt-image-1-mini",
        lane: "budget_image_generation",
        enabled: true,
        notes: "Draft mockups, thumbnails, quick creative variations."
      },
      {
        key: "gpt-image-1.5",
        lane: "standard_image_generation",
        enabled: true,
        notes: "Client-facing brand visuals and higher quality image work."
      }
    ],
    blockedModels: ["gpt-5.5", "gpt-5.5-pro", "gpt-5.4-pro"]
  },
  {
    key: "anthropic",
    displayName: "Anthropic",
    secretName: "ANTHROPIC_API_KEY",
    status: "needs secret",
    useCases: ["code review", "architecture", "agent review", "long-form reasoning"],
    models: [
      {
        key: "claude-sonnet",
        lane: "standard_senior_review",
        enabled: true,
        notes: "Code review, system planning, route/schema reasoning."
      },
      {
        key: "claude-haiku",
        lane: "cheap_fast_fallback",
        enabled: true,
        notes: "Low-cost summaries, validation, lightweight automation."
      }
    ],
    blockedModels: []
  }
];

export const routingPolicy = {
  defaultTextModel: "gpt-5.4-mini",
  cheapTextModel: "gpt-5.4-nano",
  seniorTextModel: "gpt-5.4",
  defaultImageModel: "gpt-image-1-mini",
  standardImageModel: "gpt-image-1.5",
  reviewProvider: "anthropic",
  blockedModels: ["gpt-5.5", "gpt-5.5-pro", "gpt-5.4-pro"],
  router: "deterministic_guardrails_then_thompson_sampling",
  notes:
    "Secrets stay server-side. Browser dashboard only edits metadata, preferences, and model routing policy."
};
