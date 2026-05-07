export const cmsPages = [
  {
    id: "home",
    title: "Home",
    slug: "/",
    status: "published",
    seoScore: 96,
    updatedAt: "2026-05-06",
    sections: [
      {
        id: "hero-home",
        type: "Founder Hero",
        props: {
          eyebrow: "Mechanical Engineer × AI Developer",
          heading: "Engineering-grade AI systems for technical businesses.",
          body:
            "Connor McNeely helps engineering teams, SaaS founders, and operators turn complex workflows, documents, CAD assets, and business bottlenecks into production-ready AI tools, automations, and web applications.",
          primaryCta: "Start a Project",
          secondaryCta: "View Work"
        }
      },
      {
        id: "services-home",
        type: "Services Grid",
        props: {
          heading: "AI systems, automation, CAD, and full-stack builds."
        }
      },
      {
        id: "work-home",
        type: "Featured Work",
        props: {
          heading: "Technical systems with practical outcomes."
        }
      }
    ]
  },
  {
    id: "about",
    title: "About",
    slug: "/about",
    status: "published",
    seoScore: 91,
    updatedAt: "2026-05-06",
    sections: []
  },
  {
    id: "services",
    title: "Services",
    slug: "/services",
    status: "draft",
    seoScore: 84,
    updatedAt: "2026-05-06",
    sections: []
  },
  {
    id: "work",
    title: "Work",
    slug: "/work",
    status: "review",
    seoScore: 88,
    updatedAt: "2026-05-06",
    sections: []
  }
];

export const services = [
  {
    id: "ai-engineering",
    title: "AI Engineering",
    slug: "/services/ai-engineering",
    status: "published",
    price: "$5,000+",
    summary: "Custom AI tools, copilots, LLM integrations, and multi-agent workflows."
  },
  {
    id: "rag-systems",
    title: "RAG Systems",
    slug: "/services/rag-systems",
    status: "published",
    price: "$5,000+",
    summary: "Source-cited document intelligence for manuals, SOPs, support docs, and standards."
  },
  {
    id: "full-stack-apps",
    title: "Full-Stack AI Apps",
    slug: "/services/full-stack-apps",
    status: "draft",
    price: "$8,000+",
    summary: "React/Vite apps, dashboards, APIs, auth, database, payments, and AI features."
  },
  {
    id: "cad-automation",
    title: "CAD Automation",
    slug: "/services/cad-automation",
    status: "published",
    price: "$75/hr",
    summary: "SolidWorks workflows, BOM automation, drawings, and engineering documentation."
  }
];

export const caseStudies = [
  {
    id: "mechassist-ai",
    title: "MechAssist AI",
    category: "RAG / Engineering AI",
    status: "published",
    stack: ["RAG", "Vector Search", "LLM", "Engineering Docs"],
    outcome: "Faster source-backed answers for technical documentation."
  },
  {
    id: "openclaw",
    title: "OpenClaw",
    category: "Multi-Agent AI",
    status: "draft",
    stack: ["Agents", "Automation", "CRM", "LLM"],
    outcome: "A live outbound AI workflow foundation."
  },
  {
    id: "evergrow-landscaping",
    title: "Evergrow Landscaping",
    category: "Lead Generation / CRM",
    status: "published",
    stack: ["Website", "CRM", "Chatbot", "Automation"],
    outcome: "Improved lead capture and structured follow-up."
  }
];

export const leads = [
  {
    id: "lead_001",
    name: "Jordan Blake",
    email: "jordan@example.com",
    company: "Precision Pump Group",
    projectType: "RAG System",
    budget: "$5k–$15k",
    status: "new",
    source: "/services/rag-systems",
    createdAt: "2026-05-06"
  },
  {
    id: "lead_002",
    name: "Maya Chen",
    email: "maya@example.com",
    company: "CADOps Studio",
    projectType: "CAD Automation",
    budget: "$2k–$8k",
    status: "qualified",
    source: "/contact",
    createdAt: "2026-05-06"
  },
  {
    id: "lead_003",
    name: "Elliot Hayes",
    email: "elliot@example.com",
    company: "Founder",
    projectType: "Full-Stack AI App",
    budget: "$8k–$25k",
    status: "proposal",
    source: "/services/full-stack-apps",
    createdAt: "2026-05-05"
  }
];

export const mediaAssets = [
  {
    id: "asset_001",
    name: "Connor Founder Portrait",
    type: "image",
    usage: "Founder",
    status: "ready",
    size: "420 KB"
  },
  {
    id: "asset_002",
    name: "Engineering Blueprint Texture",
    type: "texture",
    usage: "Background",
    status: "ready",
    size: "180 KB"
  },
  {
    id: "asset_003",
    name: "Rotating Pump GLB",
    type: "model",
    usage: "Hero / CAD",
    status: "needs optimization",
    size: "4.8 MB"
  }
];

export const analyticsEvents = [
  { page: "/", views: 1240, cta: 88, leads: 12, conversion: "0.97%" },
  { page: "/services/rag-systems", views: 420, cta: 44, leads: 7, conversion: "1.67%" },
  { page: "/work/mechassist-ai", views: 318, cta: 21, leads: 3, conversion: "0.94%" },
  { page: "/contact", views: 210, cta: 0, leads: 18, conversion: "8.57%" }
];
