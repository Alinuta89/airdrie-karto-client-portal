#!/usr/bin/env python3
"""Build deterministic client-facing HTML pages for the Airdrie Karto namespace."""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = Path("/tmp/airdrie-karto-audit/api/records/all")
KARTO_NS_URL = "https://main.karto.helpseeker.org/compose/ns/CoA"
REQUEST_PAGE = "/airdrie-karto-client-portal/request-workflow/"
REQUEST_API_ENDPOINT = "https://main.karto.helpseeker.org/api/compose/namespace/437118445986185217/module/437118446006632449/record/"
TICKET_LIST_PAGE = f"{KARTO_NS_URL}/pages/437118446039072769"
DASHBOARD_LIST_PAGE = f"{KARTO_NS_URL}/pages/437118446032453633"
INSIGHT_LIST_PAGE = f"{KARTO_NS_URL}/pages/437535446718873601"


NAV = [
    ("Service Plan", "/airdrie-karto-client-portal/"),
    ("Delivery Library", "/airdrie-karto-client-portal/delivery-library/"),
    ("Request Workflow", "/airdrie-karto-client-portal/request-workflow/"),
    ("Ticket Allowance", "/airdrie-karto-client-portal/subscription/"),
    ("Dashboards", "/airdrie-karto-client-portal/dashboard-gallery/"),
    ("Insights", "/airdrie-karto-client-portal/insights/"),
    ("Data Collection", "/airdrie-karto-client-portal/data-collection/"),
    ("Next Requests", "/airdrie-karto-client-portal/next-requests/"),
]


PUBLIC_DELIVERABLES = [
    {
        "title": "Parking Trade-Off Analysis",
        "area": "Parking, housing affordability, downtown development",
        "status": "Web report",
        "url": "https://hsdeliverables.z9.web.core.windows.net/airdrie/parking-tradeoff/",
    },
    {
        "title": "Digital Billboard Risk Analysis",
        "area": "Risk, litigation exposure, municipal operations",
        "status": "Web report",
        "url": "https://hsdeliverables.z9.web.core.windows.net/airdrie/billboard-risk/index.html?v=3",
    },
    {
        "title": "Youth Service Hubs",
        "area": "Youth services, service navigation, regional gaps",
        "status": "Web report",
        "url": "https://hsdeliverables.z9.web.core.windows.net/karto/kt-016-youth-hubs/?v=4",
    },
    {
        "title": "Regional Housing Coalition Brief",
        "area": "Regional housing coordination and coalition strategy",
        "status": "Web report",
        "url": "https://hsdeliverables.z9.web.core.windows.net/airdrie/mfah/",
    },
    {
        "title": "Housing Pressure Index",
        "area": "Community housing pressure benchmarking",
        "status": "Web dashboard",
        "url": "https://hsdeliverables.z9.web.core.windows.net/pressure-index/",
    },
]


EXTERNAL_REPORTS = [
    {
        "folder": "regional-housing-coalition",
        "title": "Regional Housing Coalition",
        "eyebrow": "Regional Housing Coalition",
        "headline": "Regional housing coalition strategy",
        "copy": "A client-facing wrapper for the regional housing coalition briefing, keeping the Airdrie workspace navigation and header consistent with the rest of the portal.",
        "panel_title": "Published briefing",
        "panel_text": "The source report remains hosted in the protected deliverables container. Use the embedded view below for reading inside Karto or open the report in a new tab.",
        "source_url": "https://hsdeliverables.z9.web.core.windows.net/airdrie/mfah/",
        "source_label": "Open Briefing",
    },
    {
        "folder": "housing-pressure-index",
        "title": "Housing Pressure Index",
        "eyebrow": "Housing Pressure Index",
        "headline": "Housing pressure benchmark dashboard",
        "copy": "A consistent Airdrie portal frame for the pressure-index dashboard, with the same navigation, header, and action pattern as the request workflow.",
        "panel_title": "Interactive dashboard",
        "panel_text": "The dashboard loads below. Open it in a new tab when staff need the largest workspace for filtering or presentation.",
        "source_url": "https://hsdeliverables.z9.web.core.windows.net/pressure-index/",
        "source_label": "Open Dashboard",
    },
    {
        "folder": "digital-billboard-risk-analysis",
        "title": "Digital Billboard Risk Analysis",
        "eyebrow": "Risk Analysis",
        "headline": "Digital billboard risk analysis",
        "copy": "A consistent portal entry for the digital billboard report covering risk, litigation exposure, and municipal operating considerations.",
        "panel_title": "Published web report",
        "panel_text": "The report remains hosted as a standalone deliverable. This wrapper makes it feel native to the Airdrie Karto workspace.",
        "source_url": "https://hsdeliverables.z9.web.core.windows.net/airdrie/billboard-risk/index.html?v=3",
        "source_label": "Open Report",
    },
    {
        "folder": "youth-service-hubs",
        "title": "Youth Service Hubs",
        "eyebrow": "Youth Service Hubs",
        "headline": "Youth service hubs research",
        "copy": "A consistent portal entry for the youth hubs report, linking the deliverable back to the broader Airdrie service-planning workspace.",
        "panel_title": "Published web report",
        "panel_text": "Use this page for client navigation. The embedded report keeps the original research layout intact.",
        "source_url": "https://hsdeliverables.z9.web.core.windows.net/karto/kt-016-youth-hubs/?v=4",
        "source_label": "Open Report",
    },
    {
        "folder": "parking-trade-off-analysis",
        "title": "Parking Trade-Off Analysis",
        "eyebrow": "Parking Trade-Off Analysis",
        "headline": "Parking trade-off report",
        "copy": "A consistent portal entry for the parking trade-off report, connecting parking standards, affordability, downtown development, and council-ready choices.",
        "panel_title": "Published web report",
        "panel_text": "The original report loads below. Use the new-tab action for full-screen review or presentation.",
        "source_url": "https://hsdeliverables.z9.web.core.windows.net/airdrie/parking-tradeoff/index.html?v=2",
        "source_label": "Open Report",
    },
    {
        "folder": "secondary-suites-str",
        "title": "Secondary Suites & STR",
        "eyebrow": "Secondary Suites & STR",
        "headline": "Secondary suites and short-term rentals",
        "copy": "A consistent portal entry for the STR and suite-controls deliverable, tying the report back to Airdrie's housing and HAF work program.",
        "panel_title": "Published web report",
        "panel_text": "The report remains hosted in the deliverables container. This page provides a matching Airdrie portal header and navigation shell.",
        "source_url": "https://hsdeliverables.z9.web.core.windows.net/airdrie/str/index.html?v=1",
        "source_label": "Open Report",
    },
]


