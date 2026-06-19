---
name: troubleshoot-account-verification
description: |
  Troubleshoots Microsoft Partner Center *account verification* friction when an
  ISV/partner is trying to publish a Microsoft 365 Copilot agent to the Microsoft
  Commercial Marketplace. Converges four common failure classes — identity/roles,
  legal-entity & tenant binding, business-existence evidence, and process visibility —
  into one verified, publish-ready account state, and routes each symptom to the block
  that unblocks it. Use when the user says things like "I can't sign in to Partner
  Center", "I didn't get the verification code", "what roles do I need", "the tenant
  doesn't match", "Publisher Verification is stuck", "is my Microsoft App ID correct",
  "Global Admin but can't assign roles", "how long does verification take", or "what
  stage is my submission at". It guides preparation only — it never signs in, assigns
  roles, or submits on the user's behalf.
license: MIT
metadata:
  author: Mamoru Kuroda
  version: "0.1.0"
  last_updated: "2026-06-19"
---

# Troubleshoot: Partner Center Account Verification

Gets an ISV/partner *unstuck* on Partner Center account verification so they can publish a
Microsoft 365 Copilot agent to the Microsoft Commercial Marketplace.

> **EXPERIMENTAL — guidance only.** This skill diagnoses and prepares. It **never** signs in
> to Partner Center, assigns roles, edits Microsoft Entra, or submits anything on the user's
> behalf. Every portal action is performed by the user. Never ask for or store passwords,
> verification codes, or secrets.

## Design: converge from the endpoint

There is exactly **one** goal state. All friction, regardless of the symptom or the path the
user took to get stuck, resolves into the **same four-condition definition of done**. The four
classes below are *triage axes into one answer*, not four separate destinations.

### The convergence answer — "a verified, publish-ready Partner Center account"

| # | Condition (done = ✅) | Met when |
| --- | --- | --- |
| **1. Identity & roles** | The right person can sign in with the right role | User signs in to Partner Center with a work (Microsoft Entra) account, and holds a role that can do the intended task (publish / manage users) |
| **2. Legal entity & tenant** | The publisher's tenant and app identity line up | The Microsoft Entra tenant used to register the app is the **same tenant** as the Partner Center account; publisher legal name/address are consistent; the app's **Microsoft App ID = the Entra application (client) ID** |
| **3. Business existence** | The org is verified as real | Publisher/employment verification is complete; account enrolled in the **Microsoft 365 and Copilot program**; legal/primary-contact info present; **MAICPP / MPN (Partner) ID** available where required |
| **4. Process visibility** | The user knows where they are and how to move | The user knows the current stage, the save→publish→submit order, the typical timeline, and how to escalate (Support Request) when the UI itself is broken |

> Always present this 4-row checklist with the user's current ✅ / ⛔ / ❓ status. It is the
> shared "definition of done" for every path through this skill.

## Triage — one question routes to the blocking condition

Ask **one** question, then jump to the matching block. Stop early; don't run blocks the user
isn't blocked on.

> "Where are you stuck right now?"
> - **A** — *Can't sign in, no verification code, or 'you don't have permission / can't assign roles.'* → Block 1 (Identity & roles)
> - **B** — *'Tenant doesn't match', unsure which tenant to register the app in, or 'is my Microsoft App ID right'.* → Block 2 (Legal entity & tenant)
> - **C** — *Publisher Verification / Attestation / legal info / partner (MPN) ID is incomplete or rejected.* → Block 3 (Business existence)
> - **D** — *Submitted/saved but don't know the status, the order of steps, or how long it takes.* → Block 4 (Process visibility)

Map the user's own words to A–D from these real-world phrasings (do not require them to know the
category names):

| User says… | Class |
| --- | --- |
| "コードが来ない / can't sign in / 招待されたが入れない" | A |
| "Global Admin なのに Role を付与できない" | A → see **escalation fork** |
| "誰のアカウントで申請するの / who should be the contact" | A → see **role-owner fork** |
| "Entra のテナントは Partner Center と同じ？ / tenant mismatch" | B |
| "Microsoft App ID は Application ID で合ってる？" | B |
| "Publisher Verification が進まない / MPN ID とは" | C |
| "保存と送信どっちが先 / 審査はいつ始まる / how long" | D |

