Create a detailed Excalidraw diagram of a Vendor Query Management System Architecture with the following exact flow and components:

**Top-level flow (left to right / top to bottom):**

1. **VENDOR (External)** box at the top → arrow labeled "Sends Email" → **EMAIL CHANNEL (Mailbox)** box capturing: sender, subject, timestamp, thread ID, attachments

2. **INTEGRATION / ORCHESTRATION LAYER** (full-width box) labeled: Middleware: Routes, Retries, Logs, Governance Controls — sits below the mailbox

3. Three branches from the Integration Layer going down to:
   - **SALESFORCE (Vendor Master)** — contains: Vendor ID, Status, Tier, Contract, SLA Category, Contacts
   - **GenAI ENGINE** — Step 2: Intent Classification, Entity Extraction, Urgency Detection, Sentiment, Confidence Score
   - **ServiceNow (Ticketing)** — Step 4: Create Ticket, Update Ticket, Populate Fields, SLA Tracking, Audit Logs

4. **Step 3: Vendor Match** arrow from Salesforce back to GenAI — Email Match → Vendor ID Match → Name Similarity

**Detailed Step-by-Step Flow section (as a vertical swimlane or sequential flow):**

- STEP 1: Email Intake → Capture Metadata → Send to GenAI
- STEP 2: GenAI Understanding → Intent + Extraction → Confidence Score → HIGH branch: Auto Process / LOW branch: Human Triage Queue
- STEP 3: Vendor Match → Email Match → Vendor ID Match → Name Similarity → Fetch Vendor Context
- STEP 4: Ticket Create/Update → New Thread? YES → Create New Ticket / NO → Append to Existing Ticket
- STEP 5: Acknowledgment Email → GenAI Draft → Template + Ticket No. + SLA Timeline → High Confidence: AUTO SEND / Low Confidence: DRAFT for Human Review
- STEP 6: Intelligent Routing → Intent/Category → Finance / Procurement / IT / Legal → Vendor Tier + Urgency → Priority Adjustment
- STEP 7: Investigation Support (AI Copilot) → Agent View: Vendor Snapshot + Ticket History → GenAI: Suggest Resolution + Draft Response Options
- STEP 8: Hold/Resume Logic → Docs Needed? → Awaiting Vendor (SLA Paused) / Internal Dep? → Awaiting Internal Info (SLA Paused)
- STEP 9: Escalation Logic → SLA Timer: 70% → 85% → 95% → ALERT → High Tier Vendor / Negative Sentiment → Auto Escalate → Escalation Email → Manager Review
- STEP 10: Resolution + Closure → Resolved → GenAI Draft Resolution Email → Vendor Confirms: CLOSE Ticket / No Response: Auto-Close (Policy Window) → Vendor Replies After Close? YES: Detect + Reopen/Link to Prior Ticket / NO: Generate Final Audit Summary

**Bottom summary panels (3 separate bordered boxes):**

- **ROLES SUMMARY**: Vendor, Support/Triage, Resolver Groups, Manager, GenAI System, Admin — each with their responsibility
- **GOVERNANCE CONTROLS**: Confidence Score → Auto-Send vs Draft vs Human Triage, Audit Logs, RBAC, Attachment Scan, Prompt Control
- **OUT OF SCOPE (Phase 1)**: Payment Authorization, Contract Modification, Legal Decision Making, Salesforce Master Data Edit (without approval), Fully Autonomous Resolution

**Styling:**
- Use distinct background colors per section: blue for system components, green for GenAI, orange for Salesforce, purple for ServiceNow, red for escalation/out-of-scope, yellow for governance
- Diamond shapes for decision nodes (New Thread?, High/Low Confidence, Docs Needed?, Vendor Confirms?)
- Rectangles for process steps
- Arrows with labels connecting all steps
- Bold section headers for each major group
- Keep layout clean and readable with generous spacing between sections