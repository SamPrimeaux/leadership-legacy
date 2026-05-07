import {
  LayoutDashboard,
  FileText,
  Layers,
  Image,
  Briefcase,
  Wrench,
  Inbox,
  ClipboardList,
  BarChart3,
  Rocket,
  Settings,
  BrainCircuit
} from "lucide-react";

export const dashboardNav = [
  { label: "Overview", href: "/dashboard", icon: LayoutDashboard },
  { label: "Pages", href: "/dashboard/pages", icon: FileText },
  { label: "Sections", href: "/dashboard/sections", icon: Layers },
  { label: "Media", href: "/dashboard/media", icon: Image },
  { label: "Case Studies", href: "/dashboard/case-studies", icon: Briefcase },
  { label: "Services", href: "/dashboard/services", icon: Wrench },
  { label: "Leads", href: "/dashboard/leads", icon: Inbox },
  { label: "Forms", href: "/dashboard/forms", icon: ClipboardList },
  { label: "Analytics", href: "/dashboard/analytics", icon: BarChart3 },
  { label: "Publishing", href: "/dashboard/publishing", icon: Rocket },
  { label: "AI Providers", href: "/dashboard/settings/ai-providers", icon: BrainCircuit },
  { label: "Settings", href: "/dashboard/settings", icon: Settings }
];
