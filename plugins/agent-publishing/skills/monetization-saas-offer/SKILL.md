---
name: monetization-saas-offer
description: "(Backend B) Provisions the linked SaaS offer transaction plane that monetizes a Microsoft 365 Copilot agent: Entra multitenant app, SaaS fulfillment endpoint + landing page, licensing/entitlement DB, and optional metering. Self-contained, grounded in Microsoft Learn; delegates the actual Azure deployment to @git-ape. Invoked only when monetize == true."
argument-hint: "Pricing model (entitlement/usage), license management (publisher/Microsoft), env. Reads/writes publishing-ledger.json backend.monetization."
user-invocable: false
last_updated: "2026-06-13"
---

# Backend B: Monetization via Linked SaaS Offer

Microsoft 365 / Copilot agents are free to download and monetized through a **linked SaaS offer**.
This skill provisions that SaaS transaction plane. It is independent of agent type — it runs for a
monetized declarative OR custom engine OR Copilot Studio agent.

> When this runs: `monetize == true`. Requires enrollment in BOTH the Microsoft 365 and Copilot
> program (publish the agent) and the Microsoft Marketplace program (monetize). Never deploys
> without explicit confirmation; the actual Azure provisioning is delegated to `@git-ape`.

## Collect tenant context (just-in-time)

Triage does not collect tenant info. Read `publishing-ledger.json` `tenant.tenantId`; if it's empty
or `<TBD>`, ask the user for the target Entra tenant ID now (needed for the multitenant Entra app
registration and the `@git-ape` deployment target) and write it back to the ledger. Never assume;
never store secrets.

## What a linked SaaS offer requires

1. **Multitenant Microsoft Entra ID app registration** (SSO, "any org directory").
2. **SaaS fulfillment API integration**: a landing page + a webhook endpoint that receives
   subscription lifecycle events (activate / change-plan / change-quantity / suspend / unsubscribe).
3. **Licensing / entitlement store** (publisher-managed) OR choose **Microsoft-managed licenses**.
4. **Metering** emission (only for usage-based pricing).
5. WAF 5-pillar baseline: tenant isolation, IaC, Key Vault, CI/CD, encryption, compliance.

## Pricing models (record the choice)

- Entitlement-based: per-user or flat-rate.
- Usage-based: metered dimensions.
- Combination.

## Build steps (self-contained; actual Azure deploy delegated to @git-ape)

Provision the following yourself, grounded in the Microsoft Learn references below. Hand the
infrastructure-as-code deployment to `@git-ape` (security gate, cost estimate, audit trail). Do not
depend on any third-party skill set for the SaaS plumbing.

1. **Multitenant Entra ID app registration** — register an app with "any org directory" sign-in for
   SSO and the SaaS fulfillment token exchange.
2. **Landing page + fulfillment webhook** — stand up the landing page (token resolution) and the
   webhook endpoint that receives subscription lifecycle events. Wire it to the SaaS fulfillment APIs.
3. **Licensing / entitlement store** — choose publisher-managed (your own DB) or Microsoft-managed
   licenses, and provision the store accordingly.
4. **Metering** — only for usage-based pricing: emit usage events to the Marketplace metering service.
5. **WAF baseline** — tenant isolation, IaC, Key Vault, CI/CD, encryption, compliance.

| Capability | How |
| --- | --- |
| Multitenant SaaS baseline / landing zone | Author IaC (ARM/Bicep) and deploy via `@git-ape` |
| **SaaS fulfillment API + metering** | Implement against the SaaS fulfillment APIs (see references); deploy via `@git-ape` |
| Tenant isolation model | Decide per WAF guidance; encode in IaC |
| IaC deploy (App Service / DB / Key Vault / Entra) | `@git-ape` (security gate, cost estimate, audit) |
| Offer-type / pricing decisions | Use the Partner Center references below |

This skill owns the decisions and the Partner Center technical-config values; `@git-ape` performs
the Azure deployment.

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

## References (verify before quoting)

- Monetize a Microsoft 365 agent (linked SaaS): https://learn.microsoft.com/en-us/partner-center/marketplace-offers/monetize-addins-through-microsoft-commercial-marketplace
- AI app/agent publish & monetization models: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/artificial-intelligence-app-agent-publish-release
- SaaS fulfillment APIs: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/pc-saas-fulfillment-apis
- SaaS offer technical configuration: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/create-new-saas-offer-technical
- Startups guide (SaaS agent on Marketplace): https://learn.microsoft.com/en-us/startups/build/ai/agents/intro-marketplace-agents
- Git-Ape (delegated Azure deployment): https://azure.github.io/git-ape/
