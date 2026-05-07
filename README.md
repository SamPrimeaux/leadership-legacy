Build a production-ready multi-page Vite + React app for Connor McNeely and Leadership Legacy Digital.

The app should feel like a premium technical founder portfolio plus AI engineering studio, not a generic agency template.

Brand positioning:
- Connor McNeely is a Mechanical Engineer × AI Developer.
- Leadership Legacy Digital is the delivery brand for AI systems, automation, CAD workflows, RAG systems, and full-stack applications.
- Core message: engineering-grade AI systems for technical businesses.
- Visual tone: dark premium SaaS, engineering blueprint, AI neural systems, industrial precision, clean founder-led trust.

Implement this as a modular Vite/React app with:
- React Router
- Clean file tree under src/
- Data-driven content files under src/data/
- Config-driven nav, SEO, services, and brand tokens
- Reusable layouts
- Reusable UI components
- Fully responsive design
- Reduced-motion fallbacks
- Accessible buttons, forms, menus, and headings
- No stubs or placeholder-only components
- No emoji usage in UI copy

Required routes:
/
 /about
 /services
 /services/ai-engineering
 /services/rag-systems
 /services/full-stack-apps
 /services/cad-automation
 /services/cad-to-video
 /services/business-automation
 /services/consulting
 /work
 /work/mechassist-ai
 /work/openclaw
 /work/evergrow-landscaping
 /work/ai-meal-planner
 /work/engineercad
 /resources
 /resources/engineering-ai-playbook
 /resources/rag-readiness-checklist
 /resources/automation-roi
 /contact
 /privacy
 /terms

Use these directories:
src/components/core
src/components/ui
src/components/visual
src/components/sections
src/components/services
src/components/cases
src/components/forms
src/components/agent
src/pages
src/pages/services
src/pages/work
src/pages/resources
src/pages/legal
src/data
src/config
src/hooks
src/lib
src/styles
public/images
public/models
public/downloads
docs
scripts

Create:
- Header with dropdown nav and mobile menu
- Footer with Connor + Leadership Legacy positioning
- Homepage with hero, services, case studies, founder story, process, CTA, FAQ
- Services overview and individual service pages
- Work overview and individual case study pages
- About page focused on Connor’s engineering-to-AI story
- Contact page with project intake form
- Resources landing and resource pages
- Legal pages
- SEO metadata per page
- Sitemap generation script
- Strong responsive CSS system using tokens.css

Brand tokens:
Background: #070b12
Soft background: #0d1320
Surface: #111827
Elevated surface: #172033
Text: #f5f7fb
Muted text: #9ca8bd
Primary: #38bdf8
Primary strong: #0ea5e9
Accent: #22c55e
Warm accent: #f59e0b
Border: rgba(148, 163, 184, 0.18)
Glass: rgba(15, 23, 42, 0.72)

Typography:
Display: Satoshi or Inter fallback
Body: Inter
Mono: JetBrains Mono

Motion:
- subtle scroll reveals
- blueprint grid movement
- card lift hover
- AI node pulse
- header blur on scroll
- respect prefers-reduced-motion