## Block 1 — Identity & roles

**Goal:** the right person signs in with a role that can do the task.

1. **Sign-in basics.** Partner Center is accessed with a **work account associated with a
   Microsoft Entra tenant**. Any Entra member of the tenant can *sign in*; what they can *do* is
   governed by roles. If the user can't sign in at all, confirm they're using the work account in
   the **correct tenant** (not a personal/consumer account), and that they were added as a member
   of that tenant first.
2. **Pick the right role for the task — names matter.** Verify against the references; the casual
   names people use in chat often don't match the portal.

   | Task | Roles that can do it (canonical) |
   | --- | --- |
   | **Publish / manage a Microsoft 365 Copilot agent offer** (Microsoft 365 & Copilot *developer* program) | **Owner**, **Manager**, **Developer** |
   | **Assign/manage user roles** | Account Admin, Global Admin, User Management Admin (commercial programs) **or** Owner / Manager (developer programs) |
   | Update Apple ID / developer account settings | Developer Account **Owner** or **Manager** |

   > Caution on wording: "Account admin" is a **MAICPP** (Microsoft AI Cloud Partner Program) role,
   > **not** the role that publishes a Copilot agent. Some portal screens show checkboxes such as
   > "Account admin" / partner-program admin in a MAICPP context — don't assume those are what's
   > needed to publish. Confirm the **developer-program** roles (Owner/Manager/Developer) for
   > publishing. Verify current names in the references before quoting.
3. **Assigning roles (the user does this in the portal):** Partner Center → **Settings →
   Account Settings → User management** → select the user → set roles → **Update**. For developer
   programs the assigner must be an **Owner or Manager**; for commercial programs a Global Admin /
   User Management Admin / Account Admin.

### Escalation fork — "Global Admin but can't assign roles"

If the user has a top-level admin role yet the **role-assignment UI fails** (a known issue on
some **older Partner Center accounts**): this is no longer a permissions problem — it's a portal
defect. Route to **Block 4 → Support Request**. The fix path is a Microsoft **Support Request**,
not more permission changes.

### Role-owner fork — "who should do this / who has the top role"

If the blocker is *who* to ask: the user (or their admin) can look up role holders and the
**primary/first contact** in Partner Center → Settings → Account Settings (User management;
and Legal info → Partner tab → primary contact). Identify that person and have them perform the
role assignment or sign-in. This skill identifies *who*; it does not contact them.

## Block 2 — Legal entity & tenant binding

**Goal:** the app's tenant and identity line up with the verified publisher.

1. **Same-tenant rule.** The Microsoft Entra tenant where the app is **registered** must be the
   **same tenant** as the Partner Center account used to publish. A mismatch is a common, silent
   blocker — the app won't be recognized as the publisher's. Have the user confirm the tenant ID
   on both sides matches before proceeding.
2. **App ID identity.** The **Microsoft App ID** requested during submission is the **Application
   (client) ID** of the Microsoft Entra app registration — confirm they're using that exact value,
   not the object ID or an enterprise-app ID.
3. **Publisher legal consistency.** Publisher legal name and address should be consistent across
   the Entra tenant, the Partner Center account, and the app manifest's developer/publisher fields.
   The publisher chosen for an offer must be enrolled in the Microsoft 365 and Copilot program and
   **cannot be changed after the offer is created** — get this right up front.

## Block 3 — Business existence evidence

**Goal:** the organization is verified as a real, enrolled publisher.

1. **Program enrollment.** Publishing a Copilot agent requires enrollment in the **Microsoft 365
   and Copilot program** (open an Office/developer account in Partner Center). Without it, the
   "Microsoft 365 and Copilot" tab / offer types won't appear.
