---
name: validate-package
description: "Runs local validation of a Microsoft 365 agent app package using the Agents Toolkit CLI (schema/rules + Store test-cases). Shared by all Agents Toolkit paths. Does NOT perform Responsible AI or certification review (those are human, post-submission)."
argument-hint: "Path to manifest.json or a built app package zip, and the target env."
user-invocable: true
last_updated: "2026-06-13"
---

# Validate Package

Local, automatable validation of a Microsoft 365 Copilot agent app package before submission.
Shared by `path-declarative-atk` and `path-custom-engine-atk`.

## What this validates (and what it does not)

| Check | Tool | Covered here |
| --- | --- | --- |
| Manifest JSON schema + Teams/M365 validation rules | `atk validate --validate-method validation-rules` | ✅ |
| Pre-submission Store test cases (mirrors Teams Store automated suite) | `atk validate --validate-method test-cases` | ✅ |
| Responsible AI (RAI) policy review | Microsoft validators (human, post-submission) | ❌ — see `submit-readiness` for the manual checklist |
| Commercial marketplace certification policies | Microsoft validators (human) | ❌ |
| Functional / end-to-end testing | manual or custom harness | ❌ |
| Store listing metadata (icons, screenshots, descriptions) | Partner Center portal | ❌ |

> There is no CLI flag for RAI. Treat `validate-package` as the schema/test-case gate only;
> policy/RAI readiness is handled as a checklist in `submit-readiness`.

## Commands

```bash
# 1. Schema + validation rules (default method). --env resolves manifest ${{...}} placeholders:
atk validate --env <env> --manifest-file ./appPackage/manifest.json --validate-method validation-rules

# 2. Store-equivalent automated test cases (run against the built zip):
atk validate --env <env> --package-file ./appPackage/build/appPackage.<env>.zip --validate-method test-cases

# 3. Env-based validation against a build output folder:
atk validate --env <env> --output-folder ./appPackage/build
```

- Both validate methods return a non-zero exit code on failure — gate on the exit code.
- `--env <env>` is REQUIRED: the manifest contains `${{...}}` placeholders resolved per environment
  (verified in dry run — omitting `--env` fails with "Missing required input: env").
- Run `validation-rules` against the manifest early; run `test-cases` against the built `.zip`.
- **Account guard:** `validation-rules` needs no sign-in. `test-cases` calls the Developer Portal and
  requires an M365 account — before running it, do `atk auth list`, **confirm with the user which
  account/tenant to use** (don't assume "already signed in"), and don't force a silent WAM sign-in.
  If a specific/test tenant or browser-only flow is required, use the browser Developer Portal
  validation tool (`https://dev.teams.microsoft.com/validation`) with that tenant instead.

## Behavior

1. Locate the manifest / package from the ledger or arguments (do not assume paths blindly).
2. Run `validation-rules`; if it fails, surface the exact findings and STOP (blocking).
3. Build/locate the `.zip`, run `test-cases`; surface findings.
4. Append results to `publishing-ledger.json` `audit[]` with PASS/FAIL and the findings summary.

## Outputs

- PASS/FAIL verdict per method with the raw findings.
- A short remediation list for any failures, mapped to the manifest field at fault.

## References (verify before quoting)

- atk validate reference: https://learn.microsoft.com/en-us/microsoftteams/platform/toolkit/teams-toolkit-cli
- Submission checklist / validation tool: https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/deploy-and-publish/appsource/prepare/submission-checklist
- Store validation guidelines: https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/deploy-and-publish/appsource/prepare/teams-store-validation-guidelines
