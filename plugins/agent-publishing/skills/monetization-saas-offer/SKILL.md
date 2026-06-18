---
name: monetization-saas-offer
description: "(Backend B) Provisions the linked SaaS offer transaction plane that monetizes a Microsoft 365 Copilot agent: Entra multitenant app, SaaS fulfillment landing page + connection webhook, subscription-state store, entitlement, and optional metering. Self-contained, grounded in Microsoft Learn; delegates the actual Azure deployment to @git-ape. Invoked only when monetize == true."
argument-hint: "Pricing model (flat rate / per user; metering optional, flat rate only), license management (publisher / Microsoft), env. Reads/writes publishing-ledger.json backend.monetization."
user-invocable: true
last_updated: "2026-06-19"
---

# Backend B: Monetization via Linked SaaS Offer

Microsoft 365 / Copilot agents are free to download and monetized through a **linked SaaS offer**.
This skill provisions that SaaS transaction plane. It is independent of agent type — it runs for a
monetized declarative OR custom engine OR Copilot Studio agent.

> When this runs: `monetize == true`. Requires enrollment in BOTH the Microsoft 365 and Copilot
> program (publish the agent) and the Microsoft Marketplace program (monetize). Never deploys
> without explicit confirmation; the actual Azure provisioning is delegated to `@git-ape`.

A **transactable** offer ("Sell through Microsoft") is one in which **Microsoft facilitates the
exchange of money for a software license on the publisher's behalf**, and Microsoft bills using the
pricing model the publisher chose. ([plan-saas-offer], [plans-pricing]) Integrating with the SaaS
Fulfillment APIs is a hard requirement for creating a transactable SaaS offer. ([pc-saas-fulfillment-apis])

These three layers are **physically separated** below because they are different planes. Do not mix
them: a fact from one layer must never be stated as if it belonged to another.

| Layer | What it is | Lives in |
| --- | --- | --- |
| 1. Fulfillment (technical) | Keep subscription state in sync with Microsoft | Code: landing page + connection webhook + Fulfillment/Operations API v2 |
| 2. Pricing / Licensing (commercial) | offer → plan → pricing model; who manages licenses | Partner Center config + publisher entitlement logic |
| 3. Tax / Payment (money) | payout, withholding, W-8 / W-9 | **Partner Center only** — never in code or DB |

## Collect tenant context (just-in-time)

Triage does not collect tenant info. Read `publishing-ledger.json` `tenant.tenantId`; if it's empty
or `<TBD>`, ask the user for the target Entra tenant ID now (needed for the multitenant Entra app
registration and the `@git-ape` deployment target) and write it back to the ledger. Never assume;
never store secrets.

---

## Layer 1 — Fulfillment (technical)

Purpose: **keep the subscription state Microsoft holds in sync with the publisher's state.** Because
the goal is state synchronization, **persisting subscription state is mandatory** — this layer is not
"stateless because it's minimal."

**Canonical components** (use these terms, from the page headings):

1. **Multitenant Microsoft Entra ID app** for landing-page SSO. The landing page must support SSO with
   the multitenant Entra app and allow both work/school and personal Microsoft accounts. ([plan-saas-offer], [pc-saas-fulfillment-life-cycle])
2. **Landing page**: the URL Microsoft opens (with a purchase-identification token) after purchase. The
   publisher exchanges that token via the **Resolve API**, then calls the **Activate API** to start the
   billing cycle. Must be up **24/7**; must not contain `#` or secrets/tokens. ([create-new-saas-offer-technical], [pc-saas-fulfillment-life-cycle])
3. **Connection webhook**: HTTP endpoint Microsoft POSTs asynchronous events to
   (`Subscribe`, `ChangePlan`, `ChangeQuantity`, `Renew`, `Suspend`, `Unsubscribe`, `Reinstate`). ([pc-saas-fulfillment-webhook])
4. **Fulfillment Subscription API v2 + Operations API v2** (v1 is deprecated). These are **only** called
   from the publisher's backend service; service-to-service auth only — never from the web page. ([pc-saas-fulfillment-apis])

