# Project status

> Single source of truth for "where are we across all workstreams." One screen.
> Update this whenever a workstream changes phase, a PR opens/merges, or a decision is made.
>
> **Last updated:** 2026-07-15 by Copilot

## Workstreams

| WS | Theme | Phase | State | Issue | Next action |
|----|-------|-------|-------|-------|-------------|
| core | Plugin core (agent-publishing, 8 skills) | published v0.1.7 | ✅ live | — | — |
| B | Declarative knowledge end-to-end verify | docs fix merged | ✅ usable-complete | #3 | optional: attach a real (non-sample) source — or nothing |
| A | SaaS Tier-1 fulfillment backend | L2 proven through product UI (cold-start) + runbook re-validated | ✅ Tier-1 (A1) + L2 complete | #20 | merge this PR (admin-URL G1 fix); re-run env torn down |
| S | SaaS modernization + agent-first sample planning | repo-shape decision recorded | ✅ decision-made | #29 | if authorized, open a separate implementation issue/repo |
| P1b | Publish-path live portal walk (submit-readiness battle-test) | portal walk done + skills corrected | ✅ complete | #15 | optional: walk a second skill; otherwise done |
| PC | partner-center-onboarding (onboarding triage + verification) | v0.4.0 in review (adds §8 review/validation) | 🟡 PR open | — | merge §8, then keep collecting trial feedback |

State legend: ✅ done/live · 🟡 in progress/review · ⏸ paused/blocked · 🔴 broken

## Open PRs / Issues

