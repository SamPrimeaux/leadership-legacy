import { useState } from "react";
import { LockKeyhole } from "lucide-react";

const STORAGE_KEY = "ll-dashboard-authenticated";
const DRAFT_PASSWORD = "1234";

function hasSession() {
  if (typeof window === "undefined") return false;
  return window.sessionStorage.getItem(STORAGE_KEY) === "true";
}

export function DashboardAuthGate({ children }) {
  const [authenticated, setAuthenticated] = useState(hasSession);
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  function handleSubmit(event) {
    event.preventDefault();

    if (password === DRAFT_PASSWORD) {
      window.sessionStorage.setItem(STORAGE_KEY, "true");
      setAuthenticated(true);
      setError("");
      return;
    }

    setError("Incorrect draft password.");
  }

  if (authenticated) {
    return children;
  }

  return (
    <main className="dashboard-auth-page">
      <form className="dashboard-auth-card" onSubmit={handleSubmit}>
        <div className="auth-icon">
          <LockKeyhole size={24} />
        </div>

        <p className="dash-eyebrow">Protected Draft</p>
        <h1>Leadership Legacy Dashboard</h1>
        <p>
          This concept dashboard is password protected while the CMS, R2, AI routing,
          analytics, and publishing workflows are being drafted.
        </p>

        <label>
          Password
          <input
            autoFocus
            type="password"
            inputMode="numeric"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Enter draft password"
          />
        </label>

        {error ? <span className="auth-error">{error}</span> : null}

        <button className="primary-action" type="submit">
          Unlock Dashboard
        </button>

        <small>Draft password for concept review: 1234</small>
      </form>
    </main>
  );
}
