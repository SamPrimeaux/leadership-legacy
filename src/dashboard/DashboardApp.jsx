import { Routes, Route, Navigate } from "react-router-dom";
import { DashboardAuthGate } from "./components/DashboardAuthGate.jsx";
import { AgentIDE } from "./pages/AgentIDE.jsx";

export default function DashboardApp() {
  return (
    <DashboardAuthGate>
      <Routes>
        <Route path="/dashboard" element={<AgentIDE routeView="home" />} />
        <Route path="/dashboard/agent" element={<AgentIDE routeView="agent" />} />
        <Route path="/dashboard/dev" element={<AgentIDE routeView="agent" />} />
        <Route path="/dashboard/dev/editor" element={<AgentIDE routeView="agent" />} />
        <Route path="/dashboard/dev/terminal" element={<AgentIDE routeView="agent" initialTerminalOpen />} />

        <Route path="/dashboard/storage" element={<AgentIDE routeView="storage" />} />
        <Route path="/dashboard/settings" element={<AgentIDE routeView="settings" />} />
        <Route path="/dashboard/settings/ai-providers" element={<AgentIDE routeView="settings" />} />
        <Route path="/dashboard/analytics" element={<AgentIDE routeView="analytics" />} />
        <Route path="/dashboard/learn" element={<AgentIDE routeView="learn" />} />
        <Route path="/dashboard/mail" element={<AgentIDE routeView="mail" />} />
        <Route path="/dashboard/mcp" element={<AgentIDE routeView="mcp" />} />

        <Route path="/dashboard/pages" element={<AgentIDE routeView="cms" />} />
        <Route path="/dashboard/media" element={<AgentIDE routeView="storage" />} />
        <Route path="/dashboard/case-studies" element={<AgentIDE routeView="cms" />} />
        <Route path="/dashboard/services" element={<AgentIDE routeView="cms" />} />
        <Route path="/dashboard/leads" element={<AgentIDE routeView="analytics" />} />

        <Route path="/dashboard/login" element={<Navigate to="/dashboard" replace />} />
        <Route path="*" element={<AgentIDE routeView="agent" />} />
      </Routes>
    </DashboardAuthGate>
  );
}
