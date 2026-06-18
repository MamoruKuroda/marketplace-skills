---
name: triage-agent-type
description: "Entry point. Determines persona, agent type, and monetization intent, then routes to the correct publishing path and records decisions in publishing-ledger.json."
argument-hint: "Describe your agent idea, who you are (startup/partner/Microsoft/maker), and whether you plan to charge for it."
user-invocable: true
last_updated: "2026-06-18"
---

# Triage: Agent Type & Publishing Path

Routes a user to the correct Microsoft 365 Copilot agent publishing path, on three
orthogonal axes, and writes the result to `publishing-ledger.json` for downstream skills.

> EXPERIMENTAL. This skill guides preparation up to a submission-ready package and
> checklist. It does not submit to Partner Center on your behalf, and never deploys
> Azure resources without explicit confirmation (delegated to `@git-ape`).

## Three decisions this skill makes

1. **persona** — shapes prerequisites, guidance depth, and which paths are surfaced.
2. **agent_type** — determines the build/scaffold path and whether an execution backend (A) is needed.
3. **monetize** — determines whether a monetization backend (B), a linked SaaS offer, is needed.

These are independent. `agent_type` decides (A); `monetize` decides (B). Both can be true.

## Interview flow

Ask the following in order. Stop early only when the answer makes later questions moot.

### Q1 — Persona (one question, light routing only)
"Which best describes you?"
- `startup-isv` (P1): startup building a product agent, pro-code, likely wants to monetize.
- `partner-si` (P2): partner/SI onboarding a customer's agent on their behalf.
- `microsoft` (P3): Microsoft employee guiding a partner (demo/education).
- `lowcode-maker` (P4): prefers a low-code/GUI experience.

Routing hint (not a hard gate):
- P4 → bias toward `copilot-studio`.
- P1/P2/P3 → bias toward Agents Toolkit (pro-code) paths.

### Q2 — Marketplace intent (gate)
"Do you want this agent in the **Microsoft Commercial Marketplace** (public, transactable),
or only inside your organization?"
- `marketplace` → continue.
- `org-only` → STOP and redirect: org catalog paths (Agent Builder / Copilot Studio share)
  do not reach the Commercial Marketplace. See references. Record and exit.

### Q3 — Build approach → agent_type
"Will the agent use Copilot's own model/orchestrator, or bring its own?"
- Uses Copilot's model + orchestrator, low/no custom runtime → `declarative`.
- Brings its own model/orchestrator/runtime (pro-code) → `custom-engine`.
- Built in a low-code studio with its own channels → `copilot-studio`.

Validation against references (Marketplace reachability):
- `declarative` via **Agents Toolkit** → reaches Marketplace. (Agent Builder does NOT.)
- `custom-engine` via **Agents Toolkit** → reaches Marketplace.
- `copilot-studio` **multitenant custom** → reaches Marketplace (preview, via Partner Center).
If the user names a non-reaching builder (Agent Builder, Copilot Studio declarative,
SharePoint agent), explain the limitation and offer the nearest reaching alternative.

### Q4 — Monetization → monetize
"Do you plan to charge customers for this agent?"
- `yes` → a **linked SaaS offer** backend (B) is required: Entra multitenant app, plus a
  SaaS fulfillment landing page + connection webhook backed by a subscription-state store
  (required); entitlement and metering are optional. Requires enrolling in BOTH the
  M365 & Copilot program and the Microsoft Marketplace program.
- `no` → free download; only the M365 & Copilot program is needed.

### Tenant context — NOT collected here (collected just-in-time downstream)

Triage asks only what routing needs: **persona, marketplace intent, agent_type, monetize** (Q1–Q4).
It does **not** ask for tenant ID, publisher name, or offer name — those are not needed to route, and
asking for them up front is confusing.

Initialize the ledger's `tenant` fields as empty/placeholder. Each downstream skill that actually
needs a value collects it just-in-time and writes it to the ledger:
- `submit-readiness` → publisher display name, offer name (for the submission worksheet).
- `monetization-saas-offer` → target Entra tenant ID (multitenant Entra app registration).
- `backend-agent-runtime` / `@git-ape` → target subscription/tenant for deployment.

Never assume values; never store secrets.

## Routing table (agent_type x monetize)

| agent_type | monetize=no | monetize=yes |
| --- | --- | --- |
| declarative | path-declarative-atk | path-declarative-atk + monetization-saas-offer |
| custom-engine | path-custom-engine-atk (+ backend-agent-runtime) | path-custom-engine-atk + backend-agent-runtime + monetization-saas-offer |
| copilot-studio | path-copilot-studio | path-copilot-studio + monetization-saas-offer |

Backends:
- (A) backend-agent-runtime → only when agent_type == custom-engine.
- (B) monetization-saas-offer → only when monetize == yes (independent of agent_type).

## Deliverables (make the output tangible to the user)

1. **The ledger file** — write `publishing-ledger.json` to the current working directory, then tell
   the user explicitly: the **full path** where it was written, that it's the hand-off file for the
   next skill, and a short summary of its key fields (persona / agentType / monetize / route). Invite
   them to open it. Do not leave the deliverable invisible.
2. **Routing summary** — a short table/paragraph: which path skill runs next and why, and whether
   execution backend (A) / monetization backend (B) are needed.
3. **Next action (be explicit)** — tell the user the exact next command to run, namespaced for the
   client. In Copilot CLI that is `/agent-publishing:<next-skill>` (plugin skills are namespaced as
   `/<plugin-name>:<skill-name>`). For example, for a declarative agent:
   `/agent-publishing:path-declarative-atk`.
4. **Prerequisites** — what to confirm before the next skill (persona-dependent), with any `<TBD>`
   ledger values flagged so the user knows what's still needed.

## publishing-ledger.json (schema)

```json
{
  "schemaVersion": "0.1.0",
  "createdAt": "<ISO-8601>",
  "persona": "startup-isv | partner-si | microsoft | lowcode-maker",
  "marketplaceIntent": "marketplace | org-only",
  "agentType": "declarative | custom-engine | copilot-studio",
  "monetize": true,
  "tenant": { "tenantId": "<guid or '<TBD>'>", "publisherDisplayName": "", "offerName": "" },
  "route": {
    "pathSkill": "path-declarative-atk | path-custom-engine-atk | path-copilot-studio",
    "needsExecutionBackend": false,
    "needsMonetizationBackend": true
  },
  "backend": {
    "execution": { "status": "not-started", "resourceGroup": null, "endpoint": null },
    "monetization": { "status": "not-started", "resourceGroup": null, "fulfillmentEndpoint": null, "entraAppId": null }
  },
  "programs": { "m365AndCopilot": "required", "microsoftMarketplace": "required-if-monetize" },
  "audit": []
}
```

Downstream skills MUST read this ledger first, reuse `backend.*.resourceGroup` to avoid
duplicate provisioning, and append an entry to `audit` for every state change.

## References (authoritative; verify before quoting)

- Submission flow: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/add-in-submission-guide
- Distribution matrix: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/publish
- Agent types (declarative vs custom engine): https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agents-overview
- Monetization (linked SaaS offer): https://learn.microsoft.com/en-us/partner-center/marketplace-offers/artificial-intelligence-app-agent-publish-release
- Monetize a Microsoft 365 agent: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/monetize-addins-through-microsoft-commercial-marketplace
