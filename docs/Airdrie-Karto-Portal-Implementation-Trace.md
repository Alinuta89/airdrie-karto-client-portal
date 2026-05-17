# Airdrie Karto Portal Implementation Trace

Last updated: 2026-05-17

## Current State

The City of Airdrie Karto workspace now uses a client-facing deterministic HTML layer hosted on GitHub Pages and embedded into the live Karto namespace. Compose remains the backend system of record for ticket records, attachments, dashboards, insights, and workflow triggers.

Primary live entry point:

- `https://main.karto.helpseeker.org/compose/ns/CoA/pages/489429604772085761`

GitHub Pages portal:

- `https://alinuta89.github.io/airdrie-karto-client-portal/`

Repository:

- `https://github.com/Alinuta89/airdrie-karto-client-portal`

## Architecture

The working pattern is:

1. Staff open the Airdrie Karto namespace.
2. Visible left-rail pages are polished HTML pages embedded as Karto iframes.
3. Raw Compose record-list/admin pages are hidden from the left rail.
4. The request intake HTML posts to the Airdrie Compose `tickets` module API.
5. Compose remains the system of record and the place where secure attachments live.
6. Existing after-create ticket workflows remain attached to the ticket module.

Important security boundary:

- Do not put OAuth client secrets in GitHub Pages JavaScript.
- The request form relies on the user's active Karto session cookie.
- Users must be signed into Karto before submitting from the HTML intake.

## Live Karto Namespace

Namespace:

- name: `City of Airdrie`
- slug: `CoA`
- namespace ID: `437118445986185217`

Main page:

- `Airdrie Service Plan`
- page ID: `489429604772085761`

Visible left rail after cleanup:

- `Airdrie Service Plan`
- `Request Workflow`
- `Delivery Library`
- `Insights Library`

Under `Request Workflow`:

- `Ticket Allowance`
- `Data Collection Options`
- `Next Request Ideas`

Under `Delivery Library`:

- `Parking Trade-Off Analysis`
- `Digital Billboard Risk Analysis`
- `Youth Service Hubs`
- `Housing and Labour`
- `Regional Housing Coalition`
- `Housing Pressure Index`

Under `Insights Library`:

- `Dashboard Gallery`

Hidden raw list pages:

- Organizations
- Tickets
- Insights
- Users
- Dashboards

## Current GitHub Pages Version

Latest pushed commit:

- `f8dc32a Make Airdrie portal staff-facing`

Commit chain:

- `10d980e Build Airdrie Karto client portal`
- `be8eb55 Refresh Airdrie portal after Gmail reconciliation`
- `70896c2 Add client-facing Airdrie ticket intake`
- `f8dc32a Make Airdrie portal staff-facing`

The live Karto iframe URLs were cache-busted to `?v=f8dc32a`.

## Client-Facing Pages

The portal currently builds these pages:

- `/` - service workspace overview
- `/request-workflow/` - staff request intake form
- `/subscription/` - now labelled `Ticket Allowance`
- `/delivery-library/` - polished report library and protected archive handoff
- `/dashboard-gallery/` - dashboard records surfaced as a gallery
- `/insights/` - recurring insight themes
- `/data-collection/` - structured data collection options
- `/next-requests/` - draft request ideas
- `/housing-labour/` - housing/labour nexus summary

Staff-facing copy rules applied:

- Say `Ticket Allowance`, not `pay-as-you-go`.
- State `10 tickets per month`.
- Avoid sales language.
- Avoid internal backend terms such as `Compose` or `backend` on client-facing pages.
- Use practical submitter language: question, audience, deadline, output, files.

## Ticket Intake Flow

Current intake page:

- `https://alinuta89.github.io/airdrie-karto-client-portal/request-workflow/?v=f8dc32a`

Live Karto wrapper:

- `https://main.karto.helpseeker.org/compose/ns/CoA/pages/437118446045495297`

Write target:

- Airdrie Compose `tickets` module
- module ID: `437118446006632449`

Fields used by the HTML form:

- `ticket_name`
- `ticket_topic`
- `description`
- `objective`
- `urgency`
- `required_completion_date`
- `date_submitted`
- `geographic_scope`
- `output_format`
- `content_volume`
- `est_hrs`
- `brand`
- `private_ticket`
- `t_ticket_event_status`
- `status_notes`

Status written on submit:

- `t_ticket_event_status = Submitted`

Known caveat:

- A controlled live test ticket has not yet been submitted because it may trigger workflow emails.

Before relying on production notifications, run one test ticket with an obvious test title and verify:

- record appears in the Airdrie `tickets` module
- `status_notes` says it came from the Airdrie request form
- existing after-create workflow sends only intended notifications
- no duplicate/stale workflow fires

## Workflow Notes

