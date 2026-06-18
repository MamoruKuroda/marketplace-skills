---
name: path-custom-engine-atk
description: "Scaffolds, provisions, deploys, validates, and packages a custom engine Microsoft 365 Copilot agent with the Agents Toolkit CLI (atk). Routed to when agentType == custom-engine. Delegates the agent's Azure runtime to backend-agent-runtime."
argument-hint: "App name, language, model/orchestrator choice, hosting target. Reads publishing-ledger.json."
user-invocable: true
last_updated: "2026-06-13"
---

# Path: Custom Engine Agent (Microsoft 365 Agents Toolkit)

For agents that bring their own model and orchestrator (pro-code). Produces a submission-ready app
package AND a deployed Azure runtime (the execution backend, A).

> Precondition: `publishing-ledger.json` with `agentType == "custom-engine"`.
> This skill orchestrates `backend-agent-runtime` (A) and, if `monetize == true`,
> `monetization-saas-offer` (B). It never submits to Partner Center.

## Prerequisites

- Node.js, `atk` CLI (`@microsoft/m365agentstoolkit-cli` v1.1.x+), `atk doctor` passing.
- Azure subscription + a service principal for headless provisioning (CI) or `az login`.
- Decision: model/orchestrator (e.g., Microsoft 365 Agents SDK) and hosting (App Service / Functions / Bot).

### Account guard (M365 + Azure)

Do not assume any account is "already signed in," and never trigger a silent sign-in. Before steps
needing auth: for **M365** (`atk install`/sideload, `atk publish`) run `atk auth list` and **confirm
with the user which account/tenant to use** (avoid an accidental corporate/WAM identity); for
**Azure** (`atk provision`/`atk deploy`) confirm the target subscription/tenant. Sign-in-free steps
(`atk new`, `atk package`, `atk validate --validate-method validation-rules`) need no prompt.

## Pipeline

### 1. Scaffold
```bash
atk new \
  --capability basic-custom-engine-agent \
  --app-name <appName> \
  --programming-language typescript \
  --folder <outDir> \
  --interactive false
```
- `basic-custom-engine-agent` scaffolds a bot-backed agent (custom runtime code).
- `atk list templates` shows other custom-engine samples (e.g., `weather-agent`).

### 2. Author the agent runtime
Implement orchestrator/model logic and the bot endpoint in the scaffolded project.
The Microsoft 365 app manifest declares the bot/endpoint that the runtime serves.

### 3. Provision + deploy the execution backend (delegate to `backend-agent-runtime`)
`backend-agent-runtime` (A) runs:
```bash
atk auth login azure --service-principal true --username <CLIENT_ID> --tenant <TENANT_ID> --password <cert.pem|secret> --interactive false
atk provision --env <env>            # Bicep: App Service, Bot registration, Entra app, etc.
atk deploy --env <env> --interactive false
```
It writes `backend.execution` (resourceGroup, endpoint) to the ledger and wires the endpoint into
the manifest. For richer/custom Azure topologies, it can delegate to `@git-ape`.

### 4. Validate (delegate to `validate-package`)
```bash
atk validate --manifest-file ./appPackage/manifest.json --validate-method validation-rules
atk validate --package-file ./appPackage/build/appPackage.<env>.zip --validate-method test-cases
```

### 5. Package
```bash
atk package --env <env>   # -> ./appPackage/build/appPackage.<env>.zip
```

## Orchestration / next skills

1. `backend-agent-runtime` (A) — always, before packaging the final manifest.
2. if `monetize == true` -> `monetization-saas-offer` (B). Reuse `backend.execution.resourceGroup`
   from the ledger to avoid duplicate RG/Entra/Key Vault provisioning.
3. always -> `submit-readiness`.

## Outputs / ledger updates

- Deployed runtime endpoint + validated `appPackage.<env>.zip`.
- `route.pathSkill = "path-custom-engine-atk"`, `route.needsExecutionBackend = true`.
- `audit[]`: scaffold/provision/deploy/validate/package entries.

## References (verify before quoting)

- atk CLI (new/provision/deploy/validate/package): https://learn.microsoft.com/en-us/microsoftteams/platform/toolkit/teams-toolkit-cli
- CI/CD (Azure SP auth, GitHub Actions): https://learn.microsoft.com/en-us/microsoftteams/platform/toolkit/use-cicd-template
- Agents overview (custom engine): https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agents-overview
- Custom engine agent UX requirements: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/publish
