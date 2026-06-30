# dist -- prebuilt Microsoft 365 Copilot Cowork package

`partner-center-onboarding-cowork.zip` is a ready-to-sideload Microsoft 365 app package
(Teams manifest v1.28 + icons + both skills) for **Microsoft 365 Copilot Cowork**.

- Entry skill: `partner-center-guide` (broad triage).
- Internal specialist: `troubleshoot-account-verification` (delegated to for verification depth).
- Knowledge-only: no connector, no auth, no `az login`.

## Rebuild

The zip is built from the repo's `skills/` plus `manifest.json` + `color.png` / `outline.png`.
See [`../skills/partner-center-guide/references/cowork-setup.md`](../skills/partner-center-guide/references/cowork-setup.md)
for sideloading and rebuild steps. The CLI install path does not use this zip.