Existing enabled Airdrie workflows seen during audit:

- `airdrie_ticket_notification`
- workflow ID: `437886485295792129`
- `airdrie_notification_workflow`
- workflow ID: `462208522698031105`

The second workflow has active triggers on:

- `compose:record afterCreate`
- namespace handle: `CoA`
- module handle: `tickets`

That means records created by the HTML intake should enter the same workflow path as records created inside Compose, subject to login/session and permission behavior.

## Gmail Reconciliation

Visible Gmail sent/search review found two Airdrie items not represented as exact ticket records. These were added to the Airdrie ticket module:

- `Parking scenario engine`
- record ID: `495422687078776833`
- `Youth Integrated Hubs - email-delivered report`
- record ID: `495422943887622145`

Ticket count changed:

- before: `103`
- after: `105`

Ambiguous Gmail-visible rows not added:

- `Re: [EXTERNAL] RE: Data -`
- `Re: [EXTERNAL] Re: Exp...`
- `Karto analytics session invite`
- `HAF contact list`

Reason:

- Visible snippets were not enough to prove a scoped ticket or exact mapping.

## Static Metrics Caveat

GitHub Pages metrics are currently static snapshots generated by `build_pages.py`.

Current snapshot:

- ticket records: `105`
- dashboard records: `7`
- insight records: `22`
- completed file references: `91`
- supporting file references: `24`
- staff hours noted: `1,150`
- Gmail-reconciled records: `2`

When new tickets are submitted, Compose updates immediately. The polished HTML metrics do not update automatically unless the portal is rebuilt and pushed again.

Future improvement options:

- scheduled GitHub Action that pulls Karto records and rebuilds pages
- authenticated client-side reads for logged-in Karto users
- server-side proxy/middleware for safe read/write without exposing credentials

## Local Build and Audit Paths

Local portal repo:

- `/tmp/airdrie-karto-client-portal`

Local audit bundle:

- `/tmp/airdrie-karto-audit`

Key audit notes:

- `/tmp/airdrie-karto-audit/AIRDRIE-KARTO-CLIENT-PORTAL-AUDIT.md`
- `/tmp/airdrie-karto-audit/AIRDRIE-LEFT-RAIL-GMAIL-RECONCILIATION.md`
- `/tmp/airdrie-karto-audit/HTML-REQUEST-WORKFLOW-DEPLOYMENT.md`
- `/tmp/airdrie-karto-audit/STAFF-FACING-COPY-CLEANUP.md`

Key scripts:

- `/tmp/airdrie-karto-client-portal/build_pages.py`
- `/tmp/airdrie-karto-client-portal/portal-assets/request-intake.js`
- `/tmp/airdrie-karto-audit/embed_airdrie_client_portal.py`
- `/tmp/airdrie-karto-audit/organize_airdrie_left_rail.py`
- `/tmp/airdrie-karto-audit/add_gmail_reconciled_tickets.py`
- `/tmp/airdrie-karto-audit/activate_html_request_workflow.py`
- `/tmp/airdrie-karto-audit/update_airdrie_staff_facing_copy.py`

Do not copy secrets from any local helper scripts into GitHub Pages or wiki documentation.

## Verification Commands

Check latest repo commit:

```bash
git -C /tmp/airdrie-karto-client-portal log -1 --oneline
```

Rebuild pages:

```bash
python3 /tmp/airdrie-karto-client-portal/build_pages.py
node --check /tmp/airdrie-karto-client-portal/portal-assets/request-intake.js
```

Check for removed/salesy/internal terms:

```bash
rg -n "pay-as|Pay-as|sales|Mareto|Compose|backend|middle|Order|order|product pitch|capacity value|Internal capacity|Quota|quota|native|raw Compose|Workflow fires|admin entry" /tmp/airdrie-karto-client-portal
```

Verify hosted ticket allowance page:

```bash
curl -L -s -H 'Cache-Control: no-cache' 'https://alinuta89.github.io/airdrie-karto-client-portal/subscription/?v=f8dc32a' | rg -n "Ticket Allowance|10 tickets per month|Monthly subscription|10/month"
```

Verify hosted request page:

```bash
curl -L -s -H 'Cache-Control: no-cache' 'https://alinuta89.github.io/airdrie-karto-client-portal/request-workflow/?v=f8dc32a' | rg -n "Submit a new request|What happens next|Submit the request"
```

## Future Work Checklist

1. Run one controlled live intake submission after confirming workflow email expectations.
2. Add a refresh job for static metrics.
3. Decide whether staff need a post-submit link to the newly created secure ticket record.
4. Decide whether confidential attachment upload should remain manual or be wrapped in a safer guided flow.
5. Re-audit left rail after any new pages are added.
6. Keep all client-facing copy practical and staff-oriented.
