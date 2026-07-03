# dist -- prebuilt Microsoft 365 Copilot Cowork package

`partner-center-onboarding-cowork.zip` is a ready-to-sideload Microsoft 365 app package
(Teams manifest v1.28 + icons + both skills) for **Microsoft 365 Copilot Cowork**.

- Entry skill: `partner-center-guide` (broad triage).
- Internal specialist: `troubleshoot-account-verification` (delegated to for verification depth).
- Knowledge-only: no connector, no auth, no `az login`.

## Rebuild

Run [`../build-cowork-zip.ps1`](../build-cowork-zip.ps1) (PowerShell). It packages the
repo `skills/` plus `manifest.json` + `color.png` / `outline.png`, applying the Cowork
frontmatter allowlist: Cowork only permits `name` / `description` / `license` /
`metadata` / `compatibility` and caps each `SKILL.md` at 20000 characters, so the
script strips the CLI-only `user-invocable` line from the packaged copies (the repo
copies keep it for the CLI install path) and fails if any `SKILL.md` is over the limit.
See [`../skills/partner-center-guide/references/cowork-setup.md`](../skills/partner-center-guide/references/cowork-setup.md)
for sideloading steps. The CLI install path does not use this zip.