2. **Publisher / employment verification.** Complete any publisher-verification and
   employment-verification steps Microsoft prompts for. These prove the org and the user's
   association with it.
3. **Partner (MPN / MAICPP) ID.** Where a partner ID is required, locate the **MPN ID** (now under
   the **Microsoft AI Cloud Partner Program / MAICPP**) in Partner Center. Confirm the exact label
   in-portal against the references — naming has changed over time (MPN → Cloud Partner Program).
4. **Legal info & primary contact.** Ensure Settings → Account Settings → **Legal info → Partner
   tab → primary contact** is filled; reviewers and verification rely on it.

## Block 4 — Process visibility

**Goal:** the user knows the current stage, the order of operations, and how to move.

1. **Order of operations.** Typical flow for an agent offer: fill the offer → **Save draft** →
   **publish** the agent so review begins → then **Submit** when prompted. Saving is not
   submitting; submitting before the agent is published/review-started is a common confusion.
2. **Timeline.** App submission typically takes **four to six weeks** and **often requires
   multiple rounds**. Set this expectation explicitly so silence isn't read as failure. Suggest
   checking status every 1–2 days.
3. **Reviewer test access.** If the agent needs sign-in or a paid service, the user must provide
   **reviewer test credentials / instructions** in the submission notes, or review will stall.
4. **Escalation (Support Request).** When the blocker is a portal defect (e.g., role assignment
   failing despite sufficient permissions, verification stuck with no actionable error), the path
   forward is a **Microsoft Support Request from Partner Center**, not repeated retries. Capture
   what was tried so the SR is actionable.

## Deliverables

1. **Status checklist** — the 4-condition table with ✅ / ⛔ / ❓ per condition.
2. **Diagnosis & next action** — which condition is blocking, and the single next step the user
   should take in the portal (or "raise an SR").
3. **`verification-ledger.json`** — write to the current working directory as the hand-off file
   (schema below); print its full path and a one-line summary.

## verification-ledger.json (schema)

```json
{
  "schemaVersion": "0.1.0",
  "createdAt": "<ISO-8601>",
  "goal": "verified-publish-ready-partner-center-account",
  "conditions": {
    "identityAndRoles":  { "status": "blocked|in-progress|met|unknown", "note": "" },
    "legalEntityTenant": { "status": "blocked|in-progress|met|unknown", "note": "" },
    "businessExistence": { "status": "blocked|in-progress|met|unknown", "note": "" },
    "processVisibility": { "status": "blocked|in-progress|met|unknown", "note": "" }
  },
  "triage": { "reportedClass": "A|B|C|D", "fork": "none|escalation|role-owner" },
  "escalation": { "supportRequestNeeded": false, "reason": "" },
  "context": { "tenantIdMatches": "yes|no|unknown", "program": "m365-and-copilot", "partnerIdKnown": "yes|no|unknown" },
  "audit": []
}
```

Append an `audit[]` entry for every diagnosis. Never write secrets or codes to the ledger.

## Where this runs (portability)

This skill is a portable **Agent Skill** (`SKILL.md`, the open standard). It runs as-is in
**GitHub Copilot CLI** (this plugin marketplace), and the `skills/` folder can be packaged into a
Microsoft 365 app package (`.zip` with `manifest.json` + icons) for **Microsoft 365 Copilot
Cowork**. It deliberately avoids slash-command-only invocation and sub-agents (not yet supported
in Cowork), relying on the natural-language triggers in the description above.

## References (authoritative; verify before quoting — names/labels drift)

- Partner Center roles & permissions: https://learn.microsoft.com/en-us/partner-center/account-settings/permissions-overview
- Distribution options for Copilot extensibility: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/publish
- App submission guide (10 steps, 4–6 week timeline): https://learn.microsoft.com/en-us/partner-center/marketplace-offers/add-in-submission-guide
- Open a developer (Office) account in Partner Center: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/open-a-developer-account
- Why publish (Microsoft 365 and Copilot program): https://learn.microsoft.com/en-us/partner-center/marketplace/why-publish
- Cowork plugin development (package format): https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development
