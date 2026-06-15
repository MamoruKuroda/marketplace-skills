---
name: submit-readiness
description: "Blocking pre-submission gate for Microsoft Commercial Marketplace. Verifies program enrollment, legal/privacy/test-instructions, and Responsible AI readiness, then emits a Launch Gate report and the exact manual Partner Center steps. Marketplace submission has no API and is always manual."
argument-hint: "Reads publishing-ledger.json. Needs publisher legal entity, privacy policy URL, EULA, support URL, and test credentials/instructions."
user-invocable: true
last_updated: "2026-06-13"
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

## Program enrollment (verify first)

| Program | When required | Purpose |
| --- | --- | --- |
| Microsoft 365 and Copilot program | always | publish the agent app package |
| Microsoft Marketplace program | if `monetize == true` | monetize via a linked SaaS offer |

If `monetize == true` and only the M365 & Copilot program is enrolled, BLOCK and instruct the user
to also enroll in the Marketplace program (and ensure `monetization-saas-offer` has run).

## Blocking checklist (top causes of ~80% of rejections)

Block submission and list every missing item:

1. Valid **Terms of Use** link (https, not 404).
2. Valid **Privacy Policy** link (separate from Terms; https, not 404; names the app/service).
3. **Reviewer test instructions** present (test account / license key / SSO fallback steps).
4. **Service/account disclosure** specified.
5. **Additional-purchase disclosure** (if a paid service is required) — disclosed in the listing description.
6. **App package validation PASS** (from `validate-package`: both validation-rules and test-cases).
7. **Icons** present and correct (color 192x192, outline 32x32).
8. **Responsible AI readiness** self-attestation (see below) — RAI is reviewed by humans post-submission; ensure the agent meets RAI validation expectations.

For each item, verify what is verifiable (e.g., HTTP-check the privacy/terms URLs are not 404).

## Responsible AI readiness (manual, no CLI)

There is no automated RAI check. Capture a short self-assessment against the RAI validation
guidelines (transparency of AI use, content safety, no prohibited use, clear capability limits).
Record the attestation in the ledger; this does not replace Microsoft's human review.

## Launch Gate report (output)

Emit a report with:
- `PASS` / `BLOCKED` overall status.
- Per-item status with the blocking items first.
- The resolved values (publisher, offer name, privacy/terms/support URLs, package path).
- If monetized: the linked SaaS offer status from `backend.monetization` in the ledger.

Append the report to `publishing-ledger.json` `audit[]`.

## Manual submission steps (guide only)

When the gate is PASS, present these portal steps (do not attempt to automate):
1. Sign in to Partner Center > Marketplace offers > **Microsoft 365 and Copilot**.
2. **+ New offer** > "Apps and agents for Microsoft 365 and Copilot".
3. Name the offer (match the manifest); associate the enrolled publisher.
4. Product setup (Entra/SSO, additional purchase, lead management as applicable).
5. **Packages**: upload the validated `appPackage.<env>.zip`.
6. Properties: categories (prefer "AI Apps and Agents"), industries.
7. Legal & support: Terms/EULA, Privacy Policy, Support docs links.
8. Marketplace listing per language; availability/markets.
9. **Certification notes**: paste reviewer test instructions (and a PDF if complex).
10. Review and publish; respond to validation feedback until approved (typically iterative).

## References (verify before quoting)

- Submission guide (10 steps): https://learn.microsoft.com/en-us/partner-center/marketplace-offers/add-in-submission-guide
- Distribution matrix: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/publish
- Submission API exclusion (Teams apps): https://learn.microsoft.com/en-us/partner-center/marketplace-offers/submission-api-overview
- Monetize a Microsoft 365 agent (linked SaaS): https://learn.microsoft.com/en-us/partner-center/marketplace-offers/monetize-addins-through-microsoft-commercial-marketplace
- Store validation guidelines: https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/deploy-and-publish/appsource/prepare/review-copilot-validation-guidelines
