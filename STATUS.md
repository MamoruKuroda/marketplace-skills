# Project status

> Single source of truth for "where are we across all workstreams." One screen.
> Update this whenever a workstream changes phase, a PR opens/merges, or a decision is made.
>
> **Last updated:** 2026-06-19 by Scout

## Workstreams

| WS | Theme | Phase | State | Issue | Next action |
|----|-------|-------|-------|-------|-------------|
| core | Plugin core (agent-publishing, 8 skills) | published v0.1.5 | ✅ live | — | — |
| B | Declarative knowledge end-to-end verify | docs fix merged | ✅ usable-complete | #3 | optional: attach a real (non-sample) source — or nothing |
| A | SaaS Tier-1 fulfillment backend | live dry-run done + documented | ✅ Tier-1 (A1) complete | #5 | optional: live L2 emulator run; otherwise done |
| PC | partner-center-onboarding (account verification) | published v0.2.0 | ✅ live | — | optional refinements |

State legend: ✅ done/live · 🟡 in progress/review · ⏸ paused/blocked · 🔴 broken

## Open PRs / Issues

- All PRs merged (#1, #4, #6, #7, #8, #9, #10). No open PRs.
- #3 (WS-B) / #5 (WS-A) — open as coordination venues; the work is complete.
- Closed: #2 (SaaS 3-layer design → PR #1).

## WS-A outcome (Tier-1, done 2026-06-19)

- **Pricing model = flat rate** (metering-capable; per-user rejected because metering is flat-rate-only). No `quantity` branch / no `ChangeQuantity` in the Tier-1 state store.
- **Build route = (a) Microsoft SaaS Accelerator** (MIT, maintained) via its own installer; `@git-ape` optional for route (a). Route (b) hand-rolled IaC kept as the alternative.
- **Live dry-run:** full plane deployed in **West US 3** (VNet, Azure SQL, Key Vault, App Service B1, Admin+Customer apps, multitenant Entra app), L1 verified (landing 200, webhook-no-JWT 400, admin 500=config-pending), then **fully torn down** (no residual cost).
- **A1/A2 done-split:** A1 = reachability + synthetic verify via the SaaS API Emulator (free); A2 = real paid DEV-offer purchase (opt-in). **Tier-1 "done" = A1.**
- `.NET 8` (LTS, EOL 2026-11-10) intentional; framework upgrades left to upstream (target .NET 10 LTS).

## Milestones (history)

- 2026-06-19 — **WS-A Tier-1 complete**: SaaS Accelerator deployed+verified+torn down; skill documents both routes, the 3-roles/3-tokens model, the A1 ladder, route-(a) prereqs + cost note (PR #7, #9).
- 2026-06-19 — **partner-center-onboarding** shipped: `troubleshoot-account-verification` (4-condition convergence, triage A–D, escalation/role-owner forks) (PR #8, #10).
- 2026-06-19 — WS-B declarative path **usable-complete**: triage → scaffold → author → wire knowledge (`OneDriveAndSharePoint`/`items_by_url`) → grounded answer + citation, with license/formatting traps documented (PR #4).
- 2026-06-19 — SaaS skill **3-layer rewrite** (fulfillment / pricing+licensing / tax; state table mandatory; metering = flat-rate-only) + repo conventions (`CONTRIBUTING.md`, PR template) (PR #1).
- (earlier) — Plugin published v0.1.5: 8 skills, repo-as-marketplace, real-install verified; declarative L1/L2 verified hands-on.

---

## How to use this file (proposed convention — pending agreement in #3)

> This section is a **proposal** from Scout. It is not yet a binding rule until the Copilot CLI agent
> acks it and it is written into `CONTRIBUTING.md`.

1. **Update STATUS.md in the same PR/commit that changes a workstream's state.** Bump "Last updated."
2. **End every coordination comment with a "you-are-here" stamp** so a reader never loses the map:

   ```
   ---
   📍 WS-<A/B/...> · Phase: <phase> · This step: <what just happened>
      Next: <next action> · Blocked-on: <human decision / review / nothing> · See STATUS.md
   ```

3. Keep this file **terse** — it is a map, not a log. Detail lives in the Issues/PRs it points to.
