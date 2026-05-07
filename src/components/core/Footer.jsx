import { Link } from "react-router-dom";
import { ArrowUpRight } from "lucide-react";
import { navItems } from "../../config/nav.config.js";
import "./core.css";

export function Footer() {
  return (
    <footer className="site-footer">
      <div className="container footer-feature glass-card">
        <p className="eyebrow">Leadership Legacy Digital</p>
        <h2>Engineering-grade AI systems for technical businesses.</h2>
        <p>
          Connor McNeely blends mechanical engineering discipline with AI systems,
          automation, CAD workflows, RAG, and full-stack product development.
        </p>
        <div className="footer-feature-actions">
          <Link className="btn" to="/contact">Start a Project</Link>
          <Link className="btn secondary" to="/work">View Work</Link>
        </div>
      </div>

      <div className="container footer-grid">
        <div>
          <Link className="brand footer-brand" to="/">
            <span className="brand-mark">LL</span>
            <span className="brand-copy">
              <strong>Leadership Legacy</strong>
              <small>Connor McNeely</small>
            </span>
          </Link>
          <p>
            Mechanical engineering precision, AI workflow design, and production-minded
            software delivery for teams that need systems that hold up.
          </p>
        </div>

        <div className="footer-column">
          <h3>Site</h3>
          {navItems.map((item) => (
            <Link key={item.href} to={item.href}>{item.label}</Link>
          ))}
        </div>

        <div className="footer-column">
          <h3>Build lanes</h3>
          <Link to="/services/ai-engineering">AI Engineering</Link>
          <Link to="/services/rag-systems">RAG Systems</Link>
          <Link to="/services/cad-automation">CAD Automation</Link>
          <Link to="/services/full-stack-apps">Full-Stack Apps</Link>
        </div>

        <div className="footer-column">
          <h3>Operations</h3>
          <a href="/dashboard">Dashboard <ArrowUpRight size={13} /></a>
          <Link to="/privacy">Privacy</Link>
          <Link to="/terms">Terms</Link>
        </div>
      </div>

      <div className="container footer-bottom">
        <span>© {new Date().getFullYear()} Leadership Legacy Digital.</span>
        <span>Built for precision, clarity, and real-world systems.</span>
      </div>
    </footer>
  );
}