STR_DOC_LINKS = [
    {
        "href": "technical-report/",
        "eyebrow": "Technical Report",
        "icon": "menu_book",
        "title": "Source of truth",
        "audience": "For: full-text reference · APA 7 · 20 jurisdictions",
        "description": "Formal report covering the evidence reviews, comparative jurisdictional matrix, equity analysis, and legal-defensibility scorecard with full bibliography. Every claim cited, every assumption stated.",
    },
    {
        "href": "decision-support-brief/",
        "eyebrow": "Decision-Support Brief",
        "icon": "description",
        "title": "The two-page answer",
        "audience": "For: anyone who needs the bottom line fast",
        "description": "Standalone decision-ready brief covering Sections A through F: direct answer on caps, key risks, viable alternatives, STR role, strategic considerations, and evidence-based conclusion.",
    },
    {
        "href": "statements-council/",
        "eyebrow": "Council Briefing",
        "icon": "gavel",
        "title": "For the room where the vote happens",
        "audience": "For: elected council · CISG Standing Committee",
        "description": "Written to be read the morning of a committee meeting. Sequencing-first framing with the Edmonton 50% and Cochrane 232% empirical counter-evidence for swing-vote audiences.",
    },
    {
        "href": "statements-elt/",
        "eyebrow": "ELT Briefing",
        "icon": "summarize",
        "title": "For the CAO and directors",
        "audience": "For: Executive Leadership Team · cross-departmental implementation",
        "description": "HAF compliance risk, Bill 18 and Bill 20 latent exposure, cross-departmental implementation sequencing, and audit readiness for executive decision-makers.",
    },
    {
        "href": "statements-planner/",
        "eyebrow": "Planner Briefing",
        "icon": "architecture",
        "title": "For the team drafting the bylaw",
        "audience": "For: municipal planning staff · bylaw drafting",
        "description": "Bylaw drafting guidance, consolidated peer-jurisdiction parameters, and verification flags for B-30/2024 and B-06/2025 follow-on work. The version planners keep open while writing.",
    },
    {
        "href": "interactive-briefing/",
        "eyebrow": "Interactive Briefing",
        "icon": "dashboard",
        "title": "Branded Policy Briefing",
        "audience": "Full branded briefing",
        "description": "Full branded briefing with council brief, executive briefing, evidence record, and jurisdictional comparison views bundled into a single navigable HTML artifact. The version you share with stakeholders.",
    },
]


NEXT_REQUESTS = [
    {
        "name": "HAF milestone and amendment risk tracker",
        "why": "Airdrie has an active Housing Accelerator Fund agreement and recent tickets are already touching four-homes-per-lot, suite policy, parking, and STR controls.",
        "output": "Monthly brief plus a simple dashboard showing commitments, policy dependencies, council touchpoints, and evidence gaps.",
        "theme": "Housing delivery",
        "hours": 18,
    },
    {
        "name": "Secondary suite and STR measurement program",
        "why": "Existing research flags missing local baselines for suite distribution, complaints, parking saturation, STR listings, and rental-stock conversion.",
        "output": "Data dictionary, intake forms, field workflow, and first 90-day baseline report.",
        "theme": "Data collection",
        "hours": 24,
    },
    {
        "name": "Downtown redevelopment evidence pack",
        "why": "Airdrie's ticket history clusters around downtown revitalization, parking trade-offs, brownfield opportunities, and mixed-use development.",
        "output": "Parcel opportunity scan, policy constraints table, and council-ready redevelopment options brief.",
        "theme": "Downtown",
        "hours": 20,
    },
    {
        "name": "Regional commuter and labour-pressure monitor",
        "why": "The insight library repeatedly connects housing pressure with commuting, labour force, and Calgary-region spillover effects.",
        "output": "Regional dashboard with Airdrie, Calgary, Rocky View County, Cochrane, Chestermere, and Okotoks comparators.",
        "theme": "Regional analysis",
        "hours": 22,
    },
    {
        "name": "Affordable housing grant recipient reporting workflow",
        "why": "Airdrie can reduce manual follow-up by collecting recipient milestones, outputs, documents, and narrative updates in one repeatable workflow.",
        "output": "Structured intake forms, quarterly reporting dashboard, and export-ready grant accountability table.",
        "theme": "Grant reporting",
        "hours": 16,
    },
    {
        "name": "Community engagement synthesis pipeline",
        "why": "Airdrie uses engagement and consultation processes on housing and growth topics; those inputs can be converted into structured themes and action items.",
        "output": "Survey/interview coding framework, respondent-theme dashboard, and council summary template.",
        "theme": "Engagement",
        "hours": 14,
    },
]


def read_json(path: Path):
    return json.loads(path.read_text())


def values_map(values):
    out = {}
    for item in values or []:
        key = item.get("name")
        value = item.get("value")
        if not key:
            continue
        if key in out:
            if not isinstance(out[key], list):
                out[key] = [out[key]]
            out[key].append(value)
        else:
            out[key] = value
    return out


def as_list(value):
    if value in (None, "", []):
        return []
    return value if isinstance(value, list) else [value]


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def rel_prefix(page: str) -> str:
    if page == "index":
        return ""
    if page == "nested":
        return "../../"
    return "../"


def topnav(prefix: str) -> str:
    links = []
    for label, url in NAV:
        href = url.replace("/airdrie-karto-client-portal/", prefix)
        if href == "":
            href = "./"
        links.append(f'<a href="{href}">{esc(label)}</a>')
    return '<nav class="topnav"><div class="topnav-inner">' + "".join(links) + "</div></nav>"


def layout(page: str, title: str, body: str, extra_script: str = "", body_class: str = "") -> str:
    prefix = rel_prefix(page)
    body_attr = f' class="{esc(body_class)}"' if body_class else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} - City of Airdrie Karto</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='4' fill='%230B1F33'/%3E%3Ccircle cx='11' cy='11' r='5' fill='%234FD1C5'/%3E%3Ccircle cx='21' cy='11' r='5' fill='%230FB9B1'/%3E%3Ccircle cx='11' cy='21' r='5' fill='%230FB9B1'/%3E%3Ccircle cx='21' cy='21' r='5' fill='%234FD1C5'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet">
