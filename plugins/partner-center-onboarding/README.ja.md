# partner-center-onboarding（Partner Center オンボーディング）

> **実験的（EXPERIMENTAL）プロジェクトです。** 登録・本人確認は引き続き**ガイド専用**で、サインイン、
> ロール付与、Entra 編集、契約同意、提出を代行しません。独立した**任意の発行者ワークフロー**は本人による
> 認証後に Marketplace Ingestion MCP を利用できますが、変更は毎回、対象・変更前後を提示し個別承認後に限ります。
> パスワード・確認コード・シークレットを尋ねたり保存したりしません。

> このドキュメントは日本語版です。正本は英語版 [README.md](README.md) です。内容に差異がある場合は英語版を優先します。

ISV・パートナーが **Microsoft Marketplace** へ公開する際の **Partner Center オンボーディング**（アカウント登録
〜テナント関連付け〜本人確認〜 **Microsoft 365 Copilot エージェント**／**SaaS Offer** の公開）を自走できるよう
案内するスキル集です。

## なぜ必要か

つまずきの多くはオンボーディングの**入口**で起きます——登録、テナント関連付け、本人確認の順序、公開パスの選択
（宣言型 vs カスタムエンジン、Offer 種別、課金）、商流・税務（REO/MPO/CSP、日本の消費税）。とりわけ
**アカウント検証**はエージェント作成ではなく頻出のブロッカーです（サインイン／ロール混乱、テナント・App ID の
不一致、発行元・会社実在の証明、「今どの段階？」の不安）。非公開事例ではなく公開 Microsoft ドキュメントを根拠に、
**ひとつの入口トリアージ＋検証の専門スキル**へ集約しています。

## 想定ユーザー (Who this is for)

Partner Center と Marketplace へオンボードするソフトウェア企業・スタートアップ (SDC/ISV) と、
そうしたチームの立ち上げを手伝う人のために作られています。内容はすべて **公開されている
Microsoft のドキュメント** に基づくため、公開する企業側でも、公開を手伝う側でも自由に活用
できます。すでにオンボード済み、または Offer 公開済みの企業やその Microsoft 担当者には
アカウント案内は不要かもしれません。オンボード済みの権限を持つ発行者は、別途、下記の任意ワークフローを利用できます。

## アカウント案内：入口は1つ、専門家は1つ

- **`partner-center-guide`（入口・`user-invocable: true`）** — 広域トリアージ：登録、テナント関連付け、
  公開パス（エージェント種別／Offer 種別／課金）、商流・税務・購買（REO/MPO/CSP、FX、日本 MoR、PO 割当）、
  SaaS 境界、リスティング/コンテンツ審査（Store validation の Must-fix）。意思決定フロー画像4枚と
  日本税務チートシートを同梱。
- **`troubleshoot-account-verification`（内部・`user-invocable: false`）** — アカウント*検証*が実際の
  ブロッカーのとき入口から委譲。4条件へ収束させ `verification-ledger.json` を出力。

アカウント相談は入口（guide）から入り、検証の深掘りは委譲で到達します。新しい発行者ワークフローは別枠で、
一般的な「公開方法を教えて」だけでは起動しません。

## 任意の Marketplace Ingestion MCP ワークフロー

**発行者側の公開作業には追加する価値がありますが、アカウント登録・検証には不要です。**
[`marketplace-publishing`](skills/marketplace-publishing/SKILL.md) は最新スキーマ、承認された販売者・Offer 範囲の
参照、ペイロード作成・検証を扱い、下書き・アップロード・公開操作は個別承認後に限って実行します。
本人確認、公開カタログ検索、PMX、partner-iq、Partner Radar の代わりではありません。

- **販売者に関連付いたテナント**のアカウント、適切な Partner Center ロール、
  **Marketplace submission API アクセス**が必要です。本人がクライアントの安全な認証画面でサインイン・同意します。
  別テナントでは動作せず、本プラグインが権限を取得することもありません。
- `getSchema` と対象を絞った承認済み `fetch` から開始します。認証・ツール・権限・スキーマ・対応クライアントが
  不足する場合、公開操作は **BLOCKED**、案内は **DEGRADED: guidance only** と明示します。
- `create`、`update`、`delete`、`doAction`、アップロード URL 取得、ファイル転送、安全な資格情報設定の
  **操作ごとに**対象と変更前後を確認し、別々の承認を得ます。下書き・価格・課金の変更も対象です。
  「Offer を公開して」は configure・certify・publish や途中の変更すべてへの包括承認ではありません。
- シークレットはモデルへ渡しません。`uploadCredentials` があっても秘密情報を求めず、秘密値がモデルを通らない
  安全なネイティブ入力が確認できなければ Partner Center で本人が設定します。
- 検証結果・エラー・ジョブ状態を示し、変更後は再取得して確認します。Pending を公開済みとせず、
  結果不明の書き込みを自動再試行しません。

