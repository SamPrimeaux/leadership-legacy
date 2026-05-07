import { Link } from "react-router-dom";
import { Code2, Bot, TerminalSquare, Database, Rocket } from "lucide-react";

export function IDEHome() {
  const cards = [
    {
      title: "IDE Workspace",
      body: "Open Monaco, edit starter files, and use OpenAI to generate or refactor code.",
      href: "/dashboard/dev",
      icon: Code2
    },
    {
      title: "AI Code Agent",
      body: "Use the installed OPENAI_API_KEY through secure Worker endpoints.",
      href: "/dashboard/dev/agent",
      icon: Bot
    },
    {
      title: "Terminal Dock",
      body: "PowerShell-friendly command presets with xterm prepared for future PTY execution.",
      href: "/dashboard/dev/terminal",
      icon: TerminalSquare
    },
    {
      title: "R2 Storage",
      body: "Browse the leadership-legacy bucket and prepare CMS assets.",
      href: "/dashboard/storage",
      icon: Database
    },
    {
      title: "Publishing",
      body: "Prepare deploy, CMS publish, and snapshot workflows.",
      href: "/dashboard/publishing",
      icon: Rocket
    }
  ];

  return (
    <section>
      <p className="dash-eyebrow">Leadership Legacy IDE</p>
      <h1>Cursor-style CMS command center</h1>
      <p className="dash-subtitle">
        A full dashboard cockpit for Connor: Monaco editor, xterm terminal prep, OpenAI-powered file generation,
        CMS management, R2 storage, AI provider settings, analytics, and deployment workflows.
      </p>

      <div className="ide-home-grid">
        {cards.map((card) => {
          const Icon = card.icon;
          return (
            <Link className="ide-home-card" to={card.href} key={card.title}>
              <Icon size={22} />
              <h2>{card.title}</h2>
              <p>{card.body}</p>
            </Link>
          );
        })}
      </div>

      <article className="ide-callout">
        <p className="dash-eyebrow">OpenAI status</p>
        <h2>Worker-backed AI actions are enabled</h2>
        <p>
          The browser never sees the API key. Monaco sends the selected file and instruction to
          <code>/api/openai/code</code>, the Worker calls OpenAI’s Responses API, and the generated code can be copied
          or applied back into the editor.
        </p>
      </article>
    </section>
  );
}
