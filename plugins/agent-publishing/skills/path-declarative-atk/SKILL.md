---
name: path-declarative-atk
description: "Scaffolds, validates, and packages a declarative Microsoft 365 Copilot agent with the Microsoft 365 Agents Toolkit CLI (atk), producing a submission-ready app package. Routed to when agentType == declarative."
argument-hint: "App name, programming language, knowledge sources and actions. Reads publishing-ledger.json from triage."
user-invocable: true
last_updated: "2026-06-19"
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
- The tenant must have an **M365 Copilot license** (or Copilot Studio pay-as-you-go billing /
  Copilot Credits) for an agent with any capability beyond Web search — for example
  SharePoint/OneDrive knowledge grounding. **Sideloading alone is not sufficient to *use* a
  knowledge-grounded agent:** without a license it installs and behaves in-character but every
  grounded answer comes back empty (looks identical to a wiring bug). ([prerequisites],
  [optimize-content-retrieval])

### Microsoft 365 account guard (read before any sign-in-requiring step)

**Do not assume an account is "already signed in," and never trigger a silent sign-in.** `atk doctor`
reporting OK does not establish which identity will be used. Before any step that needs M365 auth
(`atk validate --validate-method test-cases`, `atk install`/sideload, `atk publish`):

1. Run `atk auth list` and show the user the currently signed-in M365 account (if any).
2. **Ask the user which account/tenant to use for this run**, and confirm it matches their intended
   (often a dedicated test) tenant — not a corporate identity picked by accident.
3. On Windows, `atk auth login m365` uses the OS WAM account picker. If the user requires a
   browser-only / specific-tenant flow, do **not** force it through WAM — pause and let the user sign
   in deliberately, or use the browser-based Developer Portal validation tool instead
   (`https://dev.teams.microsoft.com/validation`) with their chosen tenant.
4. **Sign-in-free steps** (`atk new`, `atk package`, `atk validate --validate-method validation-rules`)
   need no account and can proceed without this prompt.

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

### 2. Author the agent (DO THIS BEFORE PACKAGING — the scaffold is a blank template)

`atk new` produces a **generic template**: the `instructions` only say "you are a declarative agent…",
there are no knowledge sources, and no conversation starters. **If you package as-is, you ship a
generic Copilot that ignores the intended purpose** (e.g. an "HR policy Q&A" agent that answers like
plain Copilot). Always tailor it first, grounded in the intent recorded in `publishing-ledger.json`.

Actively guide the user (don't just say "edit the files"):

1. **Rewrite `instructions`** (in `appPackage/instruction.txt` → built into `declarativeAgent.json`)
   to the agent's real purpose. Propose a concrete draft from the ledger's offer name/intent. Example
   for an HR policy Q&A agent:
   > "You are an HR policy assistant for <company>. Answer questions about leave, expenses, working
   > hours, and code of conduct using ONLY the connected HR policy documents. If the answer isn't in
   > the policies, say so and point to HR. Be concise and cite the policy section."
2. **Add knowledge (decide grounding now — pick one of three).** Ask the user which fits, using
   the ledger intent to phrase the question. This is the single biggest driver of whether the agent
   feels real, so do not skip it.

   **A. "I already have a source" (the real path — default for most makers).**
   Wire the existing source as an entry in the **`capabilities`** array of
   `declarativeAgent.json` (knowledge is not a top-level field; each capability type appears at
   most once). For SharePoint/OneDrive, use the **`OneDriveAndSharePoint`** capability with
   **`items_by_url`** (an **absolute resource URL** — e.g.
   `https://contoso.sharepoint.com/Shared%20Documents/hr-policies` — **NOT** a `/:t:/g/...`
   sharing link) or `items_by_sharepoint_ids`. Best practice is to point at the **specific
   file(s)** rather than the folder for better retrieval (you can list up to 20 files); a
   folder/site URL also works. Confirm the agent can see it, then continue to validation.
   ([declarative-agent-manifest-1.7], [optimize-content-retrieval])

   **B. "I want to see it work end-to-end first" (PoC / first-timers).**
   Generate ONE throwaway sample document *derived from the ledger intent* (HR intent → a 1-page
   sample HR policy; IT intent → a 1-page sample IT FAQ — never a fixed canned file) and
   **stamp it "SAMPLE — replace with real content before packaging/publish."** Then wire it the
   **same way as A**: the `EmbeddedKnowledge` capability (local in-package files) is **not yet
   available**, so you must **upload the sample to SharePoint/OneDrive and reference it via
   `OneDriveAndSharePoint` `items_by_url`** — B converges onto A's mechanism. Authoring rules for
   the sample (so grounding is not silently empty): **plain prose, NO tables or special
   formatting** (Copilot does not parse tables in SharePoint content), keep each file
   **≤ ~36,000 characters** when referenced by site/folder URL. Tip: give each trial a **unique
   filename** and embed a **unique canary value** (e.g. a "document reference code") so a grounded
   answer can be proven to come from THIS file. Add a TODO in the ledger audit so the sample is not
   shipped by accident. ([declarative-agent-manifest-1.7], [optimize-content-retrieval])

   **C. "Knowledge-free on purpose" (advanced / actions-only).**
   Proceed, but apply the "Runs but empty" warning below so the user is not surprised.

   > **"Runs but empty" warning (applies to C, and to A/B until a source is actually attached).**
   > With good `instructions` but NO knowledge attached, the agent installs and behaves in-character
   > (introduces itself correctly, refuses off-topic asks) but **every factual question returns
   > "I couldn't find that in the connected documents."** This is expected and correct — not a bug —
   > because there is no data to ground on. Real answers require at least one knowledge source.
   >
   > **Empty-grounding triage checklist** (when a knowledge source IS attached but answers are still
   > empty, work these in order — the cause is usually one of these, not a manifest bug):
   > (a) is a knowledge source actually attached in `capabilities`?
   > (b) does the tenant have an **M365 Copilot license / metered usage**? (sideload alone is not enough)
   > (c) has the content been **indexed** yet? (a brand-new SharePoint upload can lag and look empty)
   > (d) has **table/special formatting** been stripped from the source? (Copilot does not parse tables)
3. **Add conversation starters** that match the purpose (e.g. "How do I request annual leave?",
   "What's the expense approval limit?").
4. Update the **Microsoft 365 app manifest** (`manifest.json`) name/description and the `color.png`
   (192x192) / `outline.png` (32x32) icons.
5. For actions, add an API plugin: `atk add action` (and `atk add auth-config` if the API needs auth).

> Note: API plugins are supported as actions within declarative agents.
>
> **Gate:** before packaging, confirm (1) `instructions` are purpose-specific (not the template
> default), and (2) the knowledge decision A/B/C was made explicitly. If B, confirm the sample is
> flagged "replace before publish." If C, confirm the user accepted the "Runs but empty" behavior.

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
- [declarative-agent-manifest-1.7] (capabilities array, `OneDriveAndSharePoint` `items_by_url`,
  `EmbeddedKnowledge` "not yet available", license note): https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-manifest-1.7
- [optimize-content-retrieval] (reference specific files; ≤36,000 chars for site/folder URL refs;
  remove tables/special formatting; license note): https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/optimize-content-retrieval
- [prerequisites] (M365 Copilot license / Copilot Studio metered usage required to ground on
  organizational data): https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/prerequisites
