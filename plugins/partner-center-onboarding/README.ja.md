# partner-center-onboarding（Partner Center オンボーディング）

> **実験的（EXPERIMENTAL）プロジェクトです。** 登録・本人確認は引き続き**ガイド専用**で、サインイン、
> ロール付与、Entra 編集、契約同意、提出を代行しません。独立した**任意の発行者ワークフロー**は本人による
> 実行時ツールの存在と本人による認証が前提で、変更は毎回、対象・変更前後を提示し個別承認後に限ります。
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
- まず会話に実行時ツールが出ているかを確認します。ツール/server がない場合は
  `BLOCKED: 接続ツールが会話に出ていない` のみを返して停止し、認証失敗や販売者権限不足と推定しません。
  ツールがある場合だけ `getSchema` と対象を絞った承認済み `fetch` へ進みます。明示的なアクセスエラーは
  公開操作を停止する根拠になりますが、未検証の前提は **UNVERIFIED** のままです。
  アカウント案内は **DEGRADED: guidance only** として継続でき、接続成功を意味しません。
- `create`、`update`、`delete`、`doAction`、アップロード URL 取得、ファイル転送、安全な資格情報設定の
  **操作ごとに**対象と変更前後を確認し、別々の承認を得ます。下書き・価格・課金の変更も対象です。
  「Offer を公開して」は configure・certify・publish や途中の変更すべてへの包括承認ではありません。
- シークレットはモデルへ渡しません。`uploadCredentials` があっても秘密情報を求めず、秘密値がモデルを通らない
  安全なネイティブ入力が確認できなければ Partner Center で本人が設定します。
- 検証結果・エラー・ジョブ状態を示し、変更後は再取得して確認します。Pending を公開済みとせず、
  結果不明の書き込みを自動再試行しません。

**Cowork 4.2.1 / CLI 0.7.1 は診断文書のみを修正する候補で、未公開です。**
manifest **1.29**、既存 app ID・コネクタ、公式エンドポイント
`https://ingestion-mcp.marketplace-ingestion.mp.microsoft.com/mcp` は変更しません。
2026-10-27 の公開メタデータが Dynamic Client Registration（DCR）を示すため、`authorization` は省略しています。
**匿名認証ではなく**、架空の OAuth 登録 ID も入れていません。1.29 では架空のツール記述ファイルは不要です。
ただしメタデータ確認は Cowork での動作証明ではなく、**実行時ツール検出の成功・同意・販売者アクセスは未確認**です。
下記の「利用可能表示と実行時ツールの差」は観測済みですが、本候補で接続を修復したとは主張しません。
サーバー公式文書が挙げるクライアントは現在 VS Code と GitHub Copilot CLI です。
[セットアップ・認証の根拠](skills/partner-center-guide/references/cowork-setup.md)を参照してください。

## 既知の問題：利用可能なコネクタが会話にツールを出さない

**2026-10-28** 時点の汎用的な技術観測です。個別アカウントやテナントの診断ではありません。
パッケージ/コネクタの利用可能表示と、検出済み・実行時・認証済みのツールは別です。
本候補は診断表現の修正に限り、接続の原因解決を保証しません。

| 調査・対象 | 状態 | 確認できた範囲 |
| --- | --- | --- |
| 先に報告された実機 UI・実行時観測 | **VERIFIED** | プラグイン有効、3 スキルと Marketplace Ingestion の利用可能表示を確認。一方、会話に server/ツールはなく、確認したチャット・Sources & Skills・プラグイン詳細ではサインイン/同意の操作は見つかりませんでした。 |
| 報告された Cowork 新規タスク | **VERIFIED**（限定的） | 2026-10-28 に新規作成したタスクでも構成は enabled/active、3 スキル・コネクタ利用可能。一方、Ingestion/MCP 名の実際のツール検索では該当 server/ツールは 0 件。その会話に可視のサインイン/エラーはなく、販売者ツール/認証は呼んでいません。 |
| H1：静的なパッケージ/スキーマ確認 | **VERIFIED**（限定的） | 変更前の 4.2.0 ZIP は最新の公式 1.29 スキーマと既存テスト 15 件に合格。既存の Microsoft manifest ヘルパーによるオフラインのスキーマ確認も合格。ただしプラットフォームの deep 検証や実行時ツール検出の証明ではありません。 |
| 報告された公開 wire の発見経路差 | **VERIFIED**（限定的） | origin は DCR を広告しますが、広告された Entra issuer の確認した OAuth メタデータ 2 経路は 404。OIDC `openid-configuration` は 200 で `registration_endpoint` がありません。Cowork がどの経路を選ぶか、そこで実行時に失敗するかは未確認です。 |
| 報告された未認証のプロトコル応答 | **VERIFIED**（限定的） | `initialize` と `tools/list` の POST は `copilot-cowork` と比較 User-Agent の双方で 401。区別できる User-Agent 別応答は観測されませんでした。401 単独は保護された通常の挙動で、根本原因ではありません。 |
| 報告されたネイティブ CLI ホスト状態 | **VERIFIED**（認証前のみ） | GitHub Copilot CLI 1.0.101、セッション限定の `--additional-mcp-config`、無関係の MCP を無効にした比較で、`session.mcp_server_status_changed` の `pending -> needs-auth` が繰り返し記録されました。ログイン成功・ツール一覧取得の証明ではありません。 |
| H2/H3/H4/H5 | **UNVERIFIED** | 発見経路・メタデータの差は観測済みですが、Cowork が選択したメタデータ経路、実際の DCR/OAuth、権限、ポリシー、根本原因は引き続きクライアント/サーバー側の証拠待ちです。 |
| 実行時ツールのない発行者ワークフロー | **BLOCKED** | `BLOCKED: 接続ツールが会話に出ていない` のみを返し、スキーマ呼び出し・販売者参照・書き込みの前に停止。既存アカウント案内は継続できます。 |

