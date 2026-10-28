# partner-center-onboarding

> 日本語版は [README.ja.md](README.ja.md) を参照してください。

> **EXPERIMENTAL.** Account registration and verification remain **guidance only**: no
> automatic sign-in, role grants, Entra edits, agreements, or submissions. An independent,
> **optional publisher workflow** needs actual runtime tools and human authentication;
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
- Check runtime tool availability first. When no tools/server are exposed to the conversation,
  stop with `BLOCKED: 接続ツールが会話に出ていない`; do not infer an auth or seller-rights failure.
  Only after tools are available, start with `getSchema` and a minimal authorized `fetch`.
  Explicit access errors can block publishing; untested prerequisites stay **UNVERIFIED**.
  Account guidance remains **DEGRADED: guidance only**, not a claim that the connector works.
- Every `create`, `update`, `delete`, lifecycle `doAction`, upload-URL request, file upload, and
  supported secure credential step needs a separate exact-target/before-and-after preview and
  confirmation. Drafts and price/billing changes count. "Publish my offer" is not blanket
  consent to configure, certify, publish, or any intermediate change.
- Credentials stay outside model context. `uploadCredentials` is not a request for secrets:
  use a verified native secret-blind flow or leave that step human-only in Partner Center.
- Surface validation/errors/job status; verify every write by read-back. Pending is not
  published, and an uncertain write must not be retried automatically.

**Cowork package 4.2.1 / CLI 0.7.1 is a diagnostic-only candidate, not a live release.**
It retains manifest **1.29**, the existing app ID and connector, and the actual official endpoint
`https://ingestion-mcp.marketplace-ingestion.mp.microsoft.com/mcp`. Public discovery on
2026-10-27 advertised Dynamic Client Registration (DCR), so the connector intentionally omits
`authorization`; it is **not anonymous**, and contains no placeholder OAuth registration.
No fabricated tool-description file is needed at 1.29. Public metadata is not proof of working
Cowork authentication: **successful runtime discovery, consent, and seller access remain
unverified**. The availability/runtime gap below is observed, not fixed by this candidate.
Microsoft currently documents VS Code and GitHub Copilot CLI clients.
See [setup and authentication evidence](skills/partner-center-guide/references/cowork-setup.md).

## Known issue: available connector, no runtime tools

Evidence boundary as of **2026-10-28**; this is a generic technical observation, not an account
or tenant diagnosis. Package/connector availability is not discovered, runtime, or authenticated
tool access. This candidate corrects diagnostics only; it does not claim to repair the connection.

| Track | State | What is established |
| --- | --- | --- |
| Earlier reported UI/runtime observation | **VERIFIED** | Plugin enabled, three skills and Marketplace Ingestion shown as available; no server/tools exposed to the conversation. No visible sign-in/consent control was found in the checked chat, Sources & Skills, or plugin-details surfaces. |
| Reported fresh Cowork task | **VERIFIED**, limited | A genuinely new task created on 2026-10-28 reports enabled/active configuration, three skills and connector availability, but actual tool-search for Ingestion/MCP names finds zero matching servers/tools. No visible sign-in or error appears in that conversation; no seller tool/auth is called. |
| H1: static package/schema checks | **VERIFIED**, limited | The unchanged 4.2.0 baseline passes the current first-party 1.29 schema and 15 repository tests; the installed Microsoft manifest helper also passes offline schema validation. This is not platform deep validation or proof of runtime tool discovery. |
| Reported public-wire discovery difference | **VERIFIED**, limited | Origin metadata advertises DCR, but the two checked OAuth metadata locations at its advertised Entra issuer return 404. The issuer's OIDC `openid-configuration` returns 200 without `registration_endpoint`. This does not establish which path Cowork selects or a runtime failure there. |
| Reported unauthenticated protocol responses | **VERIFIED**, limited | `initialize` and `tools/list` POSTs return 401 for both `copilot-cowork` and the comparison User-Agent; no distinguishing User-Agent response was observed. 401 alone is normal protected behavior, not a root cause. |
| Reported native CLI host status | **VERIFIED**, pre-auth only | GitHub Copilot CLI 1.0.101, with session-only `--additional-mcp-config` and unrelated MCPs disabled, repeatedly emits `session.mcp_server_status_changed` with `pending -> needs-auth`. This is a host-state observation, not successful login or tool listing. |
| H2/H3/H4/H5 | **UNVERIFIED** | The discovery-path/metadata difference is observed, but Cowork's selected metadata path, actual DCR/OAuth execution, permissions, policy and root cause still need client/server evidence. |
| Publisher workflow without runtime tools | **BLOCKED** | Report only `BLOCKED: 接続ツールが会話に出ていない` and stop before schema calls, seller access or writes. Existing account guidance remains useful. |

**Checked:** the reported UI/runtime surfaces, fresh-task tool search, public unauthenticated wire
observations and native CLI structured host-status events above.
**Unchecked:** Cowork's selected metadata path and transport/backend traces, server logs,
authenticated OAuth/DCR outcomes, seller-role/API access, other sign-in surfaces, and authenticated
native-client/tool-listing results. Do not claim access to hidden logs,
promise a sign-in control in Sources & Skills or plugin details, or send the user to an unverified
sign-in screen. A conversation-sandbox DNS/HTTP failure describes that sandbox path only;
it does not establish what the Cowork connector backend can reach or which prerequisite failed.
No seller access or writes were performed in the reported test.

An old pre-update conversation alone does not explain the fresh-task reproduction.
Backend cache is not ruled out. The new-task configuration/availability flags still do not
establish runtime tools, and the earlier panel checks are not a claim that every panel was
rechecked in that fresh task.

Structured host events take precedence over model narrative for the native `needs-auth` status,
even if model prose reports no startup information. No browser auth or seller-account selection
occurred, and no seller tools were executed. This is not a same-seller-account login test.
Authenticated native-client success and tool listing remain **BLOCKED / UNVERIFIED** pending a
separately authorized human OAuth/consent action in a verified native flow. The skill must not
silently initiate sign-in, open an auth browser, select an account, or grant consent.
That is a skill safety rule, not a claim about unverified host UI behavior.

The reported 2026-10-28 origin protected-resource metadata returns 200 and advertises
`https://login.microsoftonline.com/common/v2.0`; origin authorization-server metadata returns
200 with that issuer, the origin `/register` endpoint, and PKCE `S256` (the same listed fields as
2026-10-27). That advertisement is not proof a client can discover or use DCR.
The [setup evidence](skills/partner-center-guide/references/cowork-setup.md) records the exact
two 404 OAuth paths and the 200 OIDC path. The OIDC issuer uses a `/{tenantid}/v2.0` template and
does not advertise a registration endpoint. Actual selected metadata path plus client/server
logs are still needed; the unauthenticated 401 comparison does not establish post-auth tool visibility.
No authentication or client registration was performed in those probes.

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
Set `COWORK_BASELINE_ZIP` to a preserved 4.2.0 ZIP to also compare connector configuration,
account skills and assets byte-for-byte; that comparison is reported as skipped when no baseline
is provided. `COWORK_MANIFEST_SCHEMA` can point to a previously downloaded official schema for
an offline rerun.
These checks are **not** `wiqd plugin validate --mode deep` or an **AppValidationLibrary** run.
`wiqd` is not installed in the validation environment. Installed ATK **1.1.11** package-rule
validation requests an M365 token and remote portal validation, so it was not invoked.
The installed `@microsoft/app-manifest` **1.0.6** helper was used with an explicit local schema;
it covers schema only, not skills/connector platform rules. No schema downgrade was made to
accommodate older tooling.
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
