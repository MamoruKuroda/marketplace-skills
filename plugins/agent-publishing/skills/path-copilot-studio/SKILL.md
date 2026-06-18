---
name: path-copilot-studio
description: "Guides publishing a multitenant custom agent built with Copilot Studio to the Microsoft 365 Copilot and Teams channel and, via Partner Center, to the Microsoft Commercial Marketplace (preview). Mostly GUI; this skill guides and gates rather than automates."
argument-hint: "Copilot Studio agent details, target audience, monetization intent. Reads publishing-ledger.json."
user-invocable: true
last_updated: "2026-06-13"
---

# Path: Copilot Studio Multitenant Custom Agent

For agents built in Copilot Studio (low-code). Only **multitenant custom** Copilot Studio agents can
reach the Commercial Marketplace (via Partner Center, preview). Copilot Studio *declarative* agents
and org-share only reach the org catalog and are out of scope here.

> Precondition: `publishing-ledger.json` with `agentType == "copilot-studio"`.
> Copilot Studio authoring/publishing is largely a GUI flow — this skill provides ordered guidance
> and a readiness gate, not full automation.

## Reachability check (gate)

- Multitenant **custom** agent → can be made available in Teams / Microsoft 365 Copilot and
  submitted to the Commercial Marketplace via Partner Center (preview). Continue.
- Declarative / single-tenant / share-only → BLOCK for Marketplace; redirect to org catalog guidance.

## Guided steps (GUI)

1. In Copilot Studio, finish and **publish** the agent.
2. Configure the agent as **multitenant** and add the **Microsoft 365 Copilot and Teams channel**.
3. Set **availability options** (share with users/groups, or submit to org catalog by an admin).
4. For Marketplace: follow the "make your multitenant agent available in Teams or Microsoft 365
   Copilot (preview)" flow, then create the offer in Partner Center.

## Monetization

If `monetize == true`, run `monetization-saas-offer` (B) to stand up the linked SaaS offer backend,
then link it to the offer in Partner Center. Same Marketplace-program enrollment requirement applies.

## What is NOT automated

- Copilot Studio authoring and channel configuration (portal).
- Partner Center offer creation, listing, and submission (portal + human review).
- Any Azure backend is only needed for monetization (B), not for the agent runtime itself.

## Outputs / ledger updates

- `route.pathSkill = "path-copilot-studio"`, `route.needsExecutionBackend = false`.
- A readiness summary + the ordered manual steps.
- Hand off to `submit-readiness` for the final gate and Partner Center steps.

## References (verify before quoting)

- Distribution matrix (Copilot Studio rows): https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/publish
- Make a multitenant agent available (Teams / M365 Copilot, preview): https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams
- Submission guide: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/add-in-submission-guide
