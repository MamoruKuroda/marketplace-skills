# partner-center-onboarding

> 日本語版は [README.ja.md](README.ja.md) を参照してください。

> **EXPERIMENTAL.** Account registration and verification remain **guidance only**: no
> automatic sign-in, role grants, Entra edits, agreements, or submissions. An independent,
> **optional publisher workflow** can use Marketplace Ingestion MCP after human authentication;
> every change requires its own target/before-and-after preview and explicit confirmation.
> No skill asks for or stores passwords, verification codes, or secrets.

A skill set that helps ISVs and partners **self-serve Microsoft Partner Center onboarding**
when publishing to the **Microsoft Marketplace** -- from registration through to publishing a
**Microsoft 365 Copilot agent** or **SaaS offer**.

## Why this exists

Partners most often stall at the onboarding *entrance*: registration, tenant association, the
identity-verification order, publish-path choices (declarative vs custom-engine, offer types,
billing), and channel/tax questions (REO/MPO/CSP, Japan consumption tax). Account verification in
particular -- not the agent build -- is a frequent blocker: sign-in and role confusion,
tenant/App-ID mismatches, publisher/business-existence evidence, and "what stage am I at?"
anxiety. The guidance is collapsed into a single entry-point triage plus a deep verification
specialist and is grounded in public Microsoft documentation rather than private case narratives.

## Who this is for

For software companies and startups (SDC/ISV) onboarding to Partner Center and the
Marketplace, and anyone helping those teams get set up. It's grounded entirely in
**public Microsoft documentation**, so both the company publishing and the people
helping them can use it freely. If your company is already onboarded or has an
offer live, you may not need the account guidance. Authorized, already-onboarded publishers
can separately opt into the publishing workflow below.

## Account guidance: one entrance, one specialist

- **`partner-center-guide` (entry, `user-invocable: true`)** -- broad triage: registration,
  tenant association, publish-path (agent type / offer type / billing), channel/tax
  (REO/MPO/CSP, FX, Japan MoR, purchase-order allocation), SaaS boundary questions, and
  listing/content review (Store validation Must-fix).
  Carries four decision-flow images and a JP tax cheatsheet.
- **`troubleshoot-account-verification` (internal, `user-invocable: false`)** -- the guide
  delegates here when account *verification* is the actual blocker; converges four conditions and
  emits `verification-ledger.json`.

Account questions enter through the guide; verification depth is reached by delegation.
The new publisher workflow is separate and never runs merely because someone asks how to publish.

## Optional Marketplace Ingestion MCP workflow

**Worth adding for publisher-side work, not for account onboarding.**
[`marketplace-publishing`](skills/marketplace-publishing/SKILL.md) discovers current schemas,
reads only the authorized seller/offer scope, builds and validates payloads, and can perform
individually approved draft, upload, and publishing operations. It does not replace account
verification, public Marketplace catalog search, PMX, partner-iq, or Partner Radar.

- A human must sign in and consent in a native secure client flow using an account in the
  **seller-associated tenant**, with appropriate Partner Center roles and **Marketplace
  submission API access**. Other tenants do not work. The plugin does not obtain these rights.
- Start with `getSchema` and a minimal authorized `fetch`. Missing auth, tools, roles, schemas,
  or client support means **BLOCKED** for publishing and **DEGRADED: guidance only**, not success.
- Every `create`, `update`, `delete`, lifecycle `doAction`, upload-URL request, file upload, and
  supported secure credential step needs a separate exact-target/before-and-after preview and
  confirmation. Drafts and price/billing changes count. "Publish my offer" is not blanket
  consent to configure, certify, publish, or any intermediate change.
- Credentials stay outside model context. `uploadCredentials` is not a request for secrets:
  use a verified native secret-blind flow or leave that step human-only in Partner Center.
- Surface validation/errors/job status; verify every write by read-back. Pending is not
  published, and an uncertain write must not be retried automatically.

