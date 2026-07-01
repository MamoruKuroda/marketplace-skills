---
name: troubleshoot-account-verification
description: |
  Troubleshoots Microsoft Partner Center *account verification* friction when an ISV or
  partner is publishing a Microsoft 365 Copilot agent to the Microsoft Commercial
  Marketplace. Converges identity & roles, legal-entity & publisher identity, business
  existence, and process visibility into one verified, publish-ready account state. Use
  when the user is stuck on Partner Center sign-in or verification codes, which roles are
  needed (Owner/Manager/Developer vs "Account admin"), "Global Admin but can't assign
  roles", which tenant to register the app in or whether it must match Partner Center,
  the Microsoft App ID vs Application (client) ID, Publisher Verification, MPN / Partner
  One ID / MAICPP, the primary contact, the "Microsoft 365 and Copilot" tab not
  appearing, or how long verification takes (also Japanese: コードが届かない /
  ロールを割り当てられない / 審査が長い). Guidance only: never signs in, assigns roles, edits
  Entra, or submits, and never asks for passwords or codes.
user-invocable: false
license: MIT
metadata:
  author: Mamoru Kuroda
  version: "0.2.2"
  last_updated: "2026-07-01"
---

# Troubleshoot: Partner Center Account Verification

Gets an ISV/partner *unstuck* on Partner Center account verification so they can publish a
Microsoft 365 Copilot agent to the Microsoft Commercial Marketplace.

> **Internal specialist skill (`user-invocable: false`).** The plugin's entry point is
> [`partner-center-guide`](../partner-center-guide); it triages broadly and delegates here when
> account *verification* is the actual blocker. This skill goes deep on the four-condition
> convergence and emits `verification-ledger.json`.

> **EXPERIMENTAL — guidance only.** This skill diagnoses and prepares. It **never** signs in
> to Partner Center, assigns roles, edits Microsoft Entra, or submits anything on the user's
> behalf. Every portal action is performed by the user. Never ask for or store passwords,
> verification codes, or secrets.

## Operating contract (MUST — every invocation)

Run all four of these **every time**, including single-shot / non-interactive (`-p`) runs.
**Do not stall waiting for input.**

1. **Classify** the user's situation into Condition 1–4 directly from their message (the moment
   of being stuck is usually one sentence). Only if it is genuinely ambiguous, ask **one** routing
   question; otherwise proceed.
2. **Diagnose** in the matching condition's section below.
3. **Always output** the **4-condition status checklist** (✅ / ⛔ / ❓ for all four conditions)
   and the **single next action**.
4. **Always write `verification-ledger.json`** to the current working directory, then print its
   full path and a one-line summary.

If you must assume something to proceed, **state the assumption** rather than stopping to ask.
These four outputs are mandatory in every response — never skip the checklist or the ledger.

## Design: converge from the endpoint

There is exactly **one** goal state. All friction, regardless of the symptom or the path the
user took to get stuck, resolves into the **same four-condition definition of done**. The four
classes below are *triage axes into one answer*, not four separate destinations.

### The convergence answer — "a verified, publish-ready Partner Center account"

| # | Condition (done = ✅) | Met when |
| --- | --- | --- |
| **1. Identity & roles** | The right person can sign in with the right role | User signs in to Partner Center with a work (Microsoft Entra) account, and holds a role that can do the intended task (publish / manage users) |
| **2. Legal entity & publisher identity** | The publisher identity and the app identity line up | Publisher legal name/address are consistent; the app's **Microsoft App ID = the Entra application (client) ID**; tenant *equality* with Partner Center is **not** required — if the verified-publisher badge is wanted, the app-registration tenant is **associated with the Partner Global Account (PGA)** |
| **3. Business existence** | The org is verified as real | Publisher/employment verification is complete; account enrolled in the **Microsoft 365 and Copilot program**; legal/primary-contact info present; **MAICPP / MPN (Partner) ID** available where required |
| **4. Process visibility** | The user knows where they are and how to move | The user knows the current stage, the save→publish→submit order, the typical timeline, and how to escalate (Support Request) when the UI itself is broken |

## Terminology — canonical terms & disambiguation (do this first)

Real users' wording drifts, and some terms are genuinely two different things. Before answering,
map the user's words to the **canonical term**, restate it briefly, and **if a term is ambiguous,
ask exactly one disambiguating question** before proceeding (then continue without stopping for
anything already clear).