<link rel="stylesheet" href="{prefix}portal-assets/portal.css">
</head>
<body{body_attr}>
{topnav(prefix)}
<main class="shell">
{body}
</main>
{extra_script}
</body>
</html>
"""


def report_layout(page: str, title: str, body: str) -> str:
    prefix = rel_prefix(page)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} - City of Airdrie Karto</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='4' fill='%230B1F33'/%3E%3Ccircle cx='11' cy='11' r='5' fill='%234FD1C5'/%3E%3Ccircle cx='21' cy='11' r='5' fill='%230FB9B1'/%3E%3Ccircle cx='11' cy='21' r='5' fill='%230FB9B1'/%3E%3Ccircle cx='21' cy='21' r='5' fill='%234FD1C5'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet">
<link rel="stylesheet" href="{prefix}portal-assets/portal.css">
</head>
<body class="report-skin">
{body}
</body>
</html>
"""


def metric(num: str, label: str, note: str) -> str:
    return f"""<div class="metric"><span class="num">{esc(num)}</span><span class="label">{esc(label)}</span><p>{esc(note)}</p></div>"""


def hero(title: str, subtitle: str, panel_title: str, panel_text: str, panel_small: str = "") -> str:
    small = f'<p class="small">{esc(panel_small)}</p>' if panel_small else ""
    return f"""<section class="hero">
  <div class="hero-inner">
    <div>
      <p class="eyebrow">City of Airdrie</p>
      <h1>{esc(title)}</h1>
      <p class="hero-copy">{esc(subtitle)}</p>
      <div class="actions">
        <a class="btn primary" href="{REQUEST_PAGE}">Open Request Workflow</a>
        <a class="btn ghost" href="delivery-library/">View Delivery Library</a>
      </div>
    </div>
    <aside class="hero-panel">
      <h2>{esc(panel_title)}</h2>
      <p>{esc(panel_text)}</p>
      {small}
    </aside>
  </div>
</section>"""


def build_context():
    tickets = read_json(DATA / "tickets.json")
    dashboards = read_json(DATA / "dashboards.json")
    insights = read_json(DATA / "insights.json")
    attachments = read_json(DATA / "attachment-metadata.json")
    ticket_rows = []
    topic_counts = Counter()
    month_counts = Counter()
    known_hours = 0.0
    known_hour_records = 0
    completed_records = 0
    completed_files = 0
    supporting_files = 0
    gmail_reconciled = 0
    for record in tickets:
        vals = values_map(record.get("values"))
        status_notes = str(vals.get("status_notes") or "")
        status_notes_l = status_notes.lower()
        if "gmail" in status_notes_l and "reconciliation" in status_notes_l:
            gmail_reconciled += 1
        topics = as_list(vals.get("ticket_topic") or "Unspecified")
        for topic in topics:
            topic_counts[str(topic).replace("_", " ")] += 1
        month = (record.get("createdAt") or "")[:7]
        if month:
            month_counts[month] += 1
        hours = vals.get("est_hrs")
        try:
            if hours not in (None, ""):
                known_hours += float(hours)
                known_hour_records += 1
        except (TypeError, ValueError):
            pass
        completed = as_list(vals.get("completed_ticket"))
        supporting = as_list(vals.get("supporting_files"))
        if completed:
            completed_records += 1
            completed_files += len(completed)
        if supporting:
            supporting_files += len(supporting)
        ticket_rows.append(
            {
                "title": vals.get("ticket_name") or "Untitled request",
                "topics": topics,
                "hours": hours,
                "created": record.get("createdAt"),
                "completed": bool(completed),
            }
        )
    return {
        "tickets": tickets,
        "dashboards": dashboards,
        "insights": insights,
        "attachments": attachments,
        "topic_counts": topic_counts,
        "month_counts": month_counts,
        "known_hours": known_hours,
        "known_hour_records": known_hour_records,
        "completed_records": completed_records,
        "completed_files": completed_files,
        "supporting_files": supporting_files,
        "gmail_reconciled": gmail_reconciled,
        "ticket_rows": ticket_rows,
    }


def topic_bars(ctx) -> str:
    rows = []
    max_count = max(ctx["topic_counts"].values() or [1])
    for topic, count in ctx["topic_counts"].most_common(10):
        width = int((count / max_count) * 100)
        rows.append(
            f"""<div class="bar-row">
  <div class="bar-label">{esc(topic)}</div>
  <div class="bar-track"><div class="bar-fill" style="width:{width}%"></div></div>
  <div class="bar-num">{count}</div>
</div>"""
        )
    return '<div class="bar-list">' + "\n".join(rows) + "</div>"


