# agent-publishing

> 日本語版は [README.ja.md](README.ja.md) を参照してください。

> **EXPERIMENTAL.** This is a guided-onboarding skill set, not a production product. It prepares
> a submission-ready package and checklist; it does not submit to Partner Center for you, and it
> never deploys Azure resources without explicit confirmation.

A [Git-Ape](https://github.com/Azure/git-ape) plugin that guides employees and partners through
publishing **Microsoft 365 Copilot agents** to the **Microsoft Commercial Marketplace**, with
optional monetization via a **linked SaaS offer**. The actual Azure deployment of any backend is
delegated to `@git-ape`.

## Scope

Three Marketplace-reaching agent paths:

1. **Declarative agent** (Microsoft 365 Agents Toolkit)
2. **Custom engine agent** (Microsoft 365 Agents Toolkit)
3. **Copilot Studio multitenant** custom agent

Out of scope (for now): Cowork plugins, Copilot connectors/plugins, org-catalog-only paths
(Agent Builder, Copilot Studio declarative, SharePoint agents).

## Two orthogonal decisions

- **agent_type** decides whether an **execution backend (A)** is needed (custom engine only).
- **monetize** decides whether a **monetization backend (B)** — the linked SaaS offer — is needed
  (independent of agent type).

## Personas (QuickStart)

| Persona | You are | Start with |
| --- | --- | --- |
| P1 startup-isv | pro-code startup, likely monetizing | `/triage-agent-type` → declarative/custom-engine + monetization |
| P2 partner-si | onboarding a customer's agent | `/triage-agent-type` → any path, governance-heavy |
| P3 microsoft | guiding a partner (demo/edu) | `/triage-agent-type` → any path |
| P4 lowcode-maker | low-code/GUI | `/triage-agent-type` → Copilot Studio |

## Install

First install Git-Ape (this plugin builds on it):

```bash
copilot plugin marketplace add Azure/git-ape
copilot plugin install git-ape@git-ape
```

Then, from the [`marketplace-skills`](https://github.com/MamoruKuroda/marketplace-skills) marketplace:

```bash
copilot plugin marketplace add MamoruKuroda/marketplace-skills
copilot plugin install agent-publishing@marketplace-skills
```

Or install this plugin directly:

```bash
copilot plugin install MamoruKuroda/marketplace-skills:plugins/agent-publishing
```

Verify, then start your first interview:

```text
copilot plugin list          # shows agent-publishing@marketplace-skills
copilot
> /triage-agent-type I'm a startup building a declarative HR policy agent and I want to charge for it.
```

## Skills

| Skill | Purpose |
| --- | --- |
| `triage-agent-type` | Entry point: persona + agent_type + monetize, routes and writes the ledger |
| `path-declarative-atk` | Scaffold/validate a declarative agent app package |
| `path-custom-engine-atk` | Scaffold a custom engine agent + (A) execution backend |
| `path-copilot-studio` | Guide Copilot Studio multitenant publishing |
| `backend-agent-runtime` | (A) Provision the agent's runtime (custom engine only) → `@git-ape` |
| `monetization-saas-offer` | (B) Provision the linked SaaS offer backend (self-contained) → deploy via `@git-ape` |
| `validate-package` | Local manifest / RAI / certification checks |
| `submit-readiness` | Program enrollment + blocking submission-readiness checklist |

> Status: all eight skills are in place. The declarative end-to-end path
> (`triage-agent-type` → `path-declarative-atk` → `validate-package` → `submit-readiness`) is the
> most exercised; `path-custom-engine-atk`, `backend-agent-runtime`, `monetization-saas-offer`, and
> `path-copilot-studio` are functional but less battle-tested.

## Example usage

```text
# Start here — triage decides persona, agent type, and monetization, then routes you:
@git-ape /triage-agent-type I'm a startup building a declarative HR policy agent and I want to charge for it.

# Run a specific path skill directly (advanced; normally triage routes you):
@git-ape /validate-package validate ./appPackage/manifest.json for env dev
@git-ape /submit-readiness check my offer is ready to submit to Partner Center
```

## End-to-end walkthrough (declarative agent, free)

1. `@git-ape /triage-agent-type ...` → records `agentType=declarative`, `monetize=false` in `publishing-ledger.json`, routes to `path-declarative-atk`.
2. `path-declarative-atk` scaffolds and packages:
   ```bash
   atk new --capability declarative-agent --app-name my-hr-agent --programming-language typescript --interactive false
   # author manifest + instructions + knowledge/actions
   atk package --env dev
   ```
3. `validate-package` gates the package (note: `--env` is required):
   ```bash
   atk validate --env dev --manifest-file ./appPackage/manifest.json --validate-method validation-rules
   atk validate --env dev --package-file ./appPackage/build/appPackage.dev.zip --validate-method test-cases
   ```
4. `submit-readiness` runs the blocking checklist (legal/privacy/test-instructions/RAI) and emits a Launch Gate report + the manual Partner Center steps.
5. **You** submit in the Partner Center portal and respond to review feedback.

## End-to-end walkthrough (declarative or custom engine, monetized)

Same as above, plus before `submit-readiness`:
- `monetization-saas-offer` provisions the **linked SaaS offer** backend (Entra multitenant app,
  SaaS fulfillment endpoint, licensing DB, optional metering) — defined in the skill itself and
  deployed via `@git-ape`. Requires enrolling in the **Microsoft Marketplace** program in addition
  to the **Microsoft 365 and Copilot** program.
- Custom engine agents additionally run `backend-agent-runtime` (`atk provision` / `atk deploy`)
  to stand up the agent's own runtime on Azure.

## What is automated vs manual

| Step | Automated (CLI) | Manual |
| --- | --- | --- |
| scaffold / validate / package | ✅ `atk new/validate/package` | |
| custom engine provision / deploy | ✅ `atk provision/deploy` | |
| org catalog submit | ✅ `atk publish` | admin approval in Teams Admin Center |
| **Marketplace submit + listing + review** | | ❌ Partner Center portal + human review |
| Responsible AI / certification | | ❌ human review, post-submission |

> Preview note (2026-04): the **Product Ingestion API** (`https://graph.microsoft.com/rp/product-ingestion`)
> added the "AI Apps and Agents" category and SaaS offer configuration in **preview**. Publishing still
> goes through standard certification and a manual Go-live, so API value is essentially configure/draft
> automation. These skills keep the portal flow as the primary path.

## Tenant safety

Skills never hardcode a tenant ID or secret. Tenant context is collected at triage time and stored
in `publishing-ledger.json` (no secrets). The ledger is per-user/per-workspace.

## References

- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/add-in-submission-guide
- https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/publish
- https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agents-overview
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/artificial-intelligence-app-agent-publish-release
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/monetize-addins-through-microsoft-commercial-marketplace

## License

Dual-licensed: **MIT** for code/configuration ([`LICENSE-CODE`](../../LICENSE-CODE)) and
**Creative Commons Attribution 4.0 (CC-BY-4.0)** for documentation/content ([`LICENSE`](../../LICENSE)).
Copyright Mamoru Kuroda.
