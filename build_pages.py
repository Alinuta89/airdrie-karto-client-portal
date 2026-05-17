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
REQUEST_PAGE = f"{KARTO_NS_URL}/pages/437118446045495297"
TICKET_LIST_PAGE = f"{KARTO_NS_URL}/pages/437118446039072769"
DASHBOARD_LIST_PAGE = f"{KARTO_NS_URL}/pages/437118446032453633"
INSIGHT_LIST_PAGE = f"{KARTO_NS_URL}/pages/437535446718873601"


NAV = [
    ("Service Plan", "/airdrie-karto-client-portal/"),
    ("Delivery Library", "/airdrie-karto-client-portal/delivery-library/"),
    ("Request Workflow", "/airdrie-karto-client-portal/request-workflow/"),
    ("Subscription", "/airdrie-karto-client-portal/subscription/"),
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
        "output": "Mareto-style intake form set, quarterly reporting dashboard, and export-ready grant accountability table.",
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
    return "" if page == "index" else "../"


def topnav(prefix: str) -> str:
    links = []
    for label, url in NAV:
        href = url.replace("/airdrie-karto-client-portal/", prefix)
        if href == "":
            href = "./"
        links.append(f'<a href="{href}">{esc(label)}</a>')
    return '<nav class="topnav"><div class="topnav-inner">' + "".join(links) + "</div></nav>"


def layout(page: str, title: str, body: str, extra_script: str = "") -> str:
    prefix = rel_prefix(page)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} - City of Airdrie Karto</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='4' fill='%230B1F33'/%3E%3Ccircle cx='11' cy='11' r='5' fill='%234FD1C5'/%3E%3Ccircle cx='21' cy='11' r='5' fill='%230FB9B1'/%3E%3Ccircle cx='11' cy='21' r='5' fill='%230FB9B1'/%3E%3Ccircle cx='21' cy='21' r='5' fill='%234FD1C5'/%3E%3C/svg%3E">
<link rel="stylesheet" href="{prefix}portal-assets/portal.css">
</head>
<body>
{topnav(prefix)}
<main class="shell">
{body}
</main>
{extra_script}
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
        <a class="btn primary" href="{REQUEST_PAGE}" target="_blank" rel="noopener">Open Request Workflow</a>
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
    for record in tickets:
        vals = values_map(record.get("values"))
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
        "Airdrie service plan workspace",
        "A client-facing operating view of Airdrie's Karto work: what has shipped, what is in the workflow, where the evidence base is clustering, and what should be ordered next.",
        "What changed",
        "The public-facing layer is now separated from the workflow layer. Staff can read the polished service plan first, then open the protected Karto request workflow when they need to create or manage a ticket.",
        "Protected attachments remain in Karto. This page summarizes them without mirroring confidential filenames.",
    )
    body += f"""<section class="section">
  <div class="metric-strip">
    {metric(str(len(ctx["tickets"])), "Ticket records", "Live ticket records in the City of Airdrie namespace.")}
    {metric("10", "Monthly quota", "Current ticket quota recorded for the City of Airdrie organization.")}
    {metric(str(ctx["completed_files"]), "Completed files", "Completed-ticket attachment references preserved in Karto.")}
    {metric(f'{int(ctx["known_hours"]):,}', "Estimated hours", f'Summed across {ctx["known_hour_records"]} ticket records with hour estimates.')}
  </div>
</section>
<section class="section">
  <div class="section-head">
    <div><p class="section-label">Demand pattern</p><h2>Where Airdrie is already using Karto</h2></div>
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
        <li>Airdrie has enough prior ticket volume to justify a better request workflow and a real delivery library.</li>
        <li>Mareto-style data collection should support repeatable evidence gathering, not sit as a separate product pitch.</li>
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
    <a class="card" href="subscription/"><p class="kicker">2</p><h3>Check ticket use</h3><p>Review quota, cumulative hours, file volume, and likely internal capacity saved.</p><div class="tags"><span class="tag">Quota</span><span class="tag">Hours saved</span></div></a>
    <a class="card" href="next-requests/"><p class="kicker">3</p><h3>Pick the next request</h3><p>Use the recommended ticket list to convert known pressure points into scoped work.</p><div class="tags"><span class="tag">Pipeline</span><span class="tag">Council-ready</span></div></a>
    <a class="card" href="{REQUEST_PAGE}" target="_blank" rel="noopener"><p class="kicker">4</p><h3>Submit in Karto</h3><p>Open the native request workflow so the existing notifications and record tracking remain intact.</p><div class="tags"><span class="tag">Workflow</span><span class="tag">Notifications</span></div></a>
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
    body = f"""<section class="hero">
  <div class="hero-inner">
    <div><p class="eyebrow">Request Workflow</p><h1>Submit and track work through Karto</h1><p class="hero-copy">Airdrie already has enabled notification workflows. The clean page should route staff into the native Karto ticket form instead of replacing the workflow logic.</p><div class="actions"><a class="btn primary" href="{REQUEST_PAGE}" target="_blank" rel="noopener">Open Request Workflow</a><a class="btn ghost" href="{TICKET_LIST_PAGE}" target="_blank" rel="noopener">Open Ticket Records</a></div></div>
    <aside class="hero-panel"><h2>Workflow preserved</h2><p>Two enabled workflow definitions exist in the namespace. They should remain attached to the record workflow so new submissions and status updates continue to notify the right people.</p></aside>
  </div>