def service_plan(ctx) -> str:
    body = hero(
        "Airdrie service workspace",
        "A staff view of requests, delivered work, ticket use, dashboards, insights, and draft ideas for future analysis.",
        "How to use this",
        "Start with the delivery library if you are looking for a finished report. Use the request workflow when you need a new briefing, table, dashboard, scan, or data collection task.",
        "Protected files stay in the secure ticket records. This page only summarizes the work.",
    )
    body += f"""<section class="section">
  <div class="metric-strip">
    {metric(str(len(ctx["tickets"])), "Ticket records", f'Current request records, including {ctx["gmail_reconciled"]} reconciled from email history.')}
    {metric("10", "Monthly allowance", "Airdrie's subscription includes 10 tickets per month.")}
    {metric(str(ctx["completed_files"]), "Completed files", "Completed-file references preserved in secure ticket records.")}
    {metric(f'{int(ctx["known_hours"]):,}', "Staff hours noted", f'Summed across {ctx["known_hour_records"]} ticket records with hour estimates.')}
  </div>
</section>
<section class="section">
  <div class="section-head">
    <div><p class="section-label">Request pattern</p><h2>What Airdrie has been asking for</h2></div>
    <p class="lede">The current record clusters around housing, downtown revitalization, engagement, data analysis, homelessness strategy, land use, mixed-use development, and economic diversification.</p>
  </div>
  <div class="split">
    <div class="panel">
      <h3>Ticket themes</h3>
      {topic_bars(ctx)}
    </div>
    <div class="panel dark">
      <h3>What this suggests</h3>
      <ul>
        <li>Housing and growth management are the core account themes, not one-off reports.</li>
        <li>Downtown, parking, STRs, and HAF compliance should be treated as a connected work program.</li>
        <li>Airdrie has enough prior ticket volume to keep intake, delivery, and reference materials organized in one place.</li>
        <li>Some repeat questions would benefit from structured data collection before the next analysis starts.</li>
      </ul>
    </div>
  </div>
</section>
<section class="section">
  <div class="section-head">
    <div><p class="section-label">Next action</p><h2>Recommended workspace flow</h2></div>
  </div>
  <div class="grid four">
    <a class="card" href="delivery-library/"><p class="kicker">1</p><h3>Read shipped work</h3><p>Start with the polished web reports and the protected Karto attachment archive.</p><div class="tags"><span class="tag">Reports</span><span class="tag">Word/PDF files</span></div></a>
    <a class="card" href="subscription/"><p class="kicker">2</p><h3>Check ticket use</h3><p>Review the 10-ticket monthly allowance, completed files, and staff-hour estimates.</p><div class="tags"><span class="tag">10/month</span><span class="tag">Use</span></div></a>
    <a class="card" href="next-requests/"><p class="kicker">3</p><h3>Review draft ideas</h3><p>Use the idea list as starting scope when a department needs another analysis request.</p><div class="tags"><span class="tag">Ideas</span><span class="tag">Scope</span></div></a>
    <a class="card" href="{REQUEST_PAGE}"><p class="kicker">4</p><h3>Submit a request</h3><p>Fill out the request form with the question, deadline, intended use, and files to attach.</p><div class="tags"><span class="tag">Intake</span><span class="tag">Tracking</span></div></a>
  </div>
</section>
<p class="source-note">Selected public context links: <a href="https://www.cmhc-schl.gc.ca/media-newsroom/news-releases/2024/helping-build-more-homes-faster-airdrie" target="_blank" rel="noopener">CMHC Airdrie HAF announcement</a>; <a href="https://assets.cmhc-schl.gc.ca/sites/cmhc/professional/project-funding-and-mortgage-financing/funding-programs/all-funding-programs/housing-accelerator-fund/action-plan-summaries/haf-action-plan-summary-airdrie-en.pdf" target="_blank" rel="noopener">CMHC action plan summary</a>; <a href="https://www.airdrie.ca/index.cfm?serviceID=2578" target="_blank" rel="noopener">Airdrie four-homes-per-lot consultation page</a>.</p>
"""
    return layout("index", "Service Plan", body, calculator_script())


def delivery_library(ctx) -> str:
    report_rows = "\n".join(
        f"<tr><td><strong>{esc(item['title'])}</strong></td><td>{esc(item['area'])}</td><td>{esc(item['status'])}</td><td><a class=\"btn light\" href=\"{esc(item['url'])}\" target=\"_blank\" rel=\"noopener\">Open</a></td></tr>"
        for item in PUBLIC_DELIVERABLES
    )
    body = f"""<section class="hero">
  <div class="hero-inner">
    <div><p class="eyebrow">Delivery Library</p><h1>All polished outputs in one place</h1><p class="hero-copy">Airdrie's older attachments stay in protected Karto records. Web reports and dashboards are surfaced here as a clean reading library.</p></div>
    <aside class="hero-panel"><h2>{ctx["completed_files"]} completed files preserved</h2><p>{ctx["supporting_files"]} supporting-file references are also still attached to ticket records. Use the protected archive button for authenticated downloads.</p><a class="btn primary" href="{TICKET_LIST_PAGE}" target="_blank" rel="noopener">Open Protected Archive</a></aside>
  </div>
</section>
<section class="section">
  <div class="section-head"><div><p class="section-label">Web reports</p><h2>Client-readable deliverables</h2></div><p class="lede">These are the web-published outputs already represented in Airdrie's Karto namespace or Airdrie ticket history.</p></div>
  <div class="table-panel"><table class="matrix"><thead><tr><th>Deliverable</th><th>Business area</th><th>Format</th><th>Action</th></tr></thead><tbody>{report_rows}</tbody></table></div>
</section>
<section class="section">
  <div class="notice"><strong>Attachment handling:</strong> This page does not mirror protected Word/PDF filenames into the public static layer. The Karto ticket archive remains the source of truth for attachment downloads, permissions, and auditability.</div>
</section>
"""
    return layout("sub", "Delivery Library", body)


