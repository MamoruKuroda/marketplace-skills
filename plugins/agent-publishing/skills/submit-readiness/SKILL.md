---
name: submit-readiness
description: "Blocking pre-submission gate for Microsoft Commercial Marketplace. Verifies program enrollment, legal/privacy/test-instructions, and Responsible AI readiness, then emits a Launch Gate report and a copy-paste Partner Center submission worksheet pre-filled from the ledger. Marketplace submission has no reliable API for this app type and is always done by a human."
argument-hint: "Reads publishing-ledger.json. Needs publisher legal entity, privacy policy URL, EULA, support URL, and test credentials/instructions."
user-invocable: true
last_updated: "2026-06-25"
---

# Submit Readiness (Marketplace Gate)

The final, shared gate before a human submits to Partner Center. It blocks on missing mandatory
items, then produces a Launch Gate report and a step-by-step manual submission guide.

> Hard fact: Microsoft 365 / Teams agent app types are **excluded from the older Partner Center
> Submission API**. Submission, store listing, and review are **GUI/manual** in Partner Center.
> This skill prepares; it cannot submit.
>
> Preview note (2026-04): The newer **Product Ingestion API** (`https://graph.microsoft.com/rp/product-ingestion`)
> added the "AI Apps and Agents" category and M365 Copilot app schemas (e.g.
> `m365-copilot-app-technical-configuration`) in **preview**, allowing declarative offer configuration and
> app-package upload. Even so, publishing still triggers the standard certification flow and a manual
> **Go-live**, and no end-to-end guide is published yet — so the API value is essentially configure/draft
> automation. This skill keeps the manual portal flow as the primary, reliable path.
>
> Portal-walk note (2026-06): "AI Apps and Agents" is the API-side category tag and the offer-type
> family — it is **not** a selectable value in the manual portal's **Properties → Categories** list,
> which is functional (Legal+HR, Productivity, etc.). Do not paste "AI Apps and Agents" into Categories.

## Create is a one-way door (warn before reserving the name)

Clicking **Create** in the new-offer dialog reserves the offer name and creates a draft. Two things
become **permanent** at that moment and cannot be changed afterward:

1. **Product type** — the dialog states *"you can't change the product type once created."*
2. **Publisher binding** — the offer is tied to the creating publisher account permanently.

What is **not** permanent: an **unpublished draft can be deleted**. The portal shows a **Delete**
button on the offer pages; the confirmation reads *"Any names you reserved will be released, and any
work in progress will be lost."* So the reserved name is freed and the draft is removed. (The
"name reservation expires" language in Learn refers only to releasing the **name**, not auto-deleting
a draft — drafts persist until you delete them.) Irreversibility only fully applies **after publish**
(a live offer can only be **Stop distribution**, not deleted). Tell the user: pick the product type and
publisher account deliberately, but a wrong-but-unpublished draft is safe to delete and start over.

## Collect tenant context (just-in-time)

Triage does not collect tenant info. Before building the worksheet, read `publishing-ledger.json`
`tenant`; if `publisherDisplayName` or `offerName` is empty, ask the user now and write them back to
the ledger. Explain they must match Partner Center. Never assume; never store secrets.

## Program enrollment (verify first)

| Program | When required | Purpose |
| --- | --- | --- |
| Microsoft 365 and Copilot program | always | publish the agent app package |
| Microsoft Marketplace program | if `monetize == true` | monetize via a linked SaaS offer |

If `monetize == true` and only the M365 & Copilot program is enrolled, BLOCK and instruct the user
to also enroll in the Marketplace program (and ensure `monetization-saas-offer` has run).

> Portal signal (verified 2026-06): there is **no "Microsoft 365 and Copilot" tab** in Marketplace
> offers. The real enrollment signal is whether **+ New offer** lists **"Apps and agents for
> Microsoft 365 and Copilot"** as an offer type. If it does, the program is enrolled.

## Blocking checklist (top causes of ~80% of rejections)

Block submission and list every missing item:

1. Valid **End User License Agreement (EULA) link** (https, not 404). The portal field is literally
   "EULA link" on the Properties page; if you do **not** accept the Standard Contract you must supply
   your own EULA URL.
2. Valid **Privacy Policy** link (separate from EULA; https, not 404; names the app/service, not just
   the company site).
3. Valid **Support document link** (https, not 404) — also required on the Properties page.
4. **Reviewer test instructions** present (test account / license key / SSO fallback steps), entered
   in **Notes for certification** on the Review and publish page.
