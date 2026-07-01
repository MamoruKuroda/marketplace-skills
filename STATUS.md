# Project status

> Single source of truth for "where are we across all workstreams." One screen.
> Update this whenever a workstream changes phase, a PR opens/merges, or a decision is made.
>
> **Last updated:** 2026-07-01 by Copilot

## Workstreams

| WS | Theme | Phase | State | Issue | Next action |
|----|-------|-------|-------|-------|-------------|
| core | Plugin core (agent-publishing, 8 skills) | published v0.1.7 | ✅ live | — | — |
| B | Declarative knowledge end-to-end verify | docs fix merged | ✅ usable-complete | #3 | optional: attach a real (non-sample) source — or nothing |
| A | SaaS Tier-1 fulfillment backend | live dry-run done + documented | ✅ Tier-1 (A1) complete | #5 | optional: live L2 emulator run; otherwise done |
| P1b | Publish-path live portal walk (submit-readiness battle-test) | portal walk done + skills corrected | ✅ complete | #15 | optional: walk a second skill; otherwise done |
| PC | partner-center-onboarding (onboarding triage + verification) | published v0.3.0 | ✅ live | — | collecting trial feedback (Issues) |

State legend: ✅ done/live · 🟡 in progress/review · ⏸ paused/blocked · 🔴 broken

## Open PRs / Issues

- Open: none. **PR #21 merged** (partner-center-onboarding v0.3.0 -- guide entry skill + two-skill model).
- Earlier PRs merged (#1, #4, #6, #7, #8, #9, #10, #16, #17, #19, #21).
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