def request_workflow(ctx) -> str:
    topic_options = [
        ("Housing Affordability", "Housing_Affordability"),
        ("Community Engagement", "Community_Engagement"),
        ("Data Analysis", "Data_Analysis"),
        ("Downtown Revitalization", "Downtown Revitalization"),
        ("Parking Policy", "Parking_Policy"),
        ("Land Use Designation", "Land_Use_Designation"),
        ("Residential Density", "Residential_Density"),
        ("Homelessness Strategy", "Homelessness_Strategy"),
        ("Economic Diversification", "Economic_Diversification"),
        ("Servicing Costs", "Servicing_Costs"),
        ("Water Management", "Water_Management"),
        ("Intermunicipal Collaboration", "Intermunicipal_Collaboration"),
        ("Public Transit", "Public_Transit"),
        ("Other", "Other"),
    ]
    output_options = [
        ("Briefing note / Word", "docx"),
        ("Spreadsheet / Excel", "excel"),
        ("Web report", "website"),
        ("Dashboard", "google_sheet"),
        ("Slide deck", "ppt"),
        ("PDF", "pdf"),
        ("Data collection form", "google_form"),
        ("Other", "other"),
    ]
    topics = "\n".join(
        f'<label class="check-tile"><input type="checkbox" name="ticket_topic" value="{esc(value)}"><span>{esc(label)}</span></label>'
        for label, value in topic_options
    )
    outputs = "\n".join(
        f'<label class="check-tile"><input type="checkbox" name="output_format" value="{esc(value)}"><span>{esc(label)}</span></label>'
        for label, value in output_options
    )
    body = f"""<section class="hero">
  <div class="hero-inner">
    <div><p class="eyebrow">Request Workflow</p><h1>Submit a new request</h1><p class="hero-copy">Use this form when you need a briefing note, analysis, dashboard, table, scan, or data collection task. A clear decision question and useful source files help the work move faster.</p></div>
    <aside class="hero-panel"><h2>What happens next</h2><p>Your request is saved to the Airdrie ticket workspace for review and tracking. If confidential files are needed, add them to the secure ticket record after submission.</p><p class="small">You must be signed into Karto before submitting.</p></aside>
  </div>
</section>
<section class="section">
  <form class="intake-form" id="ticket-intake" data-endpoint="{REQUEST_API_ENDPOINT}" novalidate>
    <div class="form-head">
      <div><p class="section-label">New request</p><h2>Tell us what decision this should support</h2></div>
      <p class="lede">Short, specific requests move fastest. Files can be attached after the ticket is created, using the protected ticket record.</p>
    </div>
    <div class="form-grid two">
      <label class="field wide">Ticket title
        <input name="ticket_name" required maxlength="180" placeholder="Example: HAF milestone and amendment risk tracker">
      </label>
      <label class="field">Your name
        <input name="submitter_name" autocomplete="name" placeholder="Name">
      </label>
      <label class="field">Your email
        <input name="submitter_email" type="email" autocomplete="email" placeholder="name@airdrie.ca">
      </label>
      <label class="field">Requested completion date
        <input name="required_completion_date" type="date">
      </label>
      <label class="field">Urgency
        <select name="urgency">
          <option value="medium">Medium</option>
          <option value="low">Low</option>
          <option value="high">High</option>
        </select>
      </label>
      <label class="field wide">Geographic scope
        <input name="geographic_scope" placeholder="City of Airdrie, Calgary region, Alberta comparators, etc.">
      </label>
      <label class="field wide">Objective
        <input name="objective" placeholder="What decision, meeting, policy, or operational question should this support?">
      </label>
      <label class="field wide">Request details
        <textarea name="description_plain" required rows="7" placeholder="Describe the question, audience, expected use, known context, and any constraints."></textarea>
      </label>
      <label class="field wide">Source files or links to add after submission
        <textarea name="source_notes" rows="4" placeholder="List file names, SharePoint links, council reports, spreadsheets, prior work, or people to contact."></textarea>
      </label>
    </div>
    <div class="form-section">
      <h3>Topics</h3>
      <div class="choice-grid">{topics}</div>
    </div>
    <div class="form-section">
      <h3>Expected output</h3>
      <div class="choice-grid">{outputs}</div>
    </div>
    <div class="form-grid three compact">
      <label class="field">Estimated staff hours saved
        <input name="est_hrs" type="number" min="0" max="100" step="1" placeholder="12">
      </label>
      <label class="field">Expected content volume
        <input name="content_volume" type="number" min="0" max="100" step="1" placeholder="10">
      </label>
      <label class="field">Privacy
        <select name="private_ticket">
          <option value="0">Share with Airdrie team</option>
          <option value="1">Private to requester</option>
        </select>
      </label>
      <label class="check-line"><input type="checkbox" name="brand" value="1" checked><span>Use City of Airdrie branding where possible</span></label>
    </div>
    <div class="form-actions">
      <button class="btn primary" type="submit">Submit ticket</button>
      <button class="btn light" type="reset">Clear</button>
      <span class="form-status" id="ticket-status" role="status" aria-live="polite"></span>
    </div>
    <div class="notice compact-note">This form creates the request record. Attach confidential files only in the secure ticket record or through an approved file-transfer channel.</div>
  </form>
</section>
<section class="section">
  <div class="grid three">
    <div class="card"><p class="kicker">1</p><h3>Submit the request</h3><p>Include the question, audience, deadline, expected output, and any context staff should know.</p></div>
    <div class="card"><p class="kicker">2</p><h3>Review and confirm</h3><p>The request is recorded for follow-up, assignment, and status tracking.</p></div>
    <div class="card"><p class="kicker">3</p><h3>Add files securely</h3><p>Reports, spreadsheets, agendas, or examples should be attached through the secure ticket record.</p></div>
  </div>
</section>
"""
    return layout("sub", "Request Workflow", body, '<script src="../portal-assets/request-intake.js"></script>')


def subscription(ctx) -> str:
    body = f"""<section class="hero">
  <div class="hero-inner">
    <div><p class="eyebrow">Ticket Allowance</p><h1>10 tickets per month and current use</h1><p class="hero-copy">A simple account view for staff: how many request records exist, how many have completed files, and what staff-hour estimates have been captured.</p></div>
    <aside class="hero-panel"><h2>Monthly subscription</h2><p>Airdrie's current subscription includes 10 tickets per month. This page summarizes current ticket records and related planning estimates.</p></aside>
  </div>
</section>
<section class="section">
  <div class="metric-strip">
    {metric("10/month", "Ticket allowance", "Airdrie's monthly subscription allowance.")}
    {metric(str(len(ctx["tickets"])), "Request records", f'All Airdrie ticket records, including {ctx["gmail_reconciled"]} reconciled from email history.')}
    {metric(str(ctx["completed_records"]), "With completed files", "Request records with completed-file attachments.")}
    {metric(f'{int(ctx["known_hours"]):,}', "Staff hours noted", "Current sum from ticket records with est_hrs values.")}
  </div>
</section>
<section class="section">
  {hours_calculator(ctx)}
</section>
<section class="section">
  <div class="notice">The calculator is intentionally editable. Replace the default loaded hourly rate with Airdrie's internal fully burdened analyst/planner rate for a local estimate.</div>
</section>
"""
    return layout("sub", "Ticket Allowance", body, calculator_script())


def hours_calculator(ctx) -> str:
    return f"""<div class="calc" id="hours-calculator" data-hours="{ctx["known_hours"]}" data-tickets="{len(ctx["tickets"])}">
  <h3>Staff-time planning calculator</h3>
  <p>Uses the cumulative hour estimates stored in ticket records. Staff can adjust the hourly cost and reuse factor when they need a rough planning estimate for internal reporting.</p>
  <div class="calc-controls">
    <label>Total estimated hours<input id="calc-hours" type="number" min="0" step="1" value="{int(ctx["known_hours"])}"></label>
    <label>Loaded staff cost/hour<input id="calc-rate" type="number" min="0" step="5" value="70"></label>
    <label>Reuse factor<input id="calc-reuse" type="number" min="1" step="0.25" value="1"></label>
  </div>
  <div class="calc-output">
    <div class="calc-stat"><strong id="out-hours">0</strong><span>Equivalent hours</span></div>
    <div class="calc-stat"><strong id="out-value">$0</strong><span>Planning estimate</span></div>
    <div class="calc-stat"><strong id="out-per-ticket">$0</strong><span>Estimate per ticket</span></div>
  </div>
</div>"""


