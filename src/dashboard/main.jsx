import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import DashboardApp from "./DashboardApp.jsx";
import "./dashboard.css";

createRoot(document.getElementById("dashboard-root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <DashboardApp />
    </BrowserRouter>
  </React.StrictMode>
);
