import { Link, Route, Routes } from "react-router-dom";

const services = [
  "AI Engineering",
  "RAG Systems",
  "Full-Stack Apps",
  "CAD Automation",
  "CAD-to-Video",
  "Business Automation",
  "Consulting"
];

function Header() {
  return (
    <header style={{
      position: "sticky",
      top: 0,
      zIndex: 20,
      borderBottom: "1px solid var(--color-border)",
      background: "rgba(7,11,18,.78)",
      backdropFilter: "blur(18px)"
    }}>
      <div className="container" style={{
        height: "var(--header-height)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: 24
      }}>
        <Link to="/" style={{ fontWeight: 900 }}>Leadership Legacy</Link>
        <nav style={{ display: "flex", gap: 18, color: "var(--color-text-muted)", fontWeight: 800 }}>
          <Link to="/services">Services</Link>
          <Link to="/work">Work</Link>
          <Link to="/about">About</Link>
          <Link to="/resources">Resources</Link>
          <Link to="/contact">Contact</Link>
          <a href="/dashboard">Dashboard</a>
        </nav>
      </div>
    </header>
  );
}

function Footer() {
  return (
    <footer className="section" style={{ borderTop: "1px solid var(--color-border)" }}>
      <div className="container">
        <p className="eyebrow">Leadership Legacy Digital</p>
        <h2 className="section-title">Engineering-grade AI systems for technical businesses.</h2>
        <p className="muted">
          Connor McNeely blends mechanical engineering discipline with AI systems,
          automation, CAD workflows, RAG, and full-stack product development.
        </p>
      </div>
    </footer>
  );
}

function Home() {
  return (
    <>
      <section className="section">
        <div className="container">
          <p className="eyebrow">Mechanical Engineer × AI Developer</p>
          <h1 className="section-title">Engineering-grade AI systems for technical businesses.</h1>
          <p className="muted">
            Connor McNeely helps engineering teams, SaaS founders, and operators turn
            complex workflows, documents, CAD assets, and business bottlenecks into
            production-ready AI tools, automations, and web applications.
          </p>
          <div style={{ display: "flex", gap: 12, marginTop: 28, flexWrap: "wrap" }}>
            <Link className="btn" to="/contact">Start a Project</Link>
            <Link className="btn secondary" to="/work">View Work</Link>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <p className="eyebrow">Services</p>
          <h2 className="section-title">AI systems, automation, CAD, and full-stack builds.</h2>
          <div className="card-grid">
            {services.map((service) => (
              <article className="card" key={service}>
                <h3>{service}</h3>
                <p>Production-ready service track for technical businesses.</p>
              </article>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}

function Page({ title }) {
  return (
    <section className="section">
      <div className="container">
        <p className="eyebrow">Leadership Legacy Digital</p>
        <h1 className="section-title">{title}</h1>
        <p className="muted">
          This route is scaffolded and ready for full content, CMS wiring, SEO metadata,
          media, and production components.
        </p>
      </div>
    </section>
  );
}

export default function App() {
  return (
    <>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<Page title="About Connor McNeely" />} />
          <Route path="/services" element={<Page title="Services" />} />
          <Route path="/services/:slug" element={<Page title="Service Detail" />} />
          <Route path="/work" element={<Page title="Work" />} />
          <Route path="/work/:slug" element={<Page title="Case Study" />} />
          <Route path="/resources" element={<Page title="Resources" />} />
          <Route path="/resources/:slug" element={<Page title="Resource" />} />
          <Route path="/contact" element={<Page title="Project Intake" />} />
          <Route path="/privacy" element={<Page title="Privacy Policy" />} />
          <Route path="/terms" element={<Page title="Terms of Use" />} />
        </Routes>
      </main>
      <Footer />
    </>
  );
}
