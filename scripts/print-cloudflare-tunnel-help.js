console.log(`
Leadership Legacy Cloudflare Tunnel Help

PowerShell setup:

  winget install --id Cloudflare.cloudflared
  cloudflared tunnel login
  cloudflared tunnel --url http://localhost:5173

Named tunnel flow:

  cloudflared tunnel create leadership-legacy-dev
  cloudflared tunnel route dns leadership-legacy-dev dev.leadershiplegacydigital.com
  cloudflared tunnel run leadership-legacy-dev

Vite local app:

  npm install
  npm run dev

Local URLs:

  http://localhost:5173/
  http://localhost:5173/dashboard.html
`);
