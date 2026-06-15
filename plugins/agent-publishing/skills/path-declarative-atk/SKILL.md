---
name: path-declarative-atk
description: "Scaffolds, validates, and packages a declarative Microsoft 365 Copilot agent with the Microsoft 365 Agents Toolkit CLI (atk), producing a submission-ready app package. Routed to when agentType == declarative."
argument-hint: "App name, programming language, knowledge sources and actions. Reads publishing-ledger.json from triage."
user-invocable: false
last_updated: "2026-06-13"
---

# Path: Declarative Agent (Microsoft 365 Agents Toolkit)

Takes a triaged declarative-agent intent and produces a validated, packaged Microsoft 365
app package (`.zip`) that is ready for the manual Partner Center submission.

> Precondition: `publishing-ledger.json` exists with `agentType == "declarative"`.
> If `monetize == true`, this skill hands off to `monetization-saas-offer` after packaging.
> This skill never submits to Partner Center (no API exists — see `submit-readiness`).

## Prerequisites

- Node.js >= 18 (Toolkit requires Node; CI templates use 20.x).
- `atk` CLI: `npm install -g @microsoft/m365agentstoolkit-cli` (v1.1.x+; verify with `atk -v`).
- `atk doctor` passes.
- A Microsoft 365 tenant with sideloading enabled (for local test/install).

## Pipeline (all CLI steps are automatable)

### 1. Scaffold
```bash
atk new \
  --capability declarative-agent \
  --app-name <appName> \
  --programming-language typescript \
  --folder <outDir> \
  --interactive false
```
- `--capability declarative-agent` selects the pure declarative template (instructions + knowledge
  + actions over Copilot's own model/orchestrator; no custom runtime).
- Use `atk list templates` to confirm available capabilities for the installed version.

### 2. Author the agent
Edit the scaffolded files (do not invent paths — read what `atk new` generated):
- The declarative agent manifest (instructions, conversation starters, knowledge scopes).
- The Microsoft 365 app manifest (`manifest.json`) + `color.png` (192x192) + `outline.png` (32x32).
- For actions, add an API plugin: `atk add action` (and `atk add auth-config` if the API needs auth).

> Note: API plugins are supported as actions within declarative agents.

### 3. Validate (delegate to `validate-package`)
Run the shared `validate-package` skill, which executes (note: `--env` is required to resolve
manifest `${{...}}` placeholders):
```bash
atk validate --env <env> --manifest-file ./appPackage/manifest.json --validate-method validation-rules
atk validate --env <env> --package-file ./appPackage/build/appPackage.<env>.zip --validate-method test-cases
```
`validation-rules` = schema + rules; `test-cases` = mirrors Teams Store automated validation.

### 4. Package
```bash
atk package --env <env>
# output: ./appPackage/build/appPackage.<env>.zip
```

### 5. Local install (optional, for the user to test)
```bash
atk install --file-path ./appPackage/build/appPackage.<env>.zip
```

## Outputs / ledger updates

- A validated `appPackage.<env>.zip`.
- Append to `publishing-ledger.json`:
  - `route.pathSkill = "path-declarative-atk"`, `route.needsExecutionBackend = false`.
  - `audit[]`: scaffold/validate/package results with timestamps and the package path.
- Next skill:
  - if `monetize == true` -> `monetization-saas-offer`
  - then always -> `submit-readiness`

## Boundaries

- No execution backend (A) is provisioned for declarative agents — they run on Copilot's model
  and orchestrator. (Only `path-custom-engine-atk` provisions a runtime.)
- Marketplace submission is manual; this skill stops at a submission-ready package.

## References (verify before quoting)

- atk CLI command reference: https://learn.microsoft.com/en-us/microsoftteams/platform/toolkit/teams-toolkit-cli
- App package anatomy: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agents-are-apps
- Declarative agents overview: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agents-overview
- CI/CD templates: https://learn.microsoft.com/en-us/microsoftteams/platform/toolkit/use-cicd-template