def calculator_script() -> str:
    return """<script>
function updateCalculator(){
  const hours = Number(document.getElementById('calc-hours')?.value || 0);
  const rate = Number(document.getElementById('calc-rate')?.value || 0);
  const reuse = Number(document.getElementById('calc-reuse')?.value || 1);
  const tickets = Number(document.getElementById('hours-calculator')?.dataset.tickets || 1);
  const equivalent = hours * reuse;
  const value = equivalent * rate;
  const perTicket = tickets ? value / tickets : 0;
  const money = new Intl.NumberFormat('en-CA', {style:'currency', currency:'CAD', maximumFractionDigits:0});
  const num = new Intl.NumberFormat('en-CA', {maximumFractionDigits:0});
  const oh = document.getElementById('out-hours');
  const ov = document.getElementById('out-value');
  const opt = document.getElementById('out-per-ticket');
  if (oh) oh.textContent = num.format(equivalent);
  if (ov) ov.textContent = money.format(value);
  if (opt) opt.textContent = money.format(perTicket);
}
document.addEventListener('input', updateCalculator);
document.addEventListener('DOMContentLoaded', updateCalculator);
</script>"""


def insights_page(ctx) -> str:
    insight_cards = [
        ("Housing pressure", "Repeated signals around housing affordability, HAF commitments, mixed-income family housing, and core housing need."),
        ("Regional spillover", "Records connect Airdrie's growth, commuting, Calgary-region displacement, and neighbouring municipality underbuilding."),
        ("Service planning", "Dashboard insights point to child density, poverty, gendered income vulnerability, schools, recreation, and family services."),
        ("Downtown and land use", "Tickets cluster around parking, brownfield redevelopment, mixed-use development, and strategic downtown opportunities."),
        ("Engagement", "Several ticket themes require council, ELT, public consultation, and resident-facing explanation products."),
        ("Data gaps", "Existing research repeatedly asks for local baselines before policy calibration: complaints, STR listings, suite inventory, and parking saturation."),
    ]
    cards = "\n".join(
        f'<div class="card"><p class="kicker">Insight area</p><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in insight_cards
    )
    body = f"""<section class="hero">
  <div class="hero-inner">
    <div><p class="eyebrow">Insights</p><h1>Common findings across the Airdrie work program</h1><p class="hero-copy">This view turns ticket history and dashboard records into a practical account map: what Airdrie keeps asking about, where evidence is accumulating, and where better data collection would unlock stronger recommendations.</p></div>
    <aside class="hero-panel"><h2>{len(ctx["insights"])} insight records</h2><p>Insight records remain in Karto for auditability. The polished page groups them into staff-readable themes.</p><a class="btn primary" href="{INSIGHT_LIST_PAGE}" target="_blank" rel="noopener">Open Insight Records</a></aside>
  </div>
</section>
<section class="section"><div class="grid two">{cards}</div></section>
"""
    return layout("sub", "Insights", body)


def dashboard_gallery_page(ctx) -> str:
    def dashboard_values(record):
        vals = values_map(record.get("values"))
        return {
            "name": vals.get("dashboard_name") or "Untitled dashboard",
            "description": vals.get("description") or "Airdrie dashboard record",
            "url": vals.get("embed_url") or DASHBOARD_LIST_PAGE,
            "source": vals.get("data_source") or "Karto dashboard record",
        }

    rows = []
    for record in ctx["dashboards"]:
        item = dashboard_values(record)
        rows.append(
            f"<tr><td><strong>{esc(item['name'])}</strong></td><td>{esc(item['description'])}</td><td>{esc(item['source'])}</td><td><a class=\"btn light\" href=\"{esc(item['url'])}\" target=\"_blank\" rel=\"noopener\">Open</a></td></tr>"
        )
    body = f"""<section class="hero">
  <div class="hero-inner">
    <div><p class="eyebrow">Dashboard Gallery</p><h1>Reusable views for Airdrie planning and service questions</h1><p class="hero-copy">The namespace contains Tableau-backed dashboard records. This page makes them easier to find without exposing the raw dashboard module as a left-rail admin page.</p></div>
    <aside class="hero-panel"><h2>{len(ctx["dashboards"])} dashboard records</h2><p>Use this gallery for client navigation. Use the protected Karto records when staff need to edit embeds, filters, or metadata.</p><a class="btn primary" href="{DASHBOARD_LIST_PAGE}" target="_blank" rel="noopener">Open Dashboard Records</a></aside>
  </div>
</section>
<section class="section">
  <div class="table-panel"><table class="matrix"><thead><tr><th>Dashboard</th><th>Description</th><th>Source</th><th>Action</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
</section>
"""
    return layout("sub", "Dashboard Gallery", body)


def data_collection_page(ctx) -> str:
    rows = [
        ("Secondary suite registry", "Suite location, permit status, occupancy/use, parking context, complaints, inspection milestones", "Supports suite policy and HAF risk analysis."),
        ("STR licensing and complaints", "Host type, principal-residence evidence, nights rented, complaints, enforcement actions", "Supports STR bylaw design without guessing at local impacts."),
        ("Affordable housing grant reporting", "Recipient milestones, units, dollars, completion evidence, barriers, narrative updates", "Reduces manual grant follow-up and improves reporting quality."),
        ("Engagement synthesis", "Survey responses, themes, stakeholder type, geography, sentiment, action requested", "Turns consultation into structured evidence for council reports."),
        ("Regional housing indicators", "Airdrie plus Calgary-region peers: affordability, commute, supply, service pressure, labour force", "Creates a reusable regional benchmark for future tickets."),
    ]
    table = "\n".join(f"<tr><td><strong>{esc(a)}</strong></td><td>{esc(b)}</td><td>{esc(c)}</td></tr>" for a, b, c in rows)
    body = f"""<section class="hero">
  <div class="hero-inner">
    <div><p class="eyebrow">Data Collection Options</p><h1>Make future tickets easier by collecting the missing evidence once</h1><p class="hero-copy">The next layer is not another static report. It is repeatable intake, tracking, and reporting workflows that feed future Karto analysis with Airdrie-specific evidence.</p></div>
    <aside class="hero-panel"><h2>Structured collection</h2><p>Use structured forms and workflows where the City needs recurring data from staff, partners, recipients, or residents. The resulting evidence can feed future analysis.</p></aside>
  </div>
</section>
<section class="section">
  <div class="table-panel"><table class="matrix"><thead><tr><th>Workflow</th><th>Data captured</th><th>Why it matters</th></tr></thead><tbody>{table}</tbody></table></div>
</section>
<section class="section">
  <div class="notice"><strong>Purpose:</strong> These options are for recurring information needs where one structured collection process would make future requests easier and more defensible.</div>
</section>
"""
    return layout("sub", "Data Collection", body)