The app should be polished enough to deploy as a real client-facing site. connor-leadershiplegacy-app/
├── src/
│   ├── public-app/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   └── routes.jsx
│   │
│   ├── dashboard/
│   │   ├── main.jsx
│   │   ├── DashboardApp.jsx
│   │   ├── dashboard.routes.jsx
│   │   ├── dashboard.config.js
│   │   ├── dashboard.css
│   │   │
│   │   ├── layouts/
│   │   │   ├── DashboardShell.jsx
│   │   │   ├── EditorLayout.jsx
│   │   │   ├── PreviewLayout.jsx
│   │   │   └── AuthLayout.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── DashboardHome.jsx
│   │   │   ├── CMSPages.jsx
│   │   │   ├── CMSPageEditor.jsx
│   │   │   ├── Sections.jsx
│   │   │   ├── MediaLibrary.jsx
│   │   │   ├── CaseStudies.jsx
│   │   │   ├── CaseStudyEditor.jsx
│   │   │   ├── Services.jsx
│   │   │   ├── ServiceEditor.jsx
│   │   │   ├── Leads.jsx
│   │   │   ├── LeadDetail.jsx
│   │   │   ├── IntakeForms.jsx
│   │   │   ├── Analytics.jsx
│   │   │   ├── Settings.jsx
│   │   │   ├── BrandSettings.jsx
│   │   │   ├── NavigationSettings.jsx
│   │   │   ├── SEOSettings.jsx
│   │   │   ├── Publishing.jsx
│   │   │   └── NotFoundDashboard.jsx
│   │   │
│   │   ├── components/
│   │   │   ├── shell/
│   │   │   │   ├── DashboardSidebar.jsx
│   │   │   │   ├── DashboardTopbar.jsx
│   │   │   │   ├── CommandMenu.jsx
│   │   │   │   ├── QuickActions.jsx
│   │   │   │   └── SaveStatus.jsx
│   │   │   │
│   │   │   ├── editor/
│   │   │   │   ├── LivePageEditor.jsx
│   │   │   │   ├── SectionTree.jsx
│   │   │   │   ├── SectionInspector.jsx
│   │   │   │   ├── FieldRenderer.jsx
│   │   │   │   ├── RichTextEditor.jsx
│   │   │   │   ├── CodeBlockEditor.jsx
│   │   │   │   ├── SEOInspector.jsx
│   │   │   │   ├── StyleInspector.jsx
│   │   │   │   ├── PublishPanel.jsx
│   │   │   │   ├── VersionHistory.jsx
│   │   │   │   ├── PreviewFrame.jsx
│   │   │   │   ├── SplitPreview.jsx
│   │   │   │   └── DevicePreviewToggle.jsx
│   │   │   │
│   │   │   ├── media/
│   │   │   │   ├── MediaUploader.jsx
│   │   │   │   ├── MediaGrid.jsx
│   │   │   │   ├── MediaDetailDrawer.jsx
│   │   │   │   ├── AssetPicker.jsx
│   │   │   │   └── ImageOptimizerPanel.jsx
│   │   │   │
│   │   │   ├── tables/
│   │   │   │   ├── DataTable.jsx
│   │   │   │   ├── TableToolbar.jsx
│   │   │   │   ├── StatusBadge.jsx
│   │   │   │   └── EmptyState.jsx
│   │   │   │
│   │   │   ├── forms/
│   │   │   │   ├── DashboardInput.jsx
│   │   │   │   ├── DashboardTextarea.jsx
│   │   │   │   ├── DashboardSelect.jsx
│   │   │   │   ├── SlugField.jsx
│   │   │   │   ├── JsonField.jsx
│   │   │   │   └── FormBuilder.jsx
│   │   │   │
│   │   │   └── preview/
│   │   │       ├── PublicPageRenderer.jsx
│   │   │       ├── SectionRenderer.jsx
│   │   │       ├── DraftPreviewBanner.jsx
│   │   │       └── RealtimePreviewBridge.jsx
│   │   │
│   │   ├── hooks/
│   │   │   ├── useDashboardAuth.js
│   │   │   ├── useAutosave.js
│   │   │   ├── useRealtimePreview.js
│   │   │   ├── useVersionHistory.js
│   │   │   ├── useDirtyState.js
│   │   │   └── useMediaLibrary.js
│   │   │
│   │   ├── lib/
│   │   │   ├── dashboardApi.js
│   │   │   ├── cmsClient.js
│   │   │   ├── sectionRegistry.js
│   │   │   ├── validators.js
│   │   │   ├── publishing.js
│   │   │   ├── previewBus.js
│   │   │   └── permissions.js
│   │   │
│   │   └── data/
│   │       ├── dashboardNav.js
│   │       ├── sectionSchemas.js
│   │       ├── fieldSchemas.js
│   │       └── defaultPages.js
│   │
│   ├── shared/
│   │   ├── brand/
│   │   │   ├── tokens.css
│   │   │   ├── brand.config.js
│   │   │   └── theme.js
│   │   ├── components/
│   │   ├── data/
│   │   └── lib/
│   │
│   └── styles/
│
├── dashboard.html
├── index.html
└── vite.config.js 
