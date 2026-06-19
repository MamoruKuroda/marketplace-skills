# partner-center-onboarding

> 日本語版は [README.ja.md](README.ja.md) を参照してください。

> **EXPERIMENTAL.** Guidance only.This plugin **never** signs in to Partner Center, assigns
> roles, edits Microsoft Entra, or submits anything on your behalf — every portal action is
> performed by you. It never asks for or stores passwords, verification codes, or secrets.

A skill set that gets ISVs and partners **unstuck on Microsoft Partner Center account
verification** when publishing a **Microsoft 365 Copilot agent** to the **Microsoft Commercial
Marketplace**.

## Why this exists

Account verification — not the agent build — is where partners most often stall: sign-in and
role confusion, tenant/App-ID mismatches, publisher/business-existence evidence, and "what stage
am I at?" anxiety. These were distilled from real partner support threads (Teams + Slack) and
collapsed into a single goal state.

## Design: converge from the endpoint

There is **one** goal — *a verified, publish-ready Partner Center account* — defined by four
conditions:

| # | Condition | Done when |
| --- | --- | --- |
| 1 | **Identity & roles** | Right person signs in with a role that can publish/manage users |
| 2 | **Legal entity & publisher identity** | Microsoft App ID = Entra app (client) ID; publisher legal info consistent; tenant equality with Partner Center **not** required (publisher-verification badge = app tenant associated with the Partner Global Account) |
| 3 | **Business existence** | Business/employment verification done; enrolled in Microsoft 365 & Copilot program; Partner One ID (MAICPP, formerly MPN) and primary contact present |
| 4 | **Process visibility** | Knows the save→publish→submit order, the 4–6 week timeline, and how to escalate (Support Request) |

The four common failure classes are **triage axes into the same answer**, not separate
destinations. One question routes the user to the blocking condition.

## Skills

| Skill | Purpose |
| --- | --- |
| [`troubleshoot-account-verification`](skills/troubleshoot-account-verification) | Diagnose the blocking condition and emit a status checklist, a next action, and `verification-ledger.json` |

## Relationship to `agent-publishing`

`agent-publishing` decides **what to build and how to submit** (agent type / monetization /
submission worksheet). `partner-center-onboarding` handles the **orthogonal** problem of getting
the **account itself verified** so you *can* submit. Use this when verification — not the build —
is the blocker.

## Portability (CLI + Cowork)

Skills here are portable **Agent Skills** (`SKILL.md`, the open standard). They run as-is in
**GitHub Copilot CLI**, and the `skills/` folder can be packaged into a Microsoft 365 app package
(`.zip` with `manifest.json` + icons) for **Microsoft 365 Copilot Cowork**
([packaging guide](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development)).
They avoid slash-only invocation and sub-agents (not yet supported in Cowork) and rely on
natural-language triggers.

## Install

```bash
copilot plugin marketplace add MamoruKuroda/marketplace-skills
copilot plugin install partner-center-onboarding@marketplace-skills
```

## References (verify before quoting — labels drift)

- Partner Center roles & permissions: https://learn.microsoft.com/en-us/partner-center/account-settings/permissions-overview
- Distribution options: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/publish
- App submission guide: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/add-in-submission-guide
- Open a developer account: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/open-a-developer-account
- Cowork plugin development: https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development

## License

Dual-licensed: **MIT** for code/configuration and **CC-BY-4.0** for documentation/content.
Copyright Mamoru Kuroda.
