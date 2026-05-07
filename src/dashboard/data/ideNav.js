import {
  Home,
  Code2,
  TerminalSquare,
  Bot,
  FileText,
  Image,
  Database,
  Briefcase,
  Wrench,
  Inbox,
  BarChart3,
  Rocket,
  Settings,
  BrainCircuit
} from "lucide-react";

export const idePrimaryNav = [
  { label: "Home", href: "/dashboard", icon: Home },
  { label: "IDE Workspace", href: "/dashboard/dev", icon: Code2 },
  { label: "Terminal", href: "/dashboard/dev/terminal", icon: TerminalSquare },
  { label: "AI Agent", href: "/dashboard/dev/agent", icon: Bot }
];

export const ideCMSNav = [
  { label: "Pages", href: "/dashboard/pages", icon: FileText },
  { label: "Media", href: "/dashboard/media", icon: Image },
  { label: "R2 Storage", href: "/dashboard/storage", icon: Database },
  { label: "Case Studies", href: "/dashboard/case-studies", icon: Briefcase },
  { label: "Services", href: "/dashboard/services", icon: Wrench },
  { label: "Leads", href: "/dashboard/leads", icon: Inbox },
  { label: "Analytics", href: "/dashboard/analytics", icon: BarChart3 },
  { label: "Publishing", href: "/dashboard/publishing", icon: Rocket },
  { label: "AI Providers", href: "/dashboard/settings/ai-providers", icon: BrainCircuit },
  { label: "Settings", href: "/dashboard/settings", icon: Settings }
];