| User may say (alias) | Canonical term | One-line meaning |
| --- | --- | --- |
| Publisher Verification, 発行元確認, 青バッジ, verified badge | **Entra publisher verification** (app badge) **vs** **Partner Center business verification** (org/account) | Two different things — confirm which: the app's blue *verified-publisher* badge (Condition 2) or your organization/account being verified & enrolled (Condition 3) |
| MPN ID, MPN, パートナー ID | **Partner One ID** (under **MAICPP**, formerly MPN) | Your partner-program identifier |
| Account admin (used as a *publishing* role) | dev-program **Owner / Manager / Developer** | "Account Admin" is a **MAICPP** role, not the role that publishes an agent |
| Microsoft App ID, app registration ID | **Application (client) ID** | The Entra app registration's client ID (not object ID / enterprise-app ID) |
| same tenant, 同じテナント, tenant match | app tenant **associated with the PGA** | Not "= Partner Center tenant"; tenant equality is **not** required, multitenant association is |
| MAICPP, CPP, AI Cloud Partner program | **Microsoft AI Cloud Partner Program** | Formerly Microsoft Partner Network (MPN) |
| PGA | **Partner Global Account** | Top-level account a MAICPP/CPP membership hangs under |

## Triage — classify from the user's one sentence

The moment of being stuck is usually expressible in one sentence. **Classify it into Condition
1–4 from the phrasings below** (don't require the user to know the category names). Per the
Operating contract, proceed directly; only ask a routing question if it is truly ambiguous.

| User says… | Condition | Note |
| --- | --- | --- |
| "コードが届かない / can't sign in / 招待されたが入れない" | 1 | |
| "what roles do I need / Account admin でいい?" | 1 | publishing = Owner/Manager/Developer |
| "Global Admin なのに Role を付与できない / ロールを割り当てられない" | 1 | see **role-cause → SR fork** |
| "誰のアカウントで申請 / who should be the primary contact" | 1 | see **role-owner fork** |
| "Entra のテナントは Partner Center と同じ必要? / which tenant / multitenant?" | 2 | tenant equality NOT required |
| "Microsoft App ID は Application (client) ID で合ってる?" | 2 | |
| "発行元の確認 / Publisher Verification / 青バッジ / publisher domain" | 2 or 3 | **disambiguate** (badge vs org verification) |
| "MPN / Partner One ID / MAICPP とは / employment verification" | 3 | |
| "'Microsoft 365 and Copilot' タブが出ない / program enrollment" | 3 | |
| "保存と送信どっちが先 / 審査はいつ始まる / 審査が長い / 差し戻された / how long" | 4 | |

## Condition 1 — Identity & roles

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

### Role-cause → Support Request fork — "admin but can't assign roles" (rule out the spec cause FIRST)

When the user is a top-level admin yet "can't assign roles", resolve in this **order** — do not
jump straight to "portal defect":

1. **First rule out the most common, by-design cause.** Assigning roles in a **developer program**
   (Microsoft 365 & Copilot / Marketplace) requires the assigner to be an **Owner or Manager** of
   that program — being **Global Admin alone is not sufficient** for developer-program role
   assignment (Global Admin governs commercial programs like MAICPP/CSP). Confirm the assigner
   holds Owner/Manager in the correct program context, and that they're on the developer-program
   user-management screen, before concluding anything is broken.
2. **Only if** the assigner already holds the correct role **and** the assignment UI still fails
   (a known issue on some **older Partner Center accounts**) is it a portal defect → raise a
   **Microsoft Support Request** (see Condition 4). Capture what was tried so the SR is actionable.

### Role-owner fork — "who should do this / who has the top role"

If the blocker is *who* to ask: the user (or their admin) can look up role holders and the
**primary/first contact** in Partner Center → **Settings → Account Settings → User management**
(and **Legal info → Partner tab → primary contact**). Identify that person and have them perform
the role assignment or sign-in. This skill identifies *who*; it does not contact them.

## Condition 2 — Legal entity & publisher identity

**Goal:** the publisher identity and the app identity line up. (Tenant *equality* with Partner
Center is **not** required.)

1. **Tenant equality is NOT required.** A Copilot agent published to Marketplace is a
   **multitenant** app; the Microsoft Entra tenant where the app is **registered** does **not**
   have to be the same tenant as the Partner Center account. If a tool, a partner, or a colleague
   insists the tenants "must be identical", that is almost always a misread of **publisher
   verification** (next point) — clarify rather than forcing tenant equality.
2. **Entra publisher verification (the blue "verified" badge) — only if you want it.** To earn the
   verified-publisher badge for the app, the Entra tenant where the app is registered must be
   **associated with your Partner Global Account (PGA)** — *not necessarily the same tenant*;
   multitenant association is supported. Also required: the app's **publisher domain** must match
   the domain used to verify your MAICPP/CPP account (and **cannot be `*.onmicrosoft.com`**), and
   the user must hold the required roles in **both** Microsoft Entra and Partner Center. This is an
   *app publisher-identity* feature, distinct from the *organization/account* verification in
   Condition 3.
3. **App ID identity.** The **Microsoft App ID** requested during submission is the **Application
   (client) ID** of the Microsoft Entra app registration — confirm they're using that exact value,
   not the object ID or an enterprise-app ID.
4. **Publisher legal consistency.** Publisher legal name and address should be consistent across
   the Entra tenant, the Partner Center account, and the app manifest's developer/publisher fields.
   The publisher chosen for an offer must be enrolled in the Microsoft 365 and Copilot program and
   **cannot be changed after the offer is created** — get this right up front.

> Out of scope: **monetization / SaaS-offer** tenant and Entra-app configuration (linked SaaS
> offer, SaaS fulfillment app registration, metering) is **not** part of account verification.
> If the user asks about those, point them to the `agent-publishing` plugin's
> `monetization-saas-offer` skill instead of answering here. Do not pull SaaS-fulfillment rules
> into account-verification advice.

## Condition 3 — Business existence evidence

**Goal:** the organization is verified as a real, enrolled publisher.

> Two different "verifications" share the name — keep them apart. **Entra publisher verification**
> (the blue badge; PGA-associated app tenant + publisher domain — see Condition 2) is about your
> *app's* publisher identity. **Partner Center business / identity & employment verification**
> (this condition) is about your *organization and account* being a real, enrolled publisher.
> Being stuck on one does not mean being stuck on the other; if the user says "Publisher
> Verification", confirm which they mean first.

1. **Program enrollment.** Publishing a Copilot agent requires enrollment in the **Microsoft 365
   and Copilot program** (open an Office/developer account in Partner Center). Without it, the
   "Microsoft 365 and Copilot" tab / offer types won't appear.
2. **Publisher / employment verification.** Complete any business/identity and employment
   verification steps Microsoft prompts for. These prove the org and the user's association with it.
3. **Partner (MPN / Partner One ID under MAICPP).** Where a partner ID is required, locate the
   **Partner One ID** — the identifier under the **Microsoft AI Cloud Partner Program (MAICPP**,
   formerly **MPN)** — in Partner Center. Confirm the exact label in-portal against the references;
   naming has changed over time (MPN → MAICPP; "MPN ID" → "Partner One ID").
4. **Legal info & primary contact.** Ensure Settings → Account Settings → **Legal info → Partner
   tab → primary contact** is filled; reviewers and verification rely on it.

## Condition 4 — Process visibility

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

## Deliverables (mandatory — see Operating contract)

Produce **all three on every invocation**, even single-shot / `-p`, even if you had to assume the
class:

1. **Status checklist** — the 4-condition table with ✅ / ⛔ / ❓ for **all four** conditions.
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
    "identityAndRoles":         { "status": "blocked|in-progress|met|unknown", "note": "" },
    "legalEntityPublisherId":   { "status": "blocked|in-progress|met|unknown", "note": "" },
    "businessExistence":        { "status": "blocked|in-progress|met|unknown", "note": "" },
    "processVisibility":        { "status": "blocked|in-progress|met|unknown", "note": "" }
  },
  "triage": { "reportedClass": "1|2|3|4", "fork": "none|role-cause-sr|role-owner" },
  "escalation": { "supportRequestNeeded": false, "reason": "" },
  "context": { "tenantAssociatedWithPGA": "yes|no|n/a|unknown", "program": "m365-and-copilot", "partnerIdKnown": "yes|no|unknown" },
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
- Entra publisher verification (blue badge; PGA association, publisher domain): https://learn.microsoft.com/en-us/entra/identity-platform/publisher-verification-overview
- Distribution options for Copilot extensibility: https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/publish
- App submission guide (10 steps, 4–6 week timeline): https://learn.microsoft.com/en-us/partner-center/marketplace-offers/add-in-submission-guide
- Open a developer (Office) account in Partner Center: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/open-a-developer-account
- Why publish (Microsoft 365 and Copilot program): https://learn.microsoft.com/en-us/partner-center/marketplace-offers/why-publish
- Cowork plugin development (package format): https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development
