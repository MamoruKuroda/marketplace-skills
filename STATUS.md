# Project status

> Single source of truth for "where are we across all workstreams." One screen.
> Update this whenever a workstream changes phase, a PR opens/merges, or a decision is made.
>
> **Last updated:** 2026-06-19 by Scout

## Workstreams

| WS | Theme | Phase | State | Issue | Next action |
|----|-------|-------|-------|-------|-------------|
| core | Plugin core (8 skills) | published v0.1.5 | ✅ live | — | — |
| B | Declarative knowledge end-to-end verify | docs fix merged | ✅ usable-complete | #3 | optional: attach a real (non-sample) source — or nothing |
| A | SaaS Tier-1 fulfillment backend | decisions made → building | 🟡 building | #5 | Azure sign-in (in progress) → deploy SaaS Accelerator → A1 free fulfillment checks |

State legend: ✅ done/live · 🟡 in progress/review · ⏸ paused/blocked · 🔴 broken

## Open PRs / Issues

- #5 (WS-A) — **open, building** (3 decisions resolved in-session; see below)
- #3 (WS-B) — **open**, done met; venue for the STATUS.md ops-rule agreement
- Closed: #2 (SaaS 3-layer design → PR #1) · PR #1 · PR #4 (declarative docs fix)

## WS-A decisions (resolved 2026-06-19, in-session)

- **Pricing model = flat rate** (metering-capable; per-user was rejected because metering is flat-rate-only). Tier-1 state store therefore needs no `quantity` branch; no `ChangeQuantity` webhooks.
- **Azure identity + subscription = pinned** (IDs kept session-local, not posted publicly), region **East US 2**.
- **Build route = (a) deploy the Microsoft SaaS Accelerator** (MIT-licensed, actively maintained) via its own installer; `@git-ape` onboarding is **optional** for route (a).

> **A1 / A2 are the WS-A done-split** (not WS-B): **A1** = landing+webhook deployed & reachable 24/7, webhook validated with synthetic/replayed events + state store updated (free, local). **A2** = real purchase via a paid DEV offer (opt-in, incurs invoices). Tier-1 "done" = A1.

## Milestones (history)

- 2026-06-19 — WS-A decisions locked (flat rate / Azure pinned East US 2 / route = Microsoft SaaS Accelerator); build started.
- 2026-06-19 — WS-B declarative path **usable-complete**: triage → scaffold → author → wire knowledge (`OneDriveAndSharePoint`/`items_by_url`) → grounded answer + citation, with license/formatting traps documented (PR #4).
- 2026-06-19 — SaaS skill **3-layer rewrite** merged (fulfillment / pricing+licensing / tax separation; state table mandatory; metering = flat-rate-only) (PR #1).
- 2026-06-19 — Repo conventions added (`CONTRIBUTING.md`, PR template).
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
