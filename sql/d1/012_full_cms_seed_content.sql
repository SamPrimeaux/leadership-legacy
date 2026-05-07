-- Leadership Legacy starter content seed for D1.
PRAGMA foreign_keys = ON;

INSERT OR IGNORE INTO cms_templates (
  id,
  tenant_id,
  workspace_id,
  template_key,
  name,
  template_type,
  schema_json,
  default_sections_json
) VALUES
  (
    'template_landing',
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'landing',
    'Landing Page',
    'landing',
    json_object('supports_sections', 1),
    json_array('heroConnor', 'servicesGrid', 'caseStudyGrid', 'founderStory', 'contactBand')
  ),
  (
    'template_service',
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'service',
    'Service Page',
    'service',
    json_object('supports_sections', 1),
    json_array('serviceHero', 'serviceDeliverables', 'serviceUseCases', 'contactBand')
  ),
  (
    'template_case_study',
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'case_study',
    'Case Study Page',
    'case_study',
    json_object('supports_sections', 1),
    json_array('caseStudyHero', 'problemSolution', 'stack', 'outcome', 'contactBand')
  );

INSERT OR IGNORE INTO cms_pages (
  id,
  tenant_id,
  workspace_id,
  title,
  slug,
  route_path,
  page_type,
  status,
  template_id,
  seo_json,
  draft_json,
  published_json
) VALUES
  (
    'page_about',
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'About',
    'about',
    '/about',
    'page',
    'published',
    'template_landing',
    json_object('title','About Connor McNeely','description','Mechanical engineer and AI developer building engineering-grade AI systems.'),
    json_object('sections', json_array()),
    json_object('sections', json_array())
  ),
  (
    'page_services',
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'Services',
    'services',
    '/services',
    'page',
    'published',
    'template_landing',
    json_object('title','Services | Leadership Legacy Digital','description','AI engineering, RAG systems, CAD automation, and full-stack app development.'),
    json_object('sections', json_array()),
    json_object('sections', json_array())
  ),
  (
    'page_work',
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'Work',
    'work',
    '/work',
    'page',
    'published',
    'template_landing',
    json_object('title','Work | Leadership Legacy Digital','description','Case studies for technical AI systems and automation workflows.'),
    json_object('sections', json_array()),
    json_object('sections', json_array())
  ),
  (
    'page_contact',
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'Contact',
    'contact',
    '/contact',
    'page',
    'published',
    'template_landing',
    json_object('title','Contact | Leadership Legacy Digital','description','Start a project with Connor McNeely and Leadership Legacy Digital.'),
    json_object('sections', json_array()),
    json_object('sections', json_array())
  );

INSERT OR IGNORE INTO cms_services (
  id,
  tenant_id,
  workspace_id,
  slug,
  title,
  eyebrow,
  summary,
  starting_at,
  deliverables_json,
  use_cases_json,
  stack_json,
  status,
  order_index
) VALUES
  (
    'service_ai_engineering',
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'ai-engineering',
    'AI Engineering',
    'Custom AI Systems',
    'Production-ready AI tools, copilots, and multi-agent workflows designed around real business processes.',
    '$5,000+',
    json_array('LLM integration', 'Agent workflows', 'Prompt systems', 'Tool routing', 'Deployment'),
    json_array('Internal copilots', 'Workflow automation', 'Technical assistants', 'AI-enabled dashboards'),
    json_array('OpenAI', 'Anthropic', 'Cloudflare Workers', 'D1', 'R2'),
    'published',
    10
  ),
  (
    'service_rag_systems',
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'rag-systems',
    'RAG Systems',
    'Document Intelligence',
    'Source-cited knowledge systems for engineering documents, SOPs, manuals, support libraries, and standards.',
    '$5,000+',
    json_array('Document ingestion', 'Embeddings', 'Retrieval tuning', 'Source citations', 'Admin UI'),
    json_array('Technical docs', 'Internal knowledge', 'Support automation', 'Standards lookup'),
    json_array('Vector Search', 'Postgres', 'Cloudflare Vectorize', 'OpenAI', 'Anthropic'),
    'published',
    20
  ),
  (
    'service_full_stack_apps',
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'full-stack-apps',
    'Full-Stack AI Apps',
    'SaaS & Dashboards',
    'React/Vite apps, dashboards, APIs, auth, database, payments, and AI features packaged into deployable applications.',
    '$8,000+',
    json_array('React app', 'API design', 'Database schema', 'Auth', 'Payments', 'Deployment'),
    json_array('AI SaaS MVPs', 'Admin dashboards', 'Customer portals', 'Internal tools'),
    json_array('React', 'Vite', 'Cloudflare Workers', 'D1', 'R2', 'Stripe', 'Resend'),
    'published',
    30
  ),
  (
    'service_cad_automation',
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'cad-automation',
    'CAD Automation',
    'Engineering Workflow Automation',
    'Automate repetitive CAD, drawing, BOM, and engineering documentation workflows.',
    '$75/hr',
    json_array('SolidWorks automation', 'BOM workflows', 'Drawing automation', 'CAD file structure'),
    json_array('Design iteration reduction', 'Drawing generation', 'Engineering calculators', 'Technical configurators'),
    json_array('SolidWorks', 'CAD', 'Python', 'Automation', 'Engineering Docs'),
    'published',
    40
  );

INSERT OR IGNORE INTO cms_case_studies (
  id,
  tenant_id,
  workspace_id,
  slug,
  title,
  category,
  summary,
  problem,
  solution,
  outcome,
  stack_json,
  metrics_json,
  status,
  featured,
  order_index
) VALUES
  (
    'case_mechassist_ai',
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'mechassist-ai',
    'MechAssist AI',
    'RAG / Engineering AI',
    'A mechanical engineering assistant designed to retrieve, reason over, and cite technical documentation.',
    'Engineering knowledge is scattered across manuals, standards, docs, and tribal workflows.',
    'A RAG system that retrieves relevant technical content and returns source-backed answers.',
    'Faster access to technical knowledge and a foundation for engineering-specific copilots.',
    json_array('RAG', 'Vector Search', 'LLM', 'Engineering Docs'),
    json_object('status','concept_proof'),
    'published',
    1,
    10
  ),
  (
    'case_openclaw',
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'openclaw',
    'OpenClaw',
    'Multi-Agent AI',
    'A live outbound AI agent system for automation, sales workflows, and campaign execution.',
    'Outbound workflows require research, personalization, follow-up, and structured task execution.',
    'A multi-agent workflow foundation for intelligent outreach and campaign execution.',
    'A clearer path toward automated outbound systems with human oversight.',
    json_array('Agents', 'Automation', 'CRM', 'LLM'),
    json_object('status','draft'),
    'draft',
    1,
    20
  );
