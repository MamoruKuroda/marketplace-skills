# partner-center-onboarding

> 日本語版は [README.ja.md](README.ja.md) を参照してください。

> **EXPERIMENTAL.** Guidance only.This plugin **never** signs in to Partner Center, assigns
> roles, edits Microsoft Entra, or submits anything on your behalf — every portal action is
> performed by you. It never asks for or stores passwords, verification codes, or secrets.

A skill set that helps ISVs and partners **self-serve Microsoft Partner Center onboarding**
when publishing to the **Microsoft Marketplace** -- from registration through to publishing a
**Microsoft 365 Copilot agent** or **SaaS offer**.

## Why this exists

Partners most often stall at the onboarding *entrance*: registration, tenant association, the
identity-verification order, publish-path choices (declarative vs custom-engine, offer types,
billing), and channel/tax questions (REO/MPO/CSP, Japan consumption tax). Account verification in
particular -- not the agent build -- is a frequent blocker: sign-in and role confusion,
tenant/App-ID mismatches, publisher/business-existence evidence, and "what stage am I at?"
anxiety. These were distilled from real partner support threads and collapsed into a single
entry-point triage plus a deep verification specialist.

## Who this is for

For software companies and startups (SDC/ISV) onboarding to Partner Center and the
Marketplace, and anyone helping those teams get set up. It's grounded entirely in
**public Microsoft documentation**, so both the company publishing and the people
helping them can use it freely. If your company is already onboarded or has an
Offer live — or you're its Microsoft contact — you may not need it, though partners
who help others publish still find it a useful reference.

## Two-skill model: one entrance, one specialist

- **`partner-center-guide` (entry, `user-invocable: true`)** -- broad triage: registration,
  tenant association, publish-path (agent type / offer type / billing), channel/tax
  (REO/MPO/CSP, Japan MoR), and listing/content review (Store validation Must-fix, §8).
  Carries four decision-flow images and a JP tax cheatsheet.
- **`troubleshoot-account-verification` (internal, `user-invocable: false`)** -- the guide
  delegates here when account *verification* is the actual blocker; converges four conditions and
  emits `verification-ledger.json`.

Users always enter through the guide; verification depth is reached by delegation. One entrance,
no "which skill do I use?" confusion.

## Try asking (starter prompts)

- 「Partner Center にこれから登録したい。何から始めればいい?」
- 「テナント (Entra ID) の関連付けができない。」
- 「Copilot エージェントを公開したい。宣言型とカスタムエンジン、どっち?」
- 「Publisher Attestation の項目が見当たらない。」
- 「Developer 審査が通らない (登記簿と表記が違う)。」
- 「審査 (Store validation) で sign-up / Contact のリンクが無いと差し戻された。どこを直す?」
- 「代理店 / CSP 経由で売りたい。REO と MPO の違いと、日本の消費税は?」

> Full starter list and routing live in
> [`skills/partner-center-guide/SKILL.md`](skills/partner-center-guide/SKILL.md).

## Skills

| Skill | Invocable | Purpose |
| --- | --- | --- |
| [`partner-center-guide`](skills/partner-center-guide) | entry (true) | Broad onboarding triage + publish-path + REO/MPO + JP tax; flow images + cheatsheet |
| [`troubleshoot-account-verification`](skills/troubleshoot-account-verification) | internal (false) | Deep account-verification diagnosis; 4-condition convergence + `verification-ledger.json` |

## Relationship to `agent-publishing`

`agent-publishing` decides **what to build and how to submit** (agent type / monetization /
submission worksheet). `partner-center-onboarding` handles the **orthogonal** problem of getting
the **account itself verified** so you *can* submit. Use this when verification — not the build —
is the blocker.

## Portability (CLI + Cowork)

Skills here are portable **Agent Skills** (`SKILL.md`, the open standard). They run as-is in
**GitHub Copilot CLI**, and the `skills/` folder can be packaged into a Microsoft 365 app package
(`.zip` with `manifest.json` + icons) for **Microsoft 365 Copilot Cowork**
([packaging guide](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development)).
They avoid slash-only invocation and sub-agents (not yet supported in Cowork) and rely on
natural-language triggers.

## Install

```bash
copilot plugin marketplace add MamoruKuroda/marketplace-skills
copilot plugin install partner-center-onboarding@marketplace-skills
```

## Feedback

Tried it? Please file a quick **[Trial feedback issue](../../issues/new?template=trial-feedback.yml)**
(one conversation per issue; do not paste sensitive data). A prebuilt Cowork sideload package is in
[`dist/`](dist/).

## References (verify before quoting — labels drift)

- Partner Center roles & permissions: https://learn.microsoft.com/en-us/partner-center/account-settings/permissions-overview
- Distribution options: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/publish
- App submission guide: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/add-in-submission-guide
- Open a developer account: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/open-a-developer-account
- Cowork plugin development: https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development

## License

Dual-licensed: **MIT** for code/configuration and **CC-BY-4.0** for documentation/content.
Copyright Mamoru Kuroda.