**Subscription lifecycle states** the state store must track:
`PendingFulfillmentStart` → `Subscribed` (Active, billing on) → being updated → `Suspended` →
`Unsubscribed`. With **auto activation** on, the subscription skips `PendingFulfillmentStart` and goes
straight to `Subscribed` at purchase (no Resolve/Activate call; a `Subscribe` webhook is sent instead).
The publisher has 30 days to resolve a `PendingFulfillmentStart` asset or it is voided. ([pc-saas-fulfillment-life-cycle], [create-new-saas-offer-plans])

**Webhook hard requirements** (all mandatory):

- Acknowledge every event with **HTTP 200**. ([pc-saas-fulfillment-webhook])
- For `ChangePlan` / `ChangeQuantity`, PATCH the operation status (success/failure) via the Operations
  API **within 10 seconds**; if no reply arrives in that window the change is **auto-accepted as
  Success**. ([pc-saas-fulfillment-webhook], [pc-saas-fulfillment-life-cycle])
- **Validate the Microsoft Entra token (JWT bearer)** from the request header, and call the Get
  Operation API to validate/authorize the payload before acting. ([pc-saas-fulfillment-webhook])
- Endpoint up **24 x 7** (Microsoft retries 500 times over 8 hours, then the operation fails). ([pc-saas-fulfillment-webhook])
- Do not strictly deserialize the payload — Microsoft may extend the schema. ([pc-saas-fulfillment-webhook])

> No pricing, payout, withholding, or tax logic belongs in this layer.

---

## Layer 2 — Pricing / Licensing (commercial)

The commercial hierarchy is **offer → plan → pricing model**. A **plan** (sometimes called a **SKU**)
defines scope, markets, and pricing; an offer must have at least one plan. ([plans-pricing], [create-new-saas-offer-plans])

**Pricing model — exactly two choices for SaaS:** **flat rate** or **per user**.
([plan-saas-offer], [plans-pricing])

- **One offer = one pricing model.** All plans in an offer share the same model; you cannot mix a flat
  rate plan and a per-user plan in the same offer. The choice is locked after publishing. ([plans-pricing], [saas-metered-billing])
- **Metering is not a third model.** It is an **optional extension of the flat rate model only**:
  flat-rate plans may add custom dimensions (e.g., emails, bandwidth) billed on consumption above the
  base fee. **Metering is unavailable on the per-user model.** ([plans-pricing], [saas-metered-billing])

**License management** is a **separate axis** from pricing (do not conflate with tax):

- **Publisher-managed** entitlement: the publisher maps each subscription to user access in its own
  store/logic.
- **Microsoft License Management Service**: the publisher integrates with Graph API to verify customer
  eligibility so customers manage licenses in the Microsoft Admin Center. ([plan-saas-offer])

> No payout, withholding, or W-8/W-9 logic belongs in this layer. License management ≠ tax.

---

## Layer 3 — Tax / Payment (money)

This layer is **Partner Center configuration and Microsoft's financial process only**. It must **never
appear in code or in the database** this skill provisions.

- Microsoft Marketplace runs an **agency model**: the publisher sets prices, Microsoft bills the
  customer, pays the publisher, and withholds an agency fee. ([plans-pricing])
- Payouts are generally **monthly**; payment is issued by **Microsoft Corporation (a US entity)**. ([payout-policy-details])
- To determine any applicable **withholding**, the publisher submits **Forms W-8 / W-9** in Partner
  Center. ([payout-policy-details])
- Markets can be filtered to **"Tax Remitted"** countries/regions, where Microsoft remits sales/use tax
  on the publisher's behalf — this is a Partner Center market setting, not application logic. ([plans-pricing], [create-new-saas-offer-plans])

> This skill writes no payout, tax, or withholding values to the ledger, code, or DB.

---

## Implementation tiers (what the backend builds)

Tiers are additive. They live in Layers 1–2; Layer 3 is never code.

- **Tier 1 — Fulfillment minimum (state table required).** Entra multitenant app + landing page +
  connection webhook + Subscription/Operations API v2, backed by a **subscription-state store** that
  tracks the lifecycle states above. Satisfies the transactable-offer requirement. ([pc-saas-fulfillment-apis], [pc-saas-fulfillment-life-cycle], [create-new-saas-offer-technical])
- **Tier 2 — Entitlement.** Publisher-managed mapping of subscription → user access, or integration
  with the Microsoft License Management Service via Graph API. ([plan-saas-offer])
