import { Routes, Route, Navigate } from "react-router-dom";
import { IDELayout } from "./layouts/IDELayout.jsx";
import { DashboardAuthGate } from "./components/DashboardAuthGate.jsx";
import { IDEHome } from "./pages/IDEHome.jsx";
import { IDEWorkspace } from "./pages/IDEWorkspace.jsx";
import { CMSPages } from "./pages/CMSPages.jsx";
import { CMSPageEditor } from "./pages/CMSPageEditor.jsx";
import { MediaLibrary } from "./pages/MediaLibrary.jsx";
import { R2Storage } from "./pages/R2Storage.jsx";
import { CaseStudies } from "./pages/CaseStudies.jsx";
import { Services } from "./pages/Services.jsx";
import { Leads } from "./pages/Leads.jsx";
import { IntakeForms } from "./pages/IntakeForms.jsx";
import { Analytics } from "./pages/Analytics.jsx";
import { Publishing } from "./pages/Publishing.jsx";
import { Settings } from "./pages/Settings.jsx";
import { AIProviders } from "./pages/AIProviders.jsx";
import { NotFoundDashboard } from "./pages/NotFoundDashboard.jsx";

export default function DashboardApp() {
  return (
    <DashboardAuthGate>
      <IDELayout>
        <Routes>
          <Route path="/dashboard" element={<IDEHome />} />
          <Route path="/dashboard/dev" element={<IDEWorkspace />} />
          <Route path="/dashboard/dev/editor" element={<IDEWorkspace startTab="editor" />} />
          <Route path="/dashboard/dev/terminal" element={<IDEWorkspace startTab="terminal" />} />
          <Route path="/dashboard/dev/agent" element={<IDEWorkspace startTab="agent" />} />
          <Route path="/dashboard/pages" element={<CMSPages />} />
          <Route path="/dashboard/pages/:pageId" element={<CMSPageEditor />} />
          <Route path="/dashboard/sections" element={<CMSPages />} />
          <Route path="/dashboard/media" element={<MediaLibrary />} />
          <Route path="/dashboard/storage" element={<R2Storage />} />
          <Route path="/dashboard/case-studies" element={<CaseStudies />} />
          <Route path="/dashboard/case-studies/:caseStudyId" element={<CaseStudies />} />
          <Route path="/dashboard/services" element={<Services />} />
          <Route path="/dashboard/services/:serviceId" element={<Services />} />
          <Route path="/dashboard/leads" element={<Leads />} />
          <Route path="/dashboard/leads/:leadId" element={<Leads />} />
          <Route path="/dashboard/forms" element={<IntakeForms />} />
          <Route path="/dashboard/analytics" element={<Analytics />} />
          <Route path="/dashboard/publishing" element={<Publishing />} />
          <Route path="/dashboard/settings" element={<Settings />} />
          <Route path="/dashboard/settings/brand" element={<Settings section="brand" />} />
          <Route path="/dashboard/settings/navigation" element={<Settings section="navigation" />} />
          <Route path="/dashboard/settings/seo" element={<Settings section="seo" />} />
          <Route path="/dashboard/settings/ai-providers" element={<AIProviders />} />
          <Route path="/dashboard/login" element={<Navigate to="/dashboard" replace />} />
          <Route path="*" element={<NotFoundDashboard />} />
        </Routes>
      </IDELayout>
    </DashboardAuthGate>
  );
}
