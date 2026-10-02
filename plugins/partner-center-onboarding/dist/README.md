# dist -- prebuilt Microsoft 365 Copilot Cowork package

`partner-center-onboarding-cowork.zip` is a ready-to-sideload Microsoft 365 app package
(Teams manifest v1.28, app version 4.1.0, icons + both skills) for **Microsoft 365 Copilot Cowork**.

- Entry skill: `partner-center-guide` (broad triage).
- Internal specialist: `troubleshoot-account-verification` (delegated to for verification depth).
- Knowledge-only: no connector, no auth, no `az login`.

## Rebuild

Run [`../build-cowork-zip.ps1`](../build-cowork-zip.ps1) (PowerShell). It packages the
repo `skills/` plus the loose packaging metadata in [`../cowork/`](../cowork)
(`manifest.json` + `color.png` / `outline.png`), applying the Cowork
frontmatter allowlist: Cowork only permits `name` / `description` / `license` /
`metadata` / `compatibility` and caps each `SKILL.md` at 20000 characters, so the
script strips the CLI-only `user-invocable` line from the packaged copies (the repo
copies keep it for the CLI install path) and fails if any `SKILL.md` is over the limit.
Edit `../cowork/manifest.json` (not the zip) to bump the package `version`, then rebuild.
See [`../skills/partner-center-guide/references/cowork-setup.md`](../skills/partner-center-guide/references/cowork-setup.md)
for sideloading steps. The CLI install path does not use this zip.

## Version history (Cowork package)

| Version | Date | Notes |
| --- | --- | --- |
| 1.1.0 | 2026-08-07 | Rebuilt with fixed Learn URLs; manifest/icons moved to `cowork/`. |
| 1.2.0 | 2026-09-11 | Marketplace guidance refresh (FX, CSP, verification, SaaS). |
| 4.0.1 | 2026-09-14 | Published to Cowork from a build outside this repo: 1.2.0 skills plus a revised `cowork-setup.md` (Customize -> Upload plugin, share / Re-share, update rules). Not committed at the time. |
| 1.3.0 | 2026-10-02 | Repo-only build (FAM routing). Superseded the same day: lower than the already published 4.0.1, so never uploaded. |
| 4.1.0 | 2026-10-02 | 4.0.1 `cowork-setup.md` brought into the repo + FAM routing from 1.3.0. Must be higher than the published Cowork version. |

Before bumping, check the version currently published in Cowork (plugin details -> Version), not only this file.