**確認済みの面:** 上記の UI・新規タスクの実際のツール検索、未認証の公開 wire、ネイティブ CLI の構造化ホスト状態。
**未確認の面:** Cowork が選択したメタデータ経路や通信/バックエンド追跡、サーバーログ、認証後の OAuth/DCR 結果、
販売者ロール/API アクセス、他の認証画面、ネイティブクライアントの認証後の成功・ツール一覧です。
非表示ログを見たと主張せず、Sources & Skills や詳細画面に
サインインが出ると約束したり、その操作の存在を確認していない画面へ誘導したりしません。
会話サンドボックスの DNS/HTTP 失敗はその経路の観測に限られ、Cowork 接続バックエンドの到達性や失敗した前提を
確定するものではありません。報告されたテストで販売者参照・書き込みは行っていません。

更新前からの古い会話だけを使ったという説明では、この新規タスクの再現は説明できません。
ただしバックエンドのキャッシュは除外していません。構成/利用可能フラグは依然として実行時ツールの証明ではなく、
先のパネル確認を新規タスクで全パネルを再確認したという意味には扱いません。

ネイティブ比較の `needs-auth` はモデル文章より構造化ホストイベントを優先して扱います。
モデルが起動情報なしと述べても、ホスト状態を否定する根拠にはしません。ブラウザー認証の開始や販売者アカウント選択はなく、
販売者ツールも実行していません。同じ販売者アカウントでのログインを試したものではありません。
認証後のネイティブ接続成功・ツール一覧は、別途許可された本人による確認済みネイティブ経路の OAuth/同意まで
**BLOCKED / UNVERIFIED** です。本スキルから黙ってサインイン、認証ブラウザー起動、アカウント選択、同意を指示・実行しません。
これはスキルの停止規則であり、未確認のホスト UI 挙動を保証する説明ではありません。

2026-10-28 の報告では、origin の protected-resource は 200 で
`https://login.microsoftonline.com/common/v2.0` を広告し、origin の authorization-server も 200 で、
同 issuer・origin の `/register`・PKCE `S256` を返しました（この列挙した項目は 2026-10-27 と同じ）。
ただし広告は、クライアントが DCR を発見・利用できる証明ではありません。
[セットアップの証拠表](skills/partner-center-guide/references/cowork-setup.md)に OAuth の 404 の 2 経路と
OIDC の 200 の経路を記録しました。OIDC の issuer は `/{tenantid}/v2.0` のテンプレートで、登録エンドポイントはありません。
実際の選択経路とクライアント/サーバーログが必要で、未認証 401 の比較から認証後のツール可視性までは判定できません。
これは発見経路・メタデータ差の観測であり、Cowork の根本原因の証明ではありません。
これらのプローブで認証・クライアント登録は行っていません。

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
保存済み 4.2.0 ZIP のパスを `COWORK_BASELINE_ZIP` に指定すると、コネクタ設定・アカウントスキル・添付を
バイト単位でも比較します。未指定ならその比較は skipped と表示します。取得済み公式スキーマのパスを
`COWORK_MANIFEST_SCHEMA` に指定すればオフラインで再実行できます。
これらは `wiqd plugin validate --mode deep` や **AppValidationLibrary** の実行ではありません。
検証環境に `wiqd` はありません。既存 ATK **1.1.11** のパッケージ規則検証は M365 トークンとリモートの
ポータル検証を使うため、呼び出していません。既存 `@microsoft/app-manifest` **1.0.6** ヘルパーには
取得済みローカルスキーマを明示して確認しましたが、対象はスキーマのみで、スキル/コネクタのプラットフォーム規則は
検証しません。古いツールに合わせたスキーマのダウングレードはしていません。
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
