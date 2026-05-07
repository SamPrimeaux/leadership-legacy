export const powershellCommands = [
  {
    id: "clone",
    label: "Clone repo",
    command: "git clone git@github.com:SamPrimeaux/leadership-legacy.git",
    notes: "Use this once on Connor's machine after SSH is connected."
  },
  {
    id: "enter-repo",
    label: "Enter repo",
    command: "cd leadership-legacy",
    notes: "PowerShell uses cd the same way zsh does."
  },
  {
    id: "install",
    label: "Install packages",
    command: "npm install",
    notes: "Installs React, Vite, Monaco, xterm, and dashboard dependencies."
  },
  {
    id: "dev",
    label: "Run local dev server",
    command: "npm run dev",
    notes: "Starts the local Vite server."
  },
  {
    id: "build",
    label: "Build app",
    command: "npm run build",
    notes: "Validates production build before deploy."
  },
  {
    id: "deploy",
    label: "Deploy to Cloudflare",
    command: "npm run deploy",
    notes: "Builds and deploys through Wrangler."
  },
  {
    id: "health",
    label: "Check deployed Worker health",
    command: "curl https://leadership-legacy.meauxbility.workers.dev/api/health",
    notes: "Verifies the Worker is responding."
  },
  {
    id: "r2-status",
    label: "Check R2 status",
    command: "curl https://leadership-legacy.meauxbility.workers.dev/api/r2/status",
    notes: "Verifies R2 binding and metadata."
  }
];

export const tunnelCommands = [
  {
    id: "install-cloudflared-winget",
    label: "Install cloudflared with winget",
    command: "winget install --id Cloudflare.cloudflared",
    notes: "Recommended for PowerShell on Windows."
  },
  {
    id: "login",
    label: "Login to Cloudflare Tunnel",
    command: "cloudflared tunnel login",
    notes: "Opens browser auth. Connor should log into his Cloudflare account."
  },
  {
    id: "create",
    label: "Create named tunnel",
    command: "cloudflared tunnel create leadership-legacy-dev",
    notes: "Creates a reusable tunnel for local dev previews."
  },
  {
    id: "route",
    label: "Route DNS to tunnel",
    command: "cloudflared tunnel route dns leadership-legacy-dev dev.leadershiplegacydigital.com",
    notes: "Only run after the real domain/DNS is ready."
  },
  {
    id: "run-local",
    label: "Expose local Vite server",
    command: "cloudflared tunnel --url http://localhost:5173",
    notes: "Quick temporary tunnel for sharing local preview."
  }
];

export const setupChecklist = [
  {
    group: "Local machine",
    items: [
      "Install Git",
      "Install Node.js LTS",
      "Install VS Code or Cursor",
      "Install Wrangler",
      "Install cloudflared",
      "Confirm PowerShell can run npm and git"
    ]
  },
  {
    group: "Repo",
    items: [
      "Clone leadership-legacy repo",
      "Run npm install",
      "Run npm run dev",
      "Open localhost public app",
      "Open localhost dashboard.html"
    ]
  },
  {
    group: "Cloudflare",
    items: [
      "Login with npx wrangler login",
      "Confirm Worker access",
      "Confirm R2 bucket",
      "Confirm D1 database",
      "Add secrets",
      "Run npm run deploy"
    ]
  },
  {
    group: "AI providers",
    items: [
      "Replace Sam's temporary OpenAI key with Connor's key",
      "Add Anthropic key",
      "Add Gemini key if available",
      "Confirm blocked model policy",
      "Confirm routing table"
    ]
  }
];

export const starterFiles = {
  "src/worker/index.js": `export default {
  async fetch(request, env) {
    return new Response("Leadership Legacy Worker online");
  }
};`,
  "src/dashboard/lib/providerRouter.js": `export function selectModel(task) {
  if (task.risk === "high") return "gpt-5.4";
  if (task.mode === "cheap") return "gpt-5.4-nano";
  return "gpt-5.4-mini";
}`,
  "wrangler.jsonc": `{
  "name": "leadership-legacy",
  "main": "src/worker/index.js",
  "compatibility_date": "2026-05-06"
}`,
  "cloudflared/config.yml": `tunnel: leadership-legacy-dev
credentials-file: C:\\\\Users\\\\Connor\\\\.cloudflared\\\\leadership-legacy-dev.json

ingress:
  - hostname: dev.leadershiplegacydigital.com
    service: http://localhost:5173
  - service: http_status:404`
};