def next_requests_page(ctx) -> str:
    cards = "\n".join(
        f"""<div class="card">
  <p class="kicker">{esc(item["theme"])} - approx. {item["hours"]} hrs</p>
  <h3>{esc(item["name"])}</h3>
  <p><strong>Why now:</strong> {esc(item["why"])}</p>
  <p><strong>Output:</strong> {esc(item["output"])}</p>
  <div class="tags"><span class="tag">Suggested ticket</span><span class="tag">{esc(item["theme"])}</span></div>
</div>"""
        for item in NEXT_REQUESTS
    )
    body = f"""<section class="hero">
  <div class="hero-inner">
    <div><p class="eyebrow">Next Requests</p><h1>Draft request ideas based on Airdrie's current work</h1><p class="hero-copy">These are starting points for staff when a department needs another briefing, dashboard, table, scan, or structured data collection task.</p><div class="actions"><a class="btn primary" href="{REQUEST_PAGE}">Start a request</a></div></div>
    <aside class="hero-panel"><h2>How to use this</h2><p>Pick one card, adjust the scope for your department, and attach any current council package or staff report that should anchor the work.</p></aside>
  </div>
</section>
<section class="section"><div class="grid two">{cards}</div></section>
"""
    return layout("sub", "Next Requests", body)


def housing_labour_page(ctx) -> str:
    body = f"""<section class="hero">
  <div class="hero-inner">
    <div><p class="eyebrow">Housing and Labour</p><h1>Housing pressure is also a workforce and service-delivery issue</h1><p class="hero-copy">Airdrie's records repeatedly connect housing affordability, commuting, labour force pressure, and regional growth spillover. This page gives the empty Housing-Labour Nexus page a client-readable destination.</p></div>
    <aside class="hero-panel"><h2>Protected source file</h2><p>The completed research report remains attached to its Karto ticket record. Open the protected archive to download the original Word document.</p><a class="btn primary" href="{TICKET_LIST_PAGE}" target="_blank" rel="noopener">Open Protected Archive</a></aside>
  </div>
</section>
<section class="section">
  <div class="grid three">
    <div class="card"><p class="kicker">Pattern</p><h3>Growth pressure</h3><p>Population growth, family household distribution, and regional spillover affect housing demand and municipal service planning together.</p></div>
    <div class="card"><p class="kicker">Pattern</p><h3>Commuting pressure</h3><p>Commuting and labour-market geography should be part of Airdrie's housing evidence base, especially for regional comparisons.</p></div>
    <div class="card"><p class="kicker">Pattern</p><h3>Data need</h3><p>Future decisions need a repeatable dashboard that connects housing, labour force, income, commute, and service-access indicators.</p></div>
  </div>
</section>
"""
    return layout("sub", "Housing Labour", body)


def external_report_page(report: dict[str, str]) -> str:
    body = f"""<section class="hero">
  <div class="hero-inner">
    <div><p class="eyebrow">{esc(report["eyebrow"])}</p><h1>{esc(report["headline"])}</h1><p class="hero-copy">{esc(report["copy"])}</p><div class="actions"><a class="btn primary" href="{esc(report["source_url"])}" target="_blank" rel="noopener">{esc(report["source_label"])}</a><a class="btn ghost" href="../delivery-library/">Back to Delivery Library</a></div></div>
    <aside class="hero-panel"><h2>{esc(report["panel_title"])}</h2><p>{esc(report["panel_text"])}</p><p class="small">Protected source records and attachments remain in Karto.</p></aside>
  </div>
</section>
<section class="section">
  <div class="report-frame"><iframe title="{esc(report["title"])}" src="{esc(report["source_url"])}" loading="lazy"></iframe></div>
</section>
"""
    return layout("sub", report["title"], body)


def ticket_archive_page() -> str:
    body = f"""<section class="hero">
  <div class="hero-inner">
    <div><p class="eyebrow">Ticket Archive</p><h1>Protected Airdrie ticket archive</h1><p class="hero-copy">Use this page when staff need the secure record list rather than the public delivery library. Attachments, private notes, and audit history stay inside Karto.</p><div class="actions"><a class="btn primary" href="{TICKET_LIST_PAGE}" target="_blank" rel="noopener">Open Protected Archive</a><a class="btn ghost" href="../delivery-library/">View Delivery Library</a></div></div>
    <aside class="hero-panel"><h2>Secure source of truth</h2><p>The delivery library summarizes client-readable outputs. The ticket archive is the authenticated workspace for records, private files, and internal status tracking.</p><p class="small">You must be signed into Karto to open protected records.</p></aside>
  </div>
</section>
<section class="section">
  <div class="grid three">
    <div class="card"><p class="kicker">Records</p><h3>Ticket history</h3><p>Review request status, scope, owners, estimates, and completion context in the protected Karto module.</p></div>
    <div class="card"><p class="kicker">Files</p><h3>Protected attachments</h3><p>Use Karto records for Word, PDF, spreadsheets, and source files that should not be mirrored into the public static layer.</p></div>
    <div class="card"><p class="kicker">Audit</p><h3>Workspace trail</h3><p>Keep changes, follow-up, and private handling inside the authenticated archive rather than a public page.</p></div>
  </div>
</section>
"""
    return layout("sub", "Ticket Archive", body)