5. **Service/account disclosure** specified.
6. **Additional-purchase disclosure** — if the agent requires a paid service, set **Additional
   purchases = Yes** on Product setup; that **forces** test credentials / a license key into the
   Notes for certification box.
7. **App package validation PASS** (from `validate-package`: both validation-rules and test-cases).
   Battle-tested 2026-06: a correctly built declarative `appPackage.<env>.zip` passes the portal's
   "Manifest checks passed"; a zip with no `manifest.json` is rejected with `ManifestFileNotFound`.
8. **Icons and listing media** — note there are **two separate icon systems**:
   - **App-package icons** (inside the .zip): color **192x192**, outline **32x32**.
   - **Marketplace listing assets** (per language, on the Marketplace listings page): **Marketplace
     icon 300x300** (≤512 KB) and **Screenshots 1366x768** (up to 5, ≤1024 KB each), plus
     Name / Summary / Description text. These are required and are **not** the package icons.
9. **Responsible AI readiness** self-attestation (see below) — RAI is reviewed by humans
   post-submission; ensure the agent meets RAI validation expectations.

> **Publisher Attestation / App Compliance is _not_ a blocker here.** All public sources mark the
> Microsoft 365 App Compliance Program (including Publisher Attestation) as **Optional** — see the
> note below. Do not list it as a required submission gate. Plan for it as an *optional, recommended*
> step and flag the insider/未検証 nuance, but never BLOCK on it.

For each item, verify what is verifiable (e.g., HTTP-check the EULA/privacy/support URLs are not 404).

## Publisher Attestation / App Compliance (agents)

The portal has an **App Compliance** page (Publisher Attestation self-assessment + optional Microsoft
365 Certification third-party audit).