</section>
<section class="section">
  <div class="grid three">
    <div class="card"><p class="kicker">Before submitting</p><h3>Frame the question</h3><p>Use a decision question, not just a topic. Good requests ask what council, ELT, or staff need to decide next.</p><div class="tags"><span class="tag">Decision</span><span class="tag">Audience</span></div></div>
    <div class="card"><p class="kicker">Attach context</p><h3>Add source files</h3><p>Upload reports, agendas, spreadsheets, presentations, or examples directly into the protected Karto workflow.</p><div class="tags"><span class="tag">Files</span><span class="tag">Evidence</span></div></div>
    <div class="card"><p class="kicker">Pick output</p><h3>Name the usable artifact</h3><p>Briefing note, technical report, dashboard, comparator table, council summary, presentation, or data collection form.</p><div class="tags"><span class="tag">Format</span><span class="tag">Deadline</span></div></div>
  </div>
</section>
"""
    return layout("sub", "Request Workflow", body)


def subscription(ctx) -> str:
    body = f"""<section class="hero">
  <div class="hero-inner">
    <div><p class="eyebrow">Subscription and Capacity</p><h1>Ticket use, quota, and estimated staff time saved</h1><p class="hero-copy">A lightweight account view for CAOs and staff: how much work has flowed through Karto, where it clusters, and what internal capacity the service is replacing.</p></div>
    <aside class="hero-panel"><h2>Pay-as-you-go signal</h2><p>The current organization record shows a monthly quota of 10 tickets. This page uses live-record totals captured from the Airdrie namespace snapshot.</p></aside>
  </div>
</section>
<section class="section">
  <div class="metric-strip">
    {metric(str(len(ctx["tickets"])), "Ticket records", "All Airdrie ticket records in the namespace.")}
    {metric(str(ctx["completed_records"]), "Tickets with files", "Ticket records with completed-ticket attachments.")}
    {metric(f'{int(ctx["known_hours"]):,}', "Estimated hours", "Current sum from ticket records with est_hrs values.")}
    {metric("$80.5K", "Default value", "Using the editable $70/hour loaded staff-cost assumption below.")}
  </div>
</section>
<section class="section">
  {hours_calculator(ctx)}
</section>
<section class="section">
  <div class="notice">The calculator is intentionally editable. Replace the default loaded hourly rate with Airdrie's internal fully burdened analyst/planner rate for a local estimate.</div>
</section>
"""
    return layout("sub", "Subscription", body, calculator_script())


def hours_calculator(ctx) -> str:
    return f"""<div class="calc" id="hours-calculator" data-hours="{ctx["known_hours"]}" data-tickets="{len(ctx["tickets"])}">
  <h3>Human-hours saved calculator</h3>
  <p>Uses the cumulative estimate stored in ticket records, then lets staff adjust the loaded hourly cost and reuse factor. Reuse factor accounts for the fact that a reusable report, table, or dashboard can support more than one meeting or decision.</p>
  <div class="calc-controls">
    <label>Total estimated hours<input id="calc-hours" type="number" min="0" step="1" value="{int(ctx["known_hours"])}"></label>
    <label>Loaded staff cost/hour<input id="calc-rate" type="number" min="0" step="5" value="70"></label>
    <label>Reuse factor<input id="calc-reuse" type="number" min="1" step="0.25" value="1"></label>
  </div>
  <div class="calc-output">
    <div class="calc-stat"><strong id="out-hours">0</strong><span>Equivalent hours</span></div>
    <div class="calc-stat"><strong id="out-value">$0</strong><span>Internal capacity value</span></div>
    <div class="calc-stat"><strong id="out-per-ticket">$0</strong><span>Value per ticket</span></div>
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
    <aside class="hero-panel"><h2>Mareto fit</h2><p>Use Mareto-style forms and workflows where the City needs recurring data from staff, partners, recipients, or residents. Use Karto to analyze the resulting evidence.</p></aside>
  </div>
</section>
<section class="section">
  <div class="table-panel"><table class="matrix"><thead><tr><th>Workflow</th><th>Data captured</th><th>Why it matters</th></tr></thead><tbody>{table}</tbody></table></div>
</section>
<section class="section">
  <div class="notice"><strong>Positioning:</strong> This is a data collection and reporting option, not a separate product detour. The purpose is to make future policy tickets faster, more local, and easier to defend.</div>
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
    <div><p class="eyebrow">Next Requests</p><h1>Ticket ideas based on Airdrie's actual demand pattern</h1><p class="hero-copy">These are scoped to the topics already appearing in Airdrie's tickets and public policy context: housing delivery, HAF, STRs, downtown, grant reporting, engagement, and regional pressure.</p><div class="actions"><a class="btn primary" href="{REQUEST_PAGE}" target="_blank" rel="noopener">Order in Karto</a></div></div>
    <aside class="hero-panel"><h2>How to use this</h2><p>Pick one card, paste the title into the Karto request workflow, and attach any current council package or staff report that should anchor the work.</p></aside>
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


def write_page(path: Path, html_text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_text)


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
    manifest = {
        "ticket_records": len(ctx["tickets"]),
        "dashboard_records": len(ctx["dashboards"]),
        "insight_records": len(ctx["insights"]),
        "completed_file_refs": ctx["completed_files"],
        "supporting_file_refs": ctx["supporting_files"],
        "known_estimated_hours": ctx["known_hours"],
        "public_attachment_filenames_mirrored": False,
        "protected_download_source": TICKET_LIST_PAGE,
    }
    (ROOT / "build-manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