def str_portal_page() -> str:
    cards = "\n".join(
        f"""<a class="tier" href="{esc(item["href"])}">
  <div class="tier-badge">{esc(item["eyebrow"])}<span class="tier-icon material-symbols-outlined">{esc(item["icon"])}</span></div>
  <div class="tier-body">
    <h3>{esc(item["title"])}</h3>
    <div class="audience">{esc(item["audience"])}</div>
    <p>{esc(item["description"])}</p>
  </div>
  <div class="tier-arrow"><span class="material-symbols-outlined">arrow_forward</span></div>
</a>"""
        for item in STR_DOC_LINKS
        if item["href"] != "interactive-briefing/"
    )
    interactive = next(item for item in STR_DOC_LINKS if item["href"] == "interactive-briefing/")
    body = f"""<header class="hero">
  <div class="hero-inner">
    <div class="eyebrow">City of Airdrie · Jurisdictional Scan</div>
    <h1>Secondary Suite Density &amp; Short-Term Rental Controls</h1>
    <p class="lede">Comparative scan across 20 Canadian municipalities of the regulatory levers Airdrie council can use to manage neighbourhood-scale residential intensification within the binding constraints of the federal Housing Accelerator Fund agreement and Alberta's legislative landscape.</p>
    <div class="meta">
      <div><strong>Client</strong>City of Airdrie, Alberta</div>
      <div><strong>Prepared</strong>May 2026 · Consultation close May 25, 2026</div>
      <div><strong>Scope</strong>Secondary suites, density caps, STR licensing, HAF compliance</div>
    </div>
  </div>
</header>
<main>
  <section class="intro">
    <div class="intro-eyebrow">Choose your view</div>
    <h2>Five documents. One evidence base.</h2>
    <p>The technical report is the source of truth. The decision-support brief, council, ELT, and planner briefings are derived from it for different audiences. The interactive briefing bundles all views into a single navigable artifact.</p>
  </section>
  <div class="tiers">{cards}</div>
  <a class="featured-card" href="{esc(interactive["href"])}">
    <div>
      <div class="featured-eyebrow">{esc(interactive["eyebrow"])}</div>
      <h3>{esc(interactive["title"])}</h3>
      <p>{esc(interactive["description"])}</p>
    </div>
    <div class="featured-icon"><span class="material-symbols-outlined">{esc(interactive["icon"])}</span></div>
  </a>
  <details class="note">
    <summary style="display:flex;justify-content:space-between;align-items:center;cursor:pointer;list-style:none">
      <h4 style="margin:0;font-size:18px;font-weight:700;color:var(--deep-navy)">Reading order</h4>
      <span style="width:26px;height:26px;border:1px solid rgba(15,185,177,0.4);border-radius:var(--r-sm);color:var(--deep-teal);font-weight:700;font-size:16px;display:flex;align-items:center;justify-content:center;flex-shrink:0" class="note-toggle"></span>
    </summary>
    <div style="margin-top:14px">
      <p>For council members preparing for the Community Infrastructure &amp; Strategic Growth Standing Committee meeting, start with the <strong>Decision-Support Brief</strong>. For planning staff drafting bylaw language, start with the <strong>Planner Briefing</strong> and reference the Technical Report for in-force peer-jurisdiction parameters. The <strong>Branded Policy Briefing</strong> bundles council, executive, and research views in a single interactive artifact.</p>
    </div>
  </details>
  <details class="note" style="margin-top:20px">
    <summary style="display:flex;justify-content:space-between;align-items:center;cursor:pointer;list-style:none">
      <h4 style="margin:0;font-size:18px;font-weight:700;color:var(--deep-navy)">Source posture</h4>
      <span style="width:26px;height:26px;border:1px solid rgba(15,185,177,0.4);border-radius:var(--r-sm);color:var(--deep-teal);font-weight:700;font-size:16px;display:flex;align-items:center;justify-content:center;flex-shrink:0" class="note-toggle"></span>
    </summary>
    <div style="margin-top:14px">
      <p>Displayed statistics are drawn from the technical report and linked public records. Load-bearing public links include the CMHC Airdrie HAF announcement, CMHC Airdrie Action Plan Summary, CMHC Red Deer HAF update, Alberta Provincial Priorities Act municipal guidance, and the Toronto Auditor General STR audit. APA 7 references are embedded in the technical report and interactive briefing evidence record.</p>
      <p>This analysis is for informational purposes. Verify in-force bylaw text, HAF disbursement status, and named staff before client-facing publication.</p>
    </div>
  </details>
</main>
<footer>
  <div class="footer-inner">
    <div>
      <strong>HelpSeeker Technologies</strong>
      Secondary Suite Density &amp; Short-Term Rental Controls · City of Airdrie · Prepared by HelpSeeker Technologies / Karto Research. Jurisdictional scan across 20 Canadian municipalities covering density rules, STR licensing, HAF compliance, and provincial legislative constraints.
    </div>
    <div>v1.0 · 2026-05-11</div>
  </div>
</footer>
"""
    return report_layout("sub", "Secondary Suites & STR", body)


def write_page(path: Path, html_text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_text, encoding="utf-8")


def main() -> int:
    ctx = build_context()
    write_page(ROOT / "index.html", service_plan(ctx))
    write_page(ROOT / "delivery-library" / "index.html", delivery_library(ctx))
    write_page(ROOT / "request-workflow" / "index.html", request_workflow(ctx))
    write_page(ROOT / "subscription" / "index.html", subscription(ctx))
    write_page(ROOT / "dashboard-gallery" / "index.html", dashboard_gallery_page(ctx))
    write_page(ROOT / "insights" / "index.html", insights_page(ctx))
    write_page(ROOT / "data-collection" / "index.html", data_collection_page(ctx))
    write_page(ROOT / "next-requests" / "index.html", next_requests_page(ctx))
    write_page(ROOT / "housing-labour" / "index.html", housing_labour_page(ctx))
    for report in EXTERNAL_REPORTS:
        if report["folder"] == "secondary-suites-str":
            write_page(ROOT / report["folder"] / "index.html", str_portal_page())
        else:
            write_page(ROOT / report["folder"] / "index.html", external_report_page(report))
    write_page(ROOT / "ticket-archive" / "index.html", ticket_archive_page())
    manifest = {
        "ticket_records": len(ctx["tickets"]),
        "dashboard_records": len(ctx["dashboards"]),
        "insight_records": len(ctx["insights"]),
        "completed_file_refs": ctx["completed_files"],
        "supporting_file_refs": ctx["supporting_files"],
        "gmail_reconciled_ticket_records": ctx["gmail_reconciled"],
        "known_estimated_hours": ctx["known_hours"],
        "public_attachment_filenames_mirrored": False,
        "protected_download_source": TICKET_LIST_PAGE,
    }
    (ROOT / "build-manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