- PR #26 (monetization-saas-offer self-complete L2 provisioning command sequence) -- **merged**.
- **Open:** admin-portal Fulfillment-URL G1 fix (repoint *both* portal + admin) + L2 re-run milestone -- this PR.
- PR #25 (L2 emulator gotchas + done-checklist) -- **merged** (`f140189`).
- **Open: PR #24** (cowork dist zip sideload validation) -- in review.
- WS-A L2 tracking: **#20 open**; upstream doc-gap filed as `microsoft/Commercial-Marketplace-SaaS-API-Emulator#68` (emulator webhook needs Accelerator `ValidateWebhookJwtToken=false`).
- Earlier PRs merged (#1, #4, #6, #7, #8, #9, #10, #16, #17, #19, #21, #22, #23, #25, #26).
- Coordination issues: #2/#3/#5 closed; **#15 (P1b portal walk) ready to close** — walk complete, both fix PRs merged.

## WS-P1b outcome (publish-path portal walk, done 2026-06-25)

- **Battle-test PASS:** a declarative `appPackage.dev.zip` built with the corrected `atk new` (no `--programming-language`) passed the Partner Center portal's **"Manifest checks passed"** (Office web / Windows / Teams). Negative control (no `manifest.json`) → `ManifestFileNotFound`. First live proof of `validate-package`/`submit-readiness`'s core claim.
- **Irreversibility resolved:** Create locks **product type + publisher** permanently, but an **unpublished draft is deletable** (confirm dialog releases the reserved name + discards work). Full irreversibility only applies post-publish (Stop distribution only).
- **submit-readiness corrected (PR #17):** worksheet restructured **page-driven**; Categories are functional (Legal+HR, not "AI Apps and Agents"); EULA/Privacy/Support live on Properties (field = "EULA link"); two icon systems (package 192/32 vs listing 300x300 + screenshots 1366x768); markets default to all 242; Entra/SSO/tenantId removed from the declarative path; no "Microsoft 365 and Copilot" tab (it's a +New offer choice).
- **App Compliance / Publisher Attestation = Optional / non-blocker:** all public sources (publish article, App Compliance userguide, pre-publish checklist) mark it Optional; the insider "required for agents" claim is retained as **未検証** and explicitly does **not** block.
- **atk fix (PR #16):** dropped `--programming-language` from declarative `atk new` (kept for custom-engine).

## WS-A outcome (Tier-1, done 2026-06-19)

- **Pricing model = flat rate** (metering-capable; per-user rejected because metering is flat-rate-only). No `quantity` branch / no `ChangeQuantity` in the Tier-1 state store.
- **Build route = (a) Microsoft SaaS Accelerator** (MIT, maintained) via its own installer; `@git-ape` optional for route (a). Route (b) hand-rolled IaC kept as the alternative.
- **Live dry-run:** full plane deployed in **West US 3** (VNet, Azure SQL, Key Vault, App Service B1, Admin+Customer apps, multitenant Entra app), L1 verified (landing 200, webhook-no-JWT 400, admin 500=config-pending), then **fully torn down** (no residual cost).
- **A1/A2 done-split:** A1 = reachability + synthetic verify via the SaaS API Emulator (free); A2 = real paid DEV-offer purchase (opt-in). **Tier-1 "done" = A1.**
- `.NET 8` (LTS, EOL 2026-11-10) intentional; framework upgrades left to upstream (target .NET 10 LTS).

## Milestones (history)

- 2026-07-10 — **WS-A L2 re-run through the product UI (cold-start)** surfaced the admin-portal
  Fulfillment-URL gap: on a fresh deploy, **Activate failed with HTTP 500 "Token invalid or expired"**
  because the installer leaves the *admin* app's `SaaSApiConfiguration__FulFillmentAPIBaseURL` on the
  real `marketplaceapi.microsoft.com` while G1 only repointed the customer portal — Resolve (portal)
  worked, Activate (admin) did not. Promoted the fulfillment-URL repoint to an explicit **both-apps**
  G1 step and sharpened the gotcha table in `monetization-saas-offer` (this PR). Re-confirmed the full
  audit chain through the product (`None → PendingFulfillmentStart → PendingActivation → Subscribed →
  Unsubscribed`). Billable re-run env torn down same day.

- 2026-07-15 — **WS-S planning decision recorded (#29)**: captured the planning-only recommendation in
  `monetization-saas-offer`: for a future modernized sample with conversational landing + publisher
  admin, prefer a **new standalone sample repo** over a long-lived Accelerator fork; keep the
  official emulator as the **token-free L2 driver** and prefer upstream modernization PRs there; bias
  the first sample toward **.NET** for parity with the Accelerator's Tier-1 plane; define v0 as
  flat-rate-only landing + Resolve/Activate + webhook/state-store sync + minimal read-mostly admin
  with explicit-confirm Activate.

- 2026-07-07 — **WS-A runbook cold-start re-validated**: rebuilt L2 from scratch following only the
  merged runbook, proving it was a gotchas-layer, not a self-sufficient provisioning guide. Surfaced
  and fixed 6 blockers now folded into the runbook (PR #26): clone must pin release tag `8.2.1` (not
  `main`); `Deploy.ps1` line ~214 uses retired `Get-AzureRmSqlServer` → patch to `az sql server show`;
  tenant governance can block the multi-tenant Landing app registration + the `--years 2` secret
  lifetime (new generalized Entra-app prereq); deploy can stop at "Execute SQL schema" before code
  publish → apply `script.sql` via **go-sqlcmd `ActiveDirectoryAzCli`**; emulator `docker/Dockerfile`
  `RUN npm install -g npm` breaks `az acr build` → remove the line; `LANDING_PAGE_URL` must be the
  **https Caddy TLS-front FQDN**, not the http emulator FQDN. Real `caddy-aci.yaml` inlined. Billable
  rebuild torn down same day (`az group exists`→false, AD apps deleted, billing stopped). Scout-brokered via #20.

- 2026-07-04 — **WS-A L2 synthetic E2E proven**: drove the SaaS Accelerator through Resolve → Activate → **webhook → state-store sync** with the official SaaS API Emulator (no purchase). Full audit chain `None → PendingFulfillmentStart → PendingActivation → Subscribed → Unsubscribed` (outbound Activate + inbound webhook both proven). Root-caused the emulator webhook **HTTP 401**: the Accelerator's `ValidateWebhookJwtToken` requires the caller token's `appid`/`azp` to equal the fixed Microsoft Marketplace app id, which the emulator cannot mint → set `false` for L2, keep `true` in production. Operational gotchas + L2 done-checklist added to `monetization-saas-offer` (PR #25); upstream doc-gap filed (emulator #68). Live env pending teardown.

- 2026-07-02 — **partner-center-guide §8 added (v0.4.0)**: new section "リスティング/コンテンツ審査でよく落ちる点 (Store validation Must-fix)" -- way forward links in 3 places (manifest + AppSource long description + first-run experience, policy 1140.1.4, put as markdown in the manifest description, no Partner Center form), manifest/listing name+description match, description prohibited content (1140.9), EULA/Privacy/Support URL auth-free, reject first-response, package (manifest id GUID / validDomains). Also §4 gains "wrong Offer type" as a second cause of a missing Attestation item. Driven by a real internal review case; all facts fetch-verified against Teams Store + agent validation guidelines. Cowork dist zip rebuilt.

- 2026-07-01 — **partner-center-onboarding v0.3.0 merged (PR #21)**: added entry skill `partner-center-guide` (broad onboarding triage + publish-path + REO/MPO/CSP + JP tax cheatsheet + 4 decision-flow images); refactored to a two-skill model (guide = entry/invocable, `troubleshoot-account-verification` = internal/non-invocable, reached by delegation); added a prebuilt Cowork app package under `dist/`. Copilot code review: 3 comments, all addressed and resolved.
- 2026-06-25 — **WS-P1b complete**: live Partner Center portal walk (S0–S9 incl. Delete cleanup); package validation battle-tested PASS; `submit-readiness` corrected to a page-driven worksheet and `path-declarative-atk` `atk new` flag fixed; App Compliance reframed Optional/非ブロッカー (PR #16 → #17, agent-publishing 0.1.7).
- 2026-06-19 — **WS-A Tier-1 complete**: SaaS Accelerator deployed+verified+torn down; skill documents both routes, the 3-roles/3-tokens model, the A1 ladder, route-(a) prereqs + cost note (PR #7, #9).
- 2026-06-19 — **partner-center-onboarding** shipped: `troubleshoot-account-verification` (4-condition convergence, triage A–D, escalation/role-owner forks) (PR #8, #10).
- 2026-06-19 — WS-B declarative path **usable-complete**: triage → scaffold → author → wire knowledge (`OneDriveAndSharePoint`/`items_by_url`) → grounded answer + citation, with license/formatting traps documented (PR #4).
- 2026-06-19 — SaaS skill **3-layer rewrite** (fulfillment / pricing+licensing / tax; state table mandatory; metering = flat-rate-only) + repo conventions (`CONTRIBUTING.md`, PR template) (PR #1).
- (earlier) — Plugin published v0.1.5: 8 skills, repo-as-marketplace, real-install verified; declarative L1/L2 verified hands-on.

---

## How to use this file

> These conventions are **binding** and codified in `CONTRIBUTING.md`
> ("Coordination & status tracking"). This section is the at-a-glance copy.

1. **Update STATUS.md in the same PR/commit that changes a workstream's state.** Bump "Last updated."
2. **End every coordination comment that changes state or hands off with a "you-are-here" stamp**
   (skip it on trivial one-line acks) so a reader never loses the map:

   ```
   ---
   📍 WS-<A/B/...> · Phase: <phase> · This step: <what just happened>
      Next: <next action> · Blocked-on: <human decision / review / nothing> · See STATUS.md
   ```

3. Keep this file **terse** — it is a map, not a log. Detail lives in the Issues/PRs it points to.