- **Tier 3 — Metering (flat rate only).** Emit usage events via the Marketplace metering service API
  for custom dimensions. **Constraint: flat-rate plans only; never attach metering to a per-user plan.**
  Only emit usage above the base fee; one event per hour per dimension per resource (the SaaS
  `subscriptionId`); TLS 1.2; `api-version=2018-08-31`. ([saas-metered-billing], [marketplace-metering-service-apis])

WAF 5-pillar baseline still applies to the deployed backend: tenant isolation, IaC, Key Vault, CI/CD,
encryption, compliance.

## Build & delegation (self-contained; Azure deploy delegated to @git-ape)

Provision the Layer 1–2 artifacts yourself, grounded in the Microsoft Learn references below. Author
the infrastructure-as-code and hand the **deployment** to `@git-ape` (security gate, cost estimate,
audit trail). Do not depend on any third-party skill set for the SaaS plumbing.

| Capability | How |
| --- | --- |
| Multitenant SaaS baseline / landing zone | Author IaC (ARM/Bicep); deploy via `@git-ape` |
| SaaS fulfillment landing page + webhook + state store | Implement against the Fulfillment APIs v2 (Layer 1); deploy via `@git-ape` |
| Tenant isolation model | Decide per WAF guidance; encode in IaC |
| IaC deploy (App Service / DB / Key Vault / Entra) | `@git-ape` (security gate, cost estimate, audit) |
| Offer-type / pricing decisions | Use the Partner Center references (Layer 2) |

This skill owns the decisions and the Partner Center technical-config values; `@git-ape` performs the
Azure deployment.

## Shared-resources contract

If `backend-agent-runtime` (A) already ran (custom engine), reuse its
`backend.execution.resourceGroup`, Entra tenant, and Key Vault from the ledger. Do not create
duplicates. Record everything under `backend.monetization`.

## Outputs / ledger updates

- `backend.monetization`: `{ status, resourceGroup, fulfillmentEndpoint, entraAppId }`.
- The Partner Center SaaS offer technical configuration values (landing page URL, webhook URL,
  Entra app/tenant IDs) for the human to paste into the SaaS offer.
- `programs.microsoftMarketplace = "enrolled"` once confirmed.
- `audit[]`: provisioning entries.

## Boundary

This skill prepares the SaaS backend and its Partner Center technical-config values. Creating and
submitting the SaaS offer (and linking it to the agent) is done by the human in Partner Center.

> Preview note (2026-04): The **Product Ingestion API** (`https://graph.microsoft.com/rp/product-ingestion`)
> can configure and publish SaaS offers and the SaaS↔agent link declaratively, and now also covers the
> "AI Apps and Agents" category (in preview). However, publishing a change still goes through the
> standard validation/certification flow and a manual **Go-live**, so API value is essentially
> configure/draft automation — the review and go-live remain manual. This skill therefore keeps the
> portal flow as the primary path; treat API automation as an emerging preview option, not a substitute
> for certification.

## References (all fetched 2026-06-19, HTTP 200)

Primary sources for every claim above. The `[token]` matches the inline citations in the body.

Concepts / terminology:
- [plan-saas-offer]: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/plan-saas-offer
- [plans-pricing]: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/plans-pricing

Fulfillment layer:
- [pc-saas-fulfillment-apis]: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/pc-saas-fulfillment-apis
- [pc-saas-fulfillment-life-cycle]: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/pc-saas-fulfillment-life-cycle
- [pc-saas-fulfillment-webhook]: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/pc-saas-fulfillment-webhook
- [create-new-saas-offer-technical]: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/create-new-saas-offer-technical

Pricing / metering layer:
- [create-new-saas-offer-plans]: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/create-new-saas-offer-plans
- [saas-metered-billing]: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/saas-metered-billing
- [marketplace-metering-service-apis]: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/marketplace-metering-service-apis

Tax / payment layer:
- [payout-policy-details]: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/payout-policy-details

Delegated Azure deployment (not a Microsoft Learn source):
- Git-Ape: https://azure.github.io/git-ape/

Not re-verified this session (do not cite as confirmed until fetched):
- monetize-addins-through-microsoft-commercial-marketplace, artificial-intelligence-app-agent-publish-release, startups/build/ai/agents/intro-marketplace-agents — 未検証.
