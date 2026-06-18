---
name: backend-agent-runtime
description: "(Backend A) Provisions and deploys the custom engine agent's own Azure runtime via atk provision/deploy, optionally delegating richer topologies to @git-ape. Invoked only when agentType == custom-engine."
argument-hint: "Hosting target, env name, Azure service principal. Reads/writes publishing-ledger.json backend.execution."
user-invocable: true
last_updated: "2026-06-13"
---

# Backend A: Agent Runtime (Custom Engine only)

Stands up the compute that runs a custom engine agent's orchestrator/model and bot endpoint.
This is the agent's *execution* plane — distinct from the *monetization* plane in
`monetization-saas-offer` (B).

> When this runs: `agentType == "custom-engine"` only. Skipped for declarative and copilot-studio
> (declarative agents run on Copilot's own model/orchestrator and need no runtime).
> Never deploys without explicit user confirmation (delegated deploys go through `@git-ape`'s gate).

## Inputs (from ledger / triage)

- `tenant.tenantId`, target Azure subscription, env name.
- Azure service principal (CI) or interactive `az`/`atk auth login azure`.
- Hosting target (App Service / Functions / Azure Bot Service).

## Provision + deploy (automatable)

```bash
# Headless Azure auth (CI):
atk auth login azure \
  --service-principal true \
  --username <CLIENT_ID> --tenant <TENANT_ID> \
  --password ./cert.pem --interactive false

# Create Azure resources (Bicep in m365agents.yml: App Service, Bot, Entra app, ...):
atk provision --env <env> --ignore-env-file

# Deploy runtime code:
atk deploy --env <env> --interactive false
```

## When to delegate to @git-ape

Use `atk provision/deploy` for the toolkit's standard Bicep topology. Delegate to `@git-ape` when
the runtime needs resources or controls beyond the template — e.g., private networking, custom
data stores, security gates, cost estimation, or WAF review. `@git-ape` enforces its security gate
and saves the deployment under `.azure/deployments/`.

## Shared-resources contract

If `monetization-saas-offer` (B) will also run, this skill provisions first and records
`backend.execution.resourceGroup`, the Entra tenant, and any Key Vault. (B) MUST reuse these
rather than creating duplicates. Coordinate via `publishing-ledger.json`.

## Outputs / ledger updates

- `backend.execution`: `{ status, resourceGroup, endpoint }` populated.
- The runtime endpoint wired into the Microsoft 365 app manifest (bot/endpoint).
- `audit[]`: provision/deploy entries with timestamps.

## References (verify before quoting)

- atk provision/deploy + Azure SP auth: https://learn.microsoft.com/en-us/microsoftteams/platform/toolkit/teams-toolkit-cli
- CI/CD templates: https://learn.microsoft.com/en-us/microsoftteams/platform/toolkit/use-cicd-template
- Git-Ape (delegated Azure deploy): https://azure.github.io/git-ape/