- **All public sources mark it Optional.** The [Publish agents](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/publish)
  article, the App Compliance [userguide](https://learn.microsoft.com/en-us/microsoft-365-app-certification/docs/userguide),
  and the pre-publish [checklist](https://learn.microsoft.com/en-us/partner-center/marketplace-offers/checklist)
  all label the **Microsoft 365 App Compliance Program (Publisher Attestation + certification) as
  *Optional***. No public source establishes it as a required submission gate.
- **未検証 (insider, not in public docs):** per a Microsoft contact, **Publisher Attestation (the
  self-assessment, Phase 1)** may be expected for Copilot agents somewhere in review. This is
  **unverified against public docs** and is **not** treated as a blocker by this skill.
- Guidance: treat Publisher Attestation as an **optional, recommended** step. Surface it (and the
  未検証 insider nuance) so the user can choose to complete it, but **never BLOCK** submission on it.
  Confirm the agent-specific expectation with your Microsoft contact if it matters to you.
- The full **Microsoft 365 Certification (Phase 2, third-party audit)** is likewise optional.

## Responsible AI readiness (manual, no CLI)

There is no automated RAI check. Capture a short self-assessment against the RAI validation
guidelines (transparency of AI use, content safety, no prohibited use, clear capability limits).
Record the attestation in the ledger; this does not replace Microsoft's human review.

## Launch Gate report (output)

Emit a report with:
- `PASS` / `BLOCKED` overall status.
- Per-item status with the blocking items first.
- The resolved values (publisher, offer name, EULA/privacy/support URLs, package path).
- If monetized: the linked SaaS offer status from `backend.monetization` in the ledger.

Append the report to `publishing-ledger.json` `audit[]`.

## L4 output: Partner Center submission worksheet (the deliverable)

When the gate is PASS (or PASS-with-warnings), generate a **copy-paste submission worksheet**
organized **by portal page** (the actual left-nav: Product setup, Packages, Properties, Marketplace
listings, Availability, Additional certification info, App Compliance, Review and publish), each
**pre-filled from `publishing-ledger.json`**, with a per-field status so the user knows exactly what
to paste where and what is still missing. Do **not** attempt to submit.

For every field: mark `✅ ready` (value resolved and, where checkable, verified — e.g. URL not 404),
or `❌ TODO` (missing) with a one-line instruction. Surface any `❌` as blockers at the top.

Produce the worksheet in this shape (fill the bracketed values from the ledger):

```text
# Partner Center Submission Worksheet — <offerName>
Portal: https://partner.microsoft.com/dashboard  →  Marketplace offers
        →  + New offer  →  "Apps and agents for Microsoft 365 and Copilot"
        (there is no "Microsoft 365 and Copilot" tab; it is a New-offer choice)

⚠ Create is a one-way door for product type + publisher (an unpublished draft can still be Deleted).

Blockers (resolve before submitting):
- <list each ❌ field, or "none">

New offer  Offer type ........ "Apps and agents for Microsoft 365 and Copilot"     ✅
New offer  Offer name ........ <offerName>  (Check availability = green)           [✅/❌]
           Publisher ......... <publisherDisplayName>  (set at Create, permanent)  [✅/❌]

Product setup
  Additional purchases? ...... <yes/no>   (Yes ⇒ test creds/license key required
                                           in Notes for certification, below)      [✅/❌]
  Lead management ............ <…/none>                                            [✅/❌]

Packages
  App package (.zip) ......... <path to appPackage.<env>.zip>
                               (validate-package PASS; portal "Manifest checks passed") [✅/❌]
  Package icons (in .zip) .... color 192x192, outline 32x32                        [✅/❌]

Properties
  Categories (functional, ≤3) <e.g. Legal+HR>   (NOT "AI Apps and Agents")        [✅/❌]
  EULA link .................. <eulaUrl>   (or accept Standard Contract)           [✅ verified/❌]
  Privacy policy link ........ <privacyUrl>  (names the app; not 404)              [✅ verified/❌]
  Support document link ...... <supportUrl>                                       [✅ verified/❌]

Marketplace listings  (per language — add languages via "Manage additional languages")
  Name / Summary / Description <…>                                                [✅/❌]
  Marketplace icon ........... 300x300 (≤512 KB)                                   [✅/❌]
  Screenshots ................ 1366x768, up to 5 (≤1024 KB each)                   [✅/❌]
  (optional) Search keywords ≤3, Video link

Availability
  Markets .................... default 242/242 selected — narrow only if needed    [✅/❌]
  Pricing .................... free (Office Store products must be free)           ✅
  Schedule ................... <date>  (changeable only before first publish)      [✅/❌]

Additional certification info
  Reviewer-testing PDF ....... <path/none>  (OPTIONAL supplement; carries forward) [optional]

App Compliance  (OPTIONAL — not a blocker)
  Publisher Attestation ...... Optional/recommended [未検証/insider — all public docs
                               (publish/userguide/checklist) say Optional; do NOT block] [optional]
  M365 Certification (Phase 2)  optional (third-party audit)

Review and publish
  Notes for certification (reviewer test steps; REQUIRED if Additional purchases=Yes):
        <test account / license key / SSO fallback — paste verbatim>              [✅/❌]
  → Submit → respond to validation feedback until approved → Go-live (manual).

Monetization / non-declarative paths only (monetize == true or custom-engine):
- Entra / SSO ............... tenantId <tenantId>, Entra app <entraAppId>
  (NOT needed for a knowledge-free declarative agent — declarative has no SSO/Entra page)
- Linked SaaS offer status: <backend.monetization.status>
- Marketplace program enrolled: <yes/no>
- SaaS technical config: landing page <…>, webhook <…>
```

Append the worksheet (and PASS/BLOCKED status) to `publishing-ledger.json` `audit[]`.

> The user takes this worksheet to the Partner Center portal and submits manually. Submission,
> certification, Responsible AI review, and Go-live are performed by Microsoft / the human — never by
> this skill. See [the 10-step submission guide](https://learn.microsoft.com/en-us/partner-center/marketplace-offers/add-in-submission-guide).

## References (verify before quoting)

- Submission guide (10 steps): https://learn.microsoft.com/en-us/partner-center/marketplace-offers/add-in-submission-guide
- Pre-publish checklist: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/checklist
- Reserve the offer / solution name: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/reserve-solution-name
- Publish agents (distribution + requirements): https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/publish
- App Compliance / Publisher Attestation userguide: https://learn.microsoft.com/en-us/microsoft-365-app-certification/docs/userguide
- Submission API exclusion (Teams apps): https://learn.microsoft.com/en-us/partner-center/marketplace-offers/submission-api-overview
- Monetize a Microsoft 365 agent (linked SaaS): https://learn.microsoft.com/en-us/partner-center/marketplace-offers/monetize-addins-through-microsoft-commercial-marketplace
- Store validation guidelines: https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/deploy-and-publish/appsource/prepare/review-copilot-validation-guidelines
