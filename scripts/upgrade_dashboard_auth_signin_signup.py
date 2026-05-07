#!/usr/bin/env python3
from pathlib import Path
import subprocess
import textwrap

ROOT = Path.cwd()

def run(cmd, check=False):
    print("$ " + " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result

def write(path, content):
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    print(f"wrote {path}")

def main():
    write("src/dashboard/components/DashboardAuthGate.jsx", r'''
    import { useState } from "react";
    import { LockKeyhole, Mail, KeyRound, UserPlus, LogIn } from "lucide-react";

    const STORAGE_KEY = "ll-dashboard-authenticated";

    // Concept-only local draft credential.
    // Do not display this value in the UI.
    // Production should replace this with Supabase Auth, Cloudflare Access,
    // or a Worker-backed session cookie.
    const DRAFT_PASSWORD = "1234";

    function hasSession() {
      if (typeof window === "undefined") return false;
      return window.sessionStorage.getItem(STORAGE_KEY) === "true";
    }

    export function DashboardAuthGate({ children }) {
      const [authenticated, setAuthenticated] = useState(hasSession);
      const [mode, setMode] = useState("signin");
      const [email, setEmail] = useState("");
      const [password, setPassword] = useState("");
      const [confirmPassword, setConfirmPassword] = useState("");
      const [displayName, setDisplayName] = useState("");
      const [error, setError] = useState("");

      function handleSubmit(event) {
        event.preventDefault();
        setError("");

        const normalizedEmail = email.trim().toLowerCase();

        if (!normalizedEmail || !normalizedEmail.includes("@")) {
          setError("Enter a valid email address.");
          return;
        }

        if (!password) {
          setError("Enter your password.");
          return;
        }

        if (mode === "signup") {
          if (!displayName.trim()) {
            setError("Enter your name.");
            return;
          }

          if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
          }
        }

        // Concept/draft behavior:
        // This simulates auth without exposing the draft password.
        // Real production auth should happen server-side.
        if (password === DRAFT_PASSWORD) {
          window.sessionStorage.setItem(STORAGE_KEY, "true");
          window.sessionStorage.setItem("ll-dashboard-email", normalizedEmail);
          window.sessionStorage.setItem("ll-dashboard-name", displayName.trim() || normalizedEmail);
          setAuthenticated(true);
          return;
        }

        setError("Invalid credentials for this draft dashboard.");
      }

      if (authenticated) {
        return children;
      }

      return (
        <main className="dashboard-auth-page">
          <section className="dashboard-auth-layout">
            <div className="dashboard-auth-intro">
              <div className="auth-icon">
                <LockKeyhole size={24} />
              </div>

              <p className="dash-eyebrow">Protected Workspace</p>
              <h1>Leadership Legacy Dashboard</h1>
              <p>
                Sign in to access the CMS, Cursor-style IDE, OpenAI code actions,
                R2 storage, analytics, publishing, and provider configuration.
              </p>

              <div className="auth-feature-grid">
                <span>CMS editing</span>
                <span>Monaco workspace</span>
                <span>OpenAI code actions</span>
                <span>R2 asset storage</span>
                <span>Provider routing</span>
                <span>Publishing workflow</span>
              </div>
            </div>

            <form className="dashboard-auth-card" onSubmit={handleSubmit}>
              <div className="auth-tabs" role="tablist" aria-label="Authentication mode">
                <button
                  type="button"
                  className={mode === "signin" ? "active" : ""}
                  onClick={() => {
                    setMode("signin");
                    setError("");
                  }}
                >
                  <LogIn size={16} />
                  Sign in
                </button>
                <button
                  type="button"
                  className={mode === "signup" ? "active" : ""}
                  onClick={() => {
                    setMode("signup");
                    setError("");
                  }}
                >
                  <UserPlus size={16} />
                  Sign up
                </button>
              </div>

              <div>
                <p className="dash-eyebrow">{mode === "signin" ? "Welcome back" : "Create access"}</p>
                <h2>{mode === "signin" ? "Sign in to dashboard" : "Create dashboard account"}</h2>
                <p>
                  {mode === "signin"
                    ? "Use your approved dashboard credentials."
                    : "Create a draft dashboard profile. Production auth will be connected later."}
                </p>
              </div>

              {mode === "signup" ? (
                <label>
                  Name
                  <div className="auth-input-wrap">
                    <UserPlus size={16} />
                    <input
                      type="text"
                      value={displayName}
                      onChange={(event) => setDisplayName(event.target.value)}
                      placeholder="Connor McNeely"
                      autoComplete="name"
                    />
                  </div>
                </label>
              ) : null}

              <label>
                Email
                <div className="auth-input-wrap">
                  <Mail size={16} />
                  <input
                    type="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    placeholder="you@example.com"
                    autoComplete="email"
                    required
                  />
                </div>
              </label>

              <label>
                Password
                <div className="auth-input-wrap">
                  <KeyRound size={16} />
                  <input
                    type="password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    placeholder="Enter password"
                    autoComplete={mode === "signin" ? "current-password" : "new-password"}
                    required
                  />
                </div>
              </label>

              {mode === "signup" ? (
                <label>
                  Confirm password
                  <div className="auth-input-wrap">
                    <KeyRound size={16} />
                    <input
                      type="password"
                      value={confirmPassword}
                      onChange={(event) => setConfirmPassword(event.target.value)}
                      placeholder="Confirm password"
                      autoComplete="new-password"
                      required
                    />
                  </div>
                </label>
              ) : null}

              {error ? <span className="auth-error">{error}</span> : null}

              <button className="primary-action auth-submit" type="submit">
                {mode === "signin" ? "Sign in" : "Create account"}
              </button>

              <small>
                This is a protected draft workspace. Production authentication should be
                upgraded to Supabase Auth, Cloudflare Access, or Worker-backed sessions.
              </small>
            </form>
          </section>
        </main>
      );
    }
    ''')

    css_path = ROOT / "src/dashboard/dashboard.css"
    existing = css_path.read_text() if css_path.exists() else ""

    # Remove old auth CSS block only by appending stronger replacement classes.
    auth_css = r'''
    .dashboard-auth-page {
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 28px;
      background:
        radial-gradient(circle at 18% 8%, rgba(56, 189, 248, 0.18), transparent 30rem),
        radial-gradient(circle at 84% 0%, rgba(34, 197, 94, 0.12), transparent 28rem),
        linear-gradient(135deg, #050812, #080b12 55%, #0b1020);
    }

    .dashboard-auth-layout {
      width: min(1080px, 100%);
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 22px;
      align-items: stretch;
    }

    .dashboard-auth-intro,
    .dashboard-auth-card {
      border: 1px solid rgba(148, 163, 184, 0.18);
      border-radius: 30px;
      background: rgba(15, 23, 42, 0.78);
      box-shadow: 0 30px 90px rgba(0, 0, 0, 0.42);
      backdrop-filter: blur(22px);
    }

    .dashboard-auth-intro {
      padding: clamp(28px, 5vw, 54px);
      display: grid;
      align-content: center;
      gap: 18px;
      position: relative;
      overflow: hidden;
    }

    .dashboard-auth-intro::before {
      content: "";
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(56, 189, 248, 0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56, 189, 248, 0.07) 1px, transparent 1px);
      background-size: 48px 48px;
      mask-image: radial-gradient(circle at 30% 20%, black, transparent 72%);
      pointer-events: none;
    }

    .dashboard-auth-intro > * {
      position: relative;
      z-index: 1;
    }

    .dashboard-auth-intro h1 {
      margin: 0;
      font-size: clamp(2.8rem, 7vw, 6rem);
      line-height: 0.9;
      letter-spacing: -0.075em;
    }

    .dashboard-auth-intro p {
      color: #a8b3c7;
      line-height: 1.7;
      max-width: 650px;
    }

    .auth-feature-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      margin-top: 10px;
    }

    .auth-feature-grid span {
      border: 1px solid rgba(56, 189, 248, 0.2);
      border-radius: 14px;
      background: rgba(56, 189, 248, 0.07);
      color: #bae6fd;
      padding: 10px 12px;
      font-size: 0.86rem;
      font-weight: 850;
    }

    .dashboard-auth-card {
      padding: clamp(22px, 4vw, 34px);
      display: grid;
      gap: 16px;
    }

    .dashboard-auth-card h2 {
      margin: 0 0 8px;
      font-size: clamp(1.8rem, 4vw, 2.8rem);
      line-height: 0.96;
      letter-spacing: -0.055em;
    }

    .dashboard-auth-card p,
    .dashboard-auth-card small {
      color: #94a3b8;
      line-height: 1.6;
    }

    .auth-tabs {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      border: 1px solid rgba(148, 163, 184, 0.14);
      background: rgba(5, 8, 18, 0.52);
      border-radius: 999px;
      padding: 6px;
    }

    .auth-tabs button {
      min-height: 40px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      border: 0;
      border-radius: 999px;
      background: transparent;
      color: #94a3b8;
      font-weight: 900;
    }

    .auth-tabs button.active {
      color: #04111f;
      background: linear-gradient(135deg, #38bdf8, #22c55e);
    }

    .dashboard-auth-card label {
      display: grid;
      gap: 8px;
      color: #cbd5e1;
      font-weight: 850;
    }

    .auth-input-wrap {
      min-height: 48px;
      display: flex;
      align-items: center;
      gap: 10px;
      border: 1px solid rgba(148, 163, 184, 0.18);
      border-radius: 16px;
      background: rgba(5, 8, 18, 0.72);
      color: #7dd3fc;
      padding: 0 13px;
    }

    .auth-input-wrap input {
      width: 100%;
      min-height: 46px;
      border: 0;
      outline: 0;
      background: transparent;
      color: #f8fafc;
      padding: 0;
    }

    .auth-input-wrap input::placeholder {
      color: #64748b;
    }

    .auth-submit {
      min-height: 48px;
      width: 100%;
      border-radius: 16px;
    }

    .auth-icon {
      width: 56px;
      height: 56px;
      display: grid;
      place-items: center;
      border-radius: 19px;
      color: #04111f;
      background: linear-gradient(135deg, #38bdf8, #22c55e);
      box-shadow: 0 0 50px rgba(56, 189, 248, 0.24);
    }

    .auth-error {
      color: #fecaca;
      border: 1px solid rgba(239, 68, 68, 0.28);
      background: rgba(239, 68, 68, 0.1);
      border-radius: 14px;
      padding: 10px 12px;
      font-weight: 850;
    }

    @media (max-width: 900px) {
      .dashboard-auth-layout {
        grid-template-columns: 1fr;
      }

      .auth-feature-grid {
        grid-template-columns: 1fr;
      }
    }
    '''

    if ".dashboard-auth-layout" not in existing:
      css_path.write_text(existing + "\n\n" + textwrap.dedent(auth_css), encoding="utf-8")
    else:
      css_path.write_text(existing + "\n\n/* refreshed sign-in/sign-up auth styles */\n" + textwrap.dedent(auth_css), encoding="utf-8")

    write("docs/DASHBOARD_AUTH.md", r'''
    # Dashboard Auth

    The dashboard now has a sign in / sign up concept screen with:

    ```txt
    email field
    password field
    confirm password field for sign up
    name field for sign up
    no visible draft password
    no exposed API keys
    ```

    ## Current State

    This is still a concept/demo auth gate. It uses browser session storage after a successful local draft credential check.

    The draft password is not shown in the UI.

    ## Production Upgrade Path

    Replace the current component with one of:

    ```txt
    Cloudflare Access
    Supabase Auth
    Worker-backed session cookies
    Google OAuth
    GitHub OAuth
    Magic link via Resend
    ```

    ## Recommended Production Auth Flow

    ```txt
    POST /api/auth/signin
    POST /api/auth/signup
    POST /api/auth/signout
    GET  /api/auth/session
    ```

    Server should:

    ```txt
    hash passwords
    use secure HttpOnly cookies
    rotate sessions
    enforce roles
    log admin activity
    rate-limit login attempts
    never expose secrets to the browser
    ```

    ## Important

    Do not ship the concept password gate as final production security.
    ''')

    run(["npm", "run", "build"], check=True)
    run(["git", "add", "src/dashboard/components/DashboardAuthGate.jsx", "src/dashboard/dashboard.css", "docs/DASHBOARD_AUTH.md"], check=True)
    run(["git", "commit", "-m", "feat: add dashboard sign in and sign up auth screen"], check=False)

    print("\nDashboard sign in / sign up auth screen added.")
    print("Next:")
    print("npm run deploy")
    print("git push origin main")

if __name__ == "__main__":
    main()
