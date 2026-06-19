# Project status

> Single source of truth for "where are we across all workstreams." One screen.
> Update this whenever a workstream changes phase, a PR opens/merges, or a decision is made.
>
> **Last updated:** 2026-06-19 by Scout

## Workstreams

| WS | Theme | Phase | State | Issue | Next action |
|----|-------|-------|-------|-------|-------------|
| core | Plugin core (8 skills) | published v0.1.5 | ✅ live | — | — |
| B | Declarative knowledge end-to-end verify | docs fix merged | ✅ usable-complete (A1) | #3 | optional: A2 live-purchase verify (opt-in) |
| A | SaaS Tier-1 fulfillment backend | design ✓ → pre-build | ⏸ paused | #5 | maker confirms 3 open decisions + Azure sign-in |

State legend: ✅ done/live · 🟡 in review · ⏸ paused/blocked · 🔴 broken

## Open PRs / Issues

- #5 (WS-A) — **open, paused** on 3 maker decisions (below)
- #3 (WS-B) — **open**, done-definition A1 met; keep open until A2 decision
- Closed: #2 (SaaS 3-layer design, → PR #1 merged) · PR #1 · PR #4 (declarative docs fix)

## Decisions waiting on the maker (Mamoru)

- [ ] **WS-A pricing model** — flat rate or per user (changes the Tier-1 state-store schema; flat rate recommended for the spike)
- [ ] **WS-A Azure identity + subscription + region** (separate from the M365 test tenant; pin a non-WAM sign-in)
- [ ] **WS-A `@git-ape` onboarding** confirmed against that subscription (else run `git-ape-onboarding` first)

## Milestones (history)

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
