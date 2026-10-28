# dist -- prebuilt Microsoft 365 Copilot Cowork package

`partner-center-onboarding-cowork.zip` is a candidate Microsoft 365 app package
(manifest v1.29, app version 4.2.1, CLI 0.7.1, icons + three skills + optional connector) for
**Microsoft 365 Copilot Cowork**. This diagnostic-only candidate is not live and does not
claim to fix connector compatibility or the known runtime-tool gap.

- Entry skill: `partner-center-guide` (broad triage).
- Internal specialist: `troubleshoot-account-verification` (delegated to for verification depth).
- Optional publisher skill: `marketplace-publishing`, with schema-first preparation and separate
  exact-target/before-and-after approval for every mutation, including drafts and uploads.
- Account guidance remains knowledge-only: no connector, auth, or `az login` required.
- Connector: official Marketplace Ingestion HTTPS endpoint, ID `market-ingest`, URL-only DCR
  configuration. Public OAuth discovery advertises a registration endpoint; no anonymous auth,
  placeholder OAuth registration, embedded credentials, or invented tool-description file.
- Runtime tools, human seller-tenant authentication, roles and submission API access are required
  for publishing. Available connector/package labels do not establish discovery or authentication.
  When no tools/server are exposed, stop with `BLOCKED: 接続ツールが会話に出ていない`;
  do not infer auth failure, seller-rights failure, hidden logs, or a sign-in UI.
- The reported 2026-10-28 UI/runtime gap is VERIFIED only within the checked surfaces;
  H2/H3/H4/H5 causes remain UNVERIFIED. The publisher workflow is BLOCKED without tools,
  while account guidance remains useful.
- A genuinely new Cowork task reproduces zero tool-search matches despite active configuration;
  an old conversation alone is not the explanation, but backend cache remains unexcluded.
  Native CLI 1.0.101 session-only comparison reports structured `pending -> needs-auth` events,
  not authenticated success. No browser auth or seller-account selection occurred; this is not
  a same-seller-account login test. Human OAuth/consent and authenticated tool listing remain pending.
- Reported public-wire origin DCR advertising differs from the checked Entra issuer metadata
  paths (OAuth 404 versus OIDC 200 without registration metadata). That difference is VERIFIED,
  not proof of Cowork's selected discovery path or root cause. Unauthenticated protocol POSTs
  return 401 for both checked User-Agents; 401 alone is normal protected behavior.
- App ID remains `fe619316-bf0b-43bf-b399-b6c9557df006`. Update the existing app; do not create
  a new identity or change the internal audience as part of packaging.

## Rebuild

Run [`../build-cowork-zip.ps1`](../build-cowork-zip.ps1) (PowerShell). It packages the
repo `skills/` plus the loose packaging metadata in [`../cowork/`](../cowork)
(`manifest.json` + `color.png` / `outline.png`), applying the Cowork
frontmatter allowlist: Cowork only permits `name` / `description` / `license` /
`metadata` / `compatibility` and caps each `SKILL.md` at 20000 characters, so the
script strips the CLI-only `user-invocable` line from the packaged copies (the repo
copies keep it for the CLI install path) and fails if any `SKILL.md` is over the limit.
Only frontmatter is transformed; body text is preserved. A failed build leaves the previous
ZIP intact. Output text is UTF-8 without BOM, and script source remains ASCII/PowerShell 5.1-safe.
Edit `../cowork/manifest.json` (not the zip) to bump the package `version`, then rebuild.
See [`../skills/partner-center-guide/references/cowork-setup.md`](../skills/partner-center-guide/references/cowork-setup.md)
for sideloading steps. The CLI install path does not use this zip.

## Targeted validation

From the repository root, with the Python dependencies in `../tests/requirements.txt` available:

```powershell
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy RemoteSigned -File .\plugins\partner-center-onboarding\build-cowork-zip.ps1
python -B .\plugins\partner-center-onboarding\tests\test_package.py
```

Tests inspect the actual ZIP and fetch the official 1.29 schema. They check packaging limits,
fixed identity, version/description consistency, the DCR-only connector configuration, preserved
guidance/images/cheatsheet, absence of credential material, and static safety contracts.
They do not register an OAuth client, authenticate, call seller tools, publish, install, or share,
and are not live-model approval enforcement tests.
With `COWORK_BASELINE_ZIP` pointing to the preserved 4.2.0 ZIP, tests also compare the unchanged
connector and all non-diagnostic skill/assets byte-for-byte; without it that comparison is skipped.
They are not `wiqd plugin validate --mode deep` / AppValidationLibrary validation.
`wiqd` is absent; ATK 1.1.11 package-rule validation uses M365 auth and a remote portal
and was not called. The installed Microsoft manifest helper 1.0.6 passed offline schema-only
checks with the current official 1.29 schema supplied locally; it does not check platform rules.
The unchanged 4.2.0 ZIP was preserved outside the repository before rebuilding.

## Version history (Cowork package)

| Version | Date | Notes |
| --- | --- | --- |
| 1.1.0 | 2026-08-07 | Rebuilt with fixed Learn URLs; manifest/icons moved to `cowork/`. |
| 1.2.0 | 2026-09-11 | Marketplace guidance refresh (FX, CSP, verification, SaaS). |
| 4.0.1 | 2026-09-14 | Published to Cowork from a build outside this repo: 1.2.0 skills plus a revised `cowork-setup.md` (Customize -> Upload plugin, share / Re-share, update rules). Not committed at the time. |
| 1.3.0 | 2026-10-02 | Repo-only build (FAM routing). Superseded the same day: lower than the already published 4.0.1, so never uploaded. |
| 4.1.0 | 2026-10-02 | 4.0.1 `cowork-setup.md` brought into the repo + FAM routing from 1.3.0. Must be higher than the published Cowork version. |
| 4.2.0 | 2026-10-27 | Published to Cowork with manifest 1.29, optional official Marketplace Ingestion DCR connector and a separate approval-gated publisher workflow; CLI 0.7.0. Existing app identity, limited internal audience, account guidance, and attachments preserved. Connector display verified; live OAuth and seller operations remain untested. |
| 4.2.1 | 2026-10-28 | Candidate only, not published. CLI 0.7.1. Diagnostic wording separates availability from runtime tools/auth; absent tools report only the observed BLOCKED symptom. Records fresh-task reproduction, pre-auth native host status and public-wire differences without asserting a Cowork root cause, authenticated success or a same-seller-account test. H2/H3/H4/H5 causes remain pending. App ID, 1.29 connector, account guidance and assets unchanged; no seller operations. |

Before bumping, check the version currently published in Cowork (plugin details -> Version), not only this file.