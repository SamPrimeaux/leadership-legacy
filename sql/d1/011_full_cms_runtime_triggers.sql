-- D1 CMS triggers for timestamps and activity.
PRAGMA foreign_keys = ON;

CREATE TRIGGER IF NOT EXISTS trg_cms_pages_updated_at
AFTER UPDATE ON cms_pages
FOR EACH ROW
BEGIN
  UPDATE cms_pages SET updated_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_cms_page_sections_updated_at
AFTER UPDATE ON cms_page_sections
FOR EACH ROW
BEGIN
  UPDATE cms_page_sections SET updated_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_cms_assets_updated_at
AFTER UPDATE ON cms_assets
FOR EACH ROW
BEGIN
  UPDATE cms_assets SET updated_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_cms_leads_updated_at
AFTER UPDATE ON cms_leads
FOR EACH ROW
BEGIN
  UPDATE cms_leads SET updated_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_cms_services_updated_at
AFTER UPDATE ON cms_services
FOR EACH ROW
BEGIN
  UPDATE cms_services SET updated_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_cms_case_studies_updated_at
AFTER UPDATE ON cms_case_studies
FOR EACH ROW
BEGIN
  UPDATE cms_case_studies SET updated_at = datetime('now') WHERE id = NEW.id;
END;
