import { Routes, Route, Navigate } from "react-router-dom";
import { DashboardAuthGate } from "./components/DashboardAuthGate.jsx";
import { AgentIDE } from "./pages/AgentIDE.jsx";

export default function DashboardApp() {
  return (
    <DashboardAuthGate>
      <Routes>
        <Route path="/dashboard" element={<AgentIDE />} />
        <Route path="/dashboard/agent" element={<AgentIDE />} />
        <Route path="/dashboard/dev" element={<AgentIDE />} />
        <Route path="/dashboard/dev/editor" element={<AgentIDE />} />
        <Route path="/dashboard/dev/terminal" element={<AgentIDE initialTerminalOpen />} />
        <Route path="/dashboard/dev/agent" element={<AgentIDE />} />
        <Route path="/dashboard/pages" element={<AgentIDE activeSidePanel="pages" />} />
        <Route path="/dashboard/media" element={<AgentIDE activeSidePanel="media" />} />
        <Route path="/dashboard/storage" element={<AgentIDE activeSidePanel="storage" />} />
        <Route path="/dashboard/case-studies" element={<AgentIDE activeSidePanel="work" />} />
        <Route path="/dashboard/services" element={<AgentIDE activeSidePanel="services" />} />
        <Route path="/dashboard/leads" element={<AgentIDE activeSidePanel="leads" />} />
        <Route path="/dashboard/analytics" element={<AgentIDE activeSidePanel="analytics" />} />
        <Route path="/dashboard/settings" element={<AgentIDE activeSidePanel="settings" />} />
        <Route path="/dashboard/settings/ai-providers" element={<AgentIDE activeSidePanel="providers" />} />
        <Route path="/dashboard/login" element={<Navigate to="/dashboard" replace />} />
        <Route path="*" element={<AgentIDE />} />
      </Routes>
    </DashboardAuthGate>
  );
}
