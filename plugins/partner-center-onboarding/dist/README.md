# dist -- prebuilt Microsoft 365 Copilot Cowork package

`partner-center-onboarding-cowork.zip` is a ready-to-sideload Microsoft 365 app package
(manifest v1.29, app version 4.2.0, icons + three skills + optional connector) for
**Microsoft 365 Copilot Cowork**. This is a built package, not proof of live connector compatibility.

- Entry skill: `partner-center-guide` (broad triage).
- Internal specialist: `troubleshoot-account-verification` (delegated to for verification depth).
- Optional publisher skill: `marketplace-publishing`, with schema-first preparation and separate
  exact-target/before-and-after approval for every mutation, including drafts and uploads.
- Account guidance remains knowledge-only: no connector, auth, or `az login` required.
- Connector: official Marketplace Ingestion HTTPS endpoint, ID `market-ingest`, URL-only DCR
  configuration. Public OAuth discovery advertises a registration endpoint; no anonymous auth,
  placeholder OAuth registration, embedded credentials, or invented tool-description file.
- Human seller-tenant authentication, roles and submission API access are required for publishing.
  Live Cowork auth/consent/tool discovery and all seller operations remain untested.
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

## Version history (Cowork package)

| Version | Date | Notes |
| --- | --- | --- |
| 1.1.0 | 2026-08-07 | Rebuilt with fixed Learn URLs; manifest/icons moved to `cowork/`. |
| 1.2.0 | 2026-09-11 | Marketplace guidance refresh (FX, CSP, verification, SaaS). |
| 4.0.1 | 2026-09-14 | Published to Cowork from a build outside this repo: 1.2.0 skills plus a revised `cowork-setup.md` (Customize -> Upload plugin, share / Re-share, update rules). Not committed at the time. |
| 1.3.0 | 2026-10-02 | Repo-only build (FAM routing). Superseded the same day: lower than the already published 4.0.1, so never uploaded. |
| 4.1.0 | 2026-10-02 | 4.0.1 `cowork-setup.md` brought into the repo + FAM routing from 1.3.0. Must be higher than the published Cowork version. |
| 4.2.0 | 2026-10-27 | Published to Cowork with manifest 1.29, optional official Marketplace Ingestion DCR connector and a separate approval-gated publisher workflow; CLI 0.7.0. Existing app identity, limited internal audience, account guidance, and attachments preserved. Connector display verified; live OAuth and seller operations remain untested. |

Before bumping, check the version currently published in Cowork (plugin details -> Version), not only this file.