**Cowork 4.2.0 / manifest 1.29** に公式エンドポイント
`https://ingestion-mcp.marketplace-ingestion.mp.microsoft.com/mcp` を追加しました。
2026-10-27 の公開メタデータが Dynamic Client Registration（DCR）を示すため、`authorization` は省略しています。
**匿名認証ではなく**、架空の OAuth 登録 ID も入れていません。1.29 では架空のツール記述ファイルは不要です。
ただしメタデータ確認は Cowork での動作証明ではなく、**実機接続・同意・ツール検出・販売者アクセスは未検証**です。
サーバー公式文書が挙げるクライアントは現在 VS Code と GitHub Copilot CLI です。
[セットアップ・認証の根拠](skills/partner-center-guide/references/cowork-setup.md)を参照してください。

**CLI は明示的な追加方式のままです。** 現行形式は `.mcp.json` / `mcpServers` に対応しますが、案内だけを使う全員へ
自動接続を追加しないため、本版には同梱しません。発行者は Microsoft の手順に従いネイティブの `/mcp add` で同じ
HTTP エンドポイントを追加できます。トークンやクライアントシークレットをプラグインへ保存しないでください。
アカウント案内はコネクタ不要です。

## 試しに聞いてみる（スターター）

- 「Partner Center にこれから登録したい。何から始めればいい?」
- 「テナント (Entra ID) の関連付けができない。」
- 「Copilot エージェントを公開したい。宣言型とカスタムエンジン、どっち?」
- 「Publisher Attestation の項目が見当たらない。」
- 「Developer 審査が通らない (登記簿と表記が違う)。」
- 「審査 (Store validation) で sign-up / Contact のリンクが無いと差し戻された。どこを直す?」
- 「CSP 経由販売、円建て/FX、PO 割当の違いを整理したい。」
- 「Marketplace Ingestion MCP を使いたい。前提とスキーマの確認から始め、変更はまだしないで。」

> 全リストとルーティングは
> [`skills/partner-center-guide/SKILL.md`](skills/partner-center-guide/SKILL.md) を参照。

## 収録スキル

| スキル | 起動 | 役割 |
| --- | --- | --- |
| [`partner-center-guide`](skills/partner-center-guide) | 入口 (true) | 広域オンボーディングのトリアージ＋公開パス＋REO/MPO＋日本税務。フロー画像＋チートシート |
| [`troubleshoot-account-verification`](skills/troubleshoot-account-verification) | 内部 (false) | アカウント検証の深掘り診断。4条件収束＋`verification-ledger.json` |
| [`marketplace-publishing`](skills/marketplace-publishing) | 明示的な選択 (true) | 発行者向け MCP。スキーマ優先の参照・検証と、操作ごとの承認付き変更 |

## `agent-publishing` との関係

`agent-publishing` は「**何を作り、どう提出するか**」（エージェント種別／収益化／提出ワークシート）を扱います。
`partner-center-onboarding` のアカウントスキルは、提出できるように**アカウント自体を検証済みにする**ことを扱います。
別の任意ワークフローは公式 API コネクタによる慎重な実行を追加しますが、エージェント作成・収益化の実装は扱いません。

## 配布先（CLI＋Cowork）

本スキルは移植性のある **Agent Skill**（`SKILL.md`、オープン標準）です。**GitHub Copilot CLI** ではそのまま
動作し、`skills/` フォルダーを Microsoft 365 アプリ パッケージ（`manifest.json`＋アイコン入りの `.zip`）に
すれば **Microsoft 365 Copilot Cowork** 用に配布できます
（[パッケージング手順](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development)）。
スラッシュコマンド専用の起動やサブエージェントには依存せず（Cowork 未対応のため）、説明文の自然言語トリガーで
発火します。

## ビルドと検証（販売者操作なし）

リポジトリのルートから Windows PowerShell 5.1 と Python を使います。
Python の前提は [`tests/requirements.txt`](tests/requirements.txt) です。

```powershell
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy RemoteSigned -File .\plugins\partner-center-onboarding\build-cowork-zip.ps1
python -B .\plugins\partner-center-onboarding\tests\test_package.py
```

実際の ZIP、公式 1.29 JSON スキーマ、固定 app ID、版番号、frontmatter、スキル・添付制限、既存ガイド・画像、
接続・認証設定、静的な実行契約を確認します。取得するのは公開 manifest スキーマのみで、販売者 API は呼びません。
実機動作やホストとは独立した承認の強制を証明するテストではありません。
`RemoteSigned` はこのプロセスだけに適用し、永続設定や組織で強制された実行ポリシーは変更しません。

## インストール

```bash
copilot plugin marketplace add MamoruKuroda/marketplace-skills
copilot plugin install partner-center-onboarding@marketplace-skills
```

## 参考資料（引用前に必ず確認——表記は変わり得ます）

- Partner Center のロールと権限: https://learn.microsoft.com/en-us/partner-center/account-settings/permissions-overview
- 配布オプション: https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/publish
- アプリ提出ガイド: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/add-in-submission-guide
- 開発者アカウントの開設: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/open-a-developer-account
- Cowork プラグイン開発: https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development
- Marketplace Ingestion MCP: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/ingestion-mcp
- CLI プラグイン構成: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference

## ライセンス

デュアル ライセンスです。コード・構成は **MIT**、ドキュメント・コンテンツは **CC-BY-4.0**。
著作権は Mamoru Kuroda。