**Cowork package 4.2.0** uses manifest **1.29** and the actual official endpoint
`https://ingestion-mcp.marketplace-ingestion.mp.microsoft.com/mcp`. Public discovery on
2026-10-27 advertised Dynamic Client Registration (DCR), so the connector intentionally omits
`authorization`; it is **not anonymous**, and contains no placeholder OAuth registration.
No fabricated tool-description file is needed at 1.29. Public metadata is not proof of working
Cowork authentication: **live Cowork connection, consent, tool discovery, and seller access
remain untested**. Microsoft currently documents VS Code and GitHub Copilot CLI clients.
See [setup and authentication evidence](skills/partner-center-guide/references/cowork-setup.md).

**CLI remains opt-in:** the legacy plugin format supports `.mcp.json`/`mcpServers`, but this
release deliberately does not auto-enable a connector for every CLI guidance user. Publishers
can add the same HTTP endpoint with the native `/mcp add` flow documented by Microsoft.
Never put tokens or client secrets in a plugin file. Account guidance needs no connector.

## Try asking (starter prompts)

- 「Partner Center にこれから登録したい。何から始めればいい?」
- 「テナント (Entra ID) の関連付けができない。」
- 「Copilot エージェントを公開したい。宣言型とカスタムエンジン、どっち?」
- 「Publisher Attestation の項目が見当たらない。」
- 「Developer 審査が通らない (登記簿と表記が違う)。」
- 「審査 (Store validation) で sign-up / Contact のリンクが無いと差し戻された。どこを直す?」
- 「CSP 経由販売、円建て/FX、PO 割当の違いを整理したい。」
- 「Marketplace Ingestion MCP を使いたい。前提とスキーマの確認から始め、変更はまだしないで。」

> Full starter list and routing live in
> [`skills/partner-center-guide/SKILL.md`](skills/partner-center-guide/SKILL.md).

## Skills

| Skill | Invocable | Purpose |
| --- | --- | --- |
| [`partner-center-guide`](skills/partner-center-guide) | entry (true) | Broad onboarding triage + publish-path + REO/MPO + JP tax; flow images + cheatsheet |
| [`troubleshoot-account-verification`](skills/troubleshoot-account-verification) | internal (false) | Deep account-verification diagnosis; 4-condition convergence + `verification-ledger.json` |
| [`marketplace-publishing`](skills/marketplace-publishing) | explicit opt-in (true) | Publisher-side MCP workflow; schema-first reads/validation and separately approved mutations |

## Relationship to `agent-publishing`

`agent-publishing` decides **what to build and how to submit** (agent type / monetization /
submission worksheet). The account skills in `partner-center-onboarding` handle getting the **account itself verified**
so you *can* submit. The separate optional publisher workflow adds guarded execution through
the official API connector; it does not duplicate agent-building or monetization implementation.

## Portability (CLI + Cowork)

Skills here are portable **Agent Skills** (`SKILL.md`, the open standard). They run as-is in
**GitHub Copilot CLI**, and the `skills/` folder can be packaged into a Microsoft 365 app package
(`.zip` with `manifest.json` + icons) for **Microsoft 365 Copilot Cowork**
([packaging guide](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development)).
They avoid slash-only invocation and sub-agents (not yet supported in Cowork) and rely on
natural-language triggers.

## Build and validate (no seller operations)

From the repository root, using Windows PowerShell 5.1 and Python with the dependencies in
[`tests/requirements.txt`](tests/requirements.txt):

```powershell
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy RemoteSigned -File .\plugins\partner-center-onboarding\build-cowork-zip.ps1
python -B .\plugins\partner-center-onboarding\tests\test_package.py
```

Tests check the actual ZIP, official 1.29 JSON schema, fixed app ID, versions, frontmatter,
skill/companion limits, preserved guidance/assets, connector/auth configuration, and static
behavior contracts. They fetch only the public manifest schema, make no seller calls, and do
not prove live client behavior or enforce approvals independently of the host.
`RemoteSigned` is process-scoped, does not change persistent settings, and does not override
organization-enforced execution policy.

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
- Distribution options: https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/publish
- App submission guide: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/add-in-submission-guide
- Open a developer account: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/open-a-developer-account
- Cowork plugin development: https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development
- Marketplace Ingestion MCP: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/ingestion-mcp
- CLI plugin configuration: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference

## License

Dual-licensed: **MIT** for code/configuration and **CC-BY-4.0** for documentation/content.
Copyright Mamoru Kuroda.
