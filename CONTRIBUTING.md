# Contributing

> This repository is **experimental**. It is a staging ground for skills that are later
> copied into a published repository under a Microsoft organization. Because of that, we keep
> a **rich history here** and **clean history when publishing**. See "Merge strategy" below.

## TL;DR

- Branch off `main`. Use a short kebab-case branch name (e.g. `saas-offer-3layer-rewrite`).
- Write commits and PR titles as **Conventional Commits** (`docs:`, `feat:`, `fix:`, ...).
- Open a PR using the template. Lead with **Why**, then **What changed**, then **Provenance / notes**.
- Cite Microsoft Learn pages only after fetching them and confirming **HTTP 200** (no guessed URLs).
- A maintainer merges. The agent never merges without explicit per-merge human approval.

## Commit messages (Conventional Commits)

Format: `type(optional-scope): summary`

```
docs: rewrite SaaS offer skill into 3-layer model
feat(triage): add monetization routing axis
fix(webhook): correct 10-second PATCH window wording
chore: bump skill last_updated dates
```

Allowed `type` values:

| type | use for |
| --- | --- |
| `docs` | skill content, READMEs, guidance (most changes in this repo) |
| `feat` | a new skill, route, or capability |
| `fix` | correcting wrong behavior, wrong facts, or broken references |
| `refactor` | restructuring without changing meaning |
| `chore` | version bumps, metadata, tooling, housekeeping |

Rules:
- Summary in the imperative mood, lower case, no trailing period, <= ~72 chars.
- Scope is optional; use a skill or area name (e.g. `triage`, `saas-offer`, `webhook`).
- Put rationale and any source URLs in the commit **body**, wrapped at ~72 columns.
- Keep the existing `(vX.Y.Z)` version bump style **out of the type prefix**; if you bump a
  version, note it in the body or as a trailing `chore:` commit, not inside the summary type.

## Pull requests

- One logical change per PR. Keep unrelated edits out.
- Title = the lead Conventional Commit (e.g. `docs: ...`).
- Body follows `.github/PULL_REQUEST_TEMPLATE.md`: **Why / What changed / Provenance / notes / Checklist**.
- Plain ASCII punctuation (avoid em dashes and smart quotes) so text survives CLI flows.

### Sourcing rule (important)

This repo guides people through Microsoft Marketplace flows, so factual accuracy matters.

- Ground claims in `learn.microsoft.com` (and official `*.microsoft.com`) pages.
- **Fetch every URL you cite and confirm it is not a 404 before quoting it.** Do not paste a
  search-result URL unmodified. If you could not verify a page, mark it explicitly as `未検証`
  (unverified) and do not state its contents as fact.
- Prefer the exact article path over a landing/overview page.

## Merge strategy (two-stage history)

We deliberately keep two different history shapes:

1. **In this experimental repo** -> prefer **merge commits**. We want the full trail
   (individual commits, conflict resolutions, experiments) so it is easy to trace later why a
   skill says what it says.
2. **When copying to the published Microsoft-org repo** -> **squash / curate** into clean,
   self-contained commits. The downstream repo wants a tidy history, not the experiment log.

So: merge PRs here with a **merge commit** unless a PR is trivial; do the cleanup at publish time.

## Skill files

- Each skill lives in `plugins/<plugin>/skills/<skill>/SKILL.md` with YAML front matter.
- Bump `last_updated` (ISO `YYYY-MM-DD`) whenever you change a `SKILL.md`.
- Keep `description`, `argument-hint`, and `user-invocable` consistent with the body.
