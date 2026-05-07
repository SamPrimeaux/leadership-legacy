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
