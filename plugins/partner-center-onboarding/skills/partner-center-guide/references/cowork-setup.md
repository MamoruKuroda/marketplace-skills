# Cowork へのセットアップ（partner-center-guide）

アカウント登録・テナント関連付け・本人確認は引き続き **知識・対話ガイド型**で、コネクタや認証は不要です。
`partner-center-guide` と `troubleshoot-account-verification` は同梱の知識・図・チートシートで案内し、
サインイン、ロール付与、Entra 編集、提出は代行しません。

4.2.0 では別の任意スキル `marketplace-publishing` と公式 Marketplace Ingestion MCP 接続を追加しました。
4.2.1 / CLI 0.7.1 は診断文書のみを修正する候補で、未公開です。app ID・コネクタ設定は変えません。
発行者がこの接続の利用を明示した場合だけ別契約で進めます。接続・認証が使えなければ公開操作は **BLOCKED**、
既存の案内は **DEGRADED: guidance only** と明示して継続します。ホストがパッケージ自体を読み込めない場合は、
その互換性エラーを報告し、接続済み・利用可能と偽りません。

## 任意の発行者接続：認証と確認済みの範囲

- 公式エンドポイント: `https://ingestion-mcp.marketplace-ingestion.mp.microsoft.com/mcp`
- パッケージ候補: manifest **1.29** / app **4.2.1**。`agentConnectors` の ID は `market-ingest`。
  `mcpToolDescription` は不要なので、架空のツールスキーマは同梱しません。
- **DCR の公開証拠（2026-10-27、未認証 GET のみ）**:
  - `https://ingestion-mcp.marketplace-ingestion.mp.microsoft.com/.well-known/oauth-protected-resource`
    は HTTP 200、resource は上記 `/mcp`、authorization server は
    `https://login.microsoftonline.com/common/v2.0`。
  - `https://ingestion-mcp.marketplace-ingestion.mp.microsoft.com/.well-known/oauth-authorization-server`
    は HTTP 200、`registration_endpoint` は
    `https://ingestion-mcp.marketplace-ingestion.mp.microsoft.com/register`、
    `code_challenge_methods_supported` は `S256`。
  - `/mcp` への GET は 405 / Allow: POST でした。GET の失敗だけで認証不可とは判定しません。
  - クライアント登録、認証、同意、`tools/call`、販売者レコード操作は実行していません。
- Cowork の公式 DCR 手順に従い `authorization` を省略しています。これは匿名の `None` ではなく、
  実在しない `OAuthPluginVault.referenceId` の代用でもありません。メタデータが変わり DCR が利用できない場合は
  接続を停止します。別の OAuth 登録が必要なら管理者・本人の安全な設定で実在する参照を得るまで **BLOCKED** です。
  プレースホルダー、`None`、トークン直書きで回避しません。
- **実機観測と未確認事項を分ける**: メタデータは DCR の広告を示すだけです。4.2.0 の利用可能表示と
  実行時ツール不在は下記の観測ですが、Cowork による登録・認証・同意・ツール検出の成功、ファイル転送、
  販売者アクセスの証明ではありません。サーバー公式文書が挙げるクライアントは **VS Code / GitHub Copilot CLI**。
  認証・互換性・ポリシーを原因として確定する証拠はまだありません。

実行時ツールと実際のネイティブ認証経路が確認できた場合に限り、本人が販売者に関連付いたテナントのアカウントで
安全な認証画面にサインイン・同意し、適切な Partner Center ロールと Marketplace submission API アクセスを
確認します。他テナントでは利用できないという API の前提と、今回のツール不在の原因は別です。
チャット・Sources & Skills・プラグイン詳細にサインインが現れるとは約束せず、存在が未確認の認証画面へ誘導しません。
パスワード、MFA コード、クライアントシークレット、トークンを会話や設定ファイルへ入力させません。
案内だけの利用で認証を完了する必要はなく、認証を代行したり開始したりしません。

会話に接続ツール/server がない場合の応答は `BLOCKED: 接続ツールが会話に出ていない` のみにして停止します。
この場合は `getSchema` や `fetch` も呼びません。ツールが実際に出た場合だけ、その入力スキーマと
`getSchema`、許可された最小範囲の `fetch` へ進みます。
保存・下書き作成・アップロード URL 取得・ファイル転送・価格/課金変更・certify・publish・unpublish・delete は
すべて変更として扱い、**操作ごとに対象・変更前後を提示し別々の承認**を得ます。「公開して」は包括承認ではありません。
`uploadCredentials` でも秘密値はモデルへ渡さず、安全なネイティブ入力が確認できなければ本人がポータルで行います。
Pending/エラー/結果不明を成功とせず、変更後は `fetch` で再確認し、結果不明の書き込みを自動再試行しません。
詳細な実行契約は `marketplace-publishing/SKILL.md` を参照してください。

CLI の現行プラグイン形式は `.mcp.json` / `mcpServers` に対応しますが、ガイド利用者へ自動接続を追加しないため
本版では同梱しません。発行者は公式手順のネイティブ `/mcp add` で名前 `marketplace-ingestion`、Type `HTTP`、
上記 URL を追加できます。インストール済みの設定・キャッシュは変更していません。

公式根拠（2026-10-27 fetch）:
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/ingestion-mcp
- https://learn.microsoft.com/en-us/copilot/cowork/cowork-plugin-development
- https://developer.microsoft.com/json-schemas/teams/v1.29/MicrosoftTeams.schema.json
- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference

## 既知の問題と証拠の境界（2026-10-28）

パッケージ/コネクタが「利用可能」でも、検出済み・実行時・認証済みのツールとは限りません。
4.2.1 はこの切り分けと停止応答を直す候補であり、接続の原因解決を実証した版ではありません。

| 対象 | 状態 | 確認したこと / 確認していないこと |
| --- | --- | --- |
| 先に報告された UI・会話の実行時観測 | **VERIFIED** | プラグイン有効、3 スキル、Marketplace Ingestion の利用可能表示。一方、会話に server/ツールはなく、確認したチャット・Sources & Skills・プラグイン詳細にサインイン/同意の操作は見つかりませんでした。 |
| 報告された Cowork 新規タスク | **VERIFIED**（限定的） | 2026-10-28 に新規作成したタスクの構成も enabled/active、3 スキル、コネクタ利用可能。Ingestion/MCP 名の実際のツール検索は該当 server/ツール 0 件で、その会話に可視のサインイン/エラーはありません。販売者ツール/認証は呼んでいません。 |
| H1：静的スキーマ・ZIP | **VERIFIED**（静的範囲のみ） | 4.2.0 の保存済みベースラインは最新の公式 1.29 スキーマと既存テスト 15 件に合格。既存 `@microsoft/app-manifest` 1.0.6 のオフラインのスキーマ確認も合格。実行時発見やプラットフォーム規則の deep 検証ではありません。 |
| 報告された公開 wire の発見経路差 | **VERIFIED**（限定的） | 下記の origin の DCR 広告と Entra issuer 側の発見経路・メタデータに差があります。Cowork の選択経路や実際の失敗を示すログではありません。 |
| 報告されたネイティブ CLI ホスト状態 | **VERIFIED**（認証前のみ） | GitHub Copilot CLI 1.0.101 のセッション限定 `--additional-mcp-config`、無関係 MCP 無効の比較で、`session.mcp_server_status_changed` が `pending -> needs-auth` を繰り返しました。認証成功やツール一覧の取得ではありません。 |
| H2/H3/H4/H5 | **UNVERIFIED** | 公開 wire の差は観測済みですが、Cowork が選択したメタデータ経路、DCR/OAuth の実行、権限、ポリシー、根本原因は追加のクライアント/サーバー側証拠待ちです。 |
| 実行時ツール不在 | **BLOCKED** | `BLOCKED: 接続ツールが会話に出ていない` のみを返し、スキーマ呼び出し・販売者参照・書き込みの前に停止。アカウント案内は継続できます。 |

確認済みは上記の報告された画面・新規タスクのツール検索、ネイティブ CLI の構造化ホスト状態、
下記の未認証の公開 wire 観測範囲です。未確認は Cowork が選択したメタデータ経路・通信/バックエンド追跡、
サーバーログ、認証後の結果、販売者ロール/API アクセス、他の認証画面です。非表示ログを見たとは主張しません。
可視のサインインが見つからないことを「認証失敗」「販売者権限不足」と読み替えません。
会話サンドボックスからの DNS/HTTP 失敗は、その経路の観測であり、Cowork 接続バックエンドの到達性を
実証するものではありません。報告されたテストで販売者参照・書き込みは行っていません。

### 新規タスクとネイティブ比較の境界（2026-10-28 報告）

単に更新前からの古い会話だけを使ったという説明では、新規タスクでも同じ不在を再現したことを説明できません。
ただしバックエンドのキャッシュは除外していません。構成の enabled/active、3 スキル、
Marketplace Ingestion の利用可能表示と、実際のツール検索で 0 件という観測を分けます。
先の Sources & Skills・プラグイン詳細の確認を、新規タスクで全パネルを再確認したとは記載しません。

ネイティブ GitHub Copilot CLI 1.0.101 の比較は `--additional-mcp-config` によるセッション限定で、
無関係 MCP は無効、認証/販売者ツール実行なしです。`session.mcp_server_status_changed` の
`pending -> needs-auth` という構造化ホストイベントを、起動情報なしというモデル文章より優先します。
この状態は認証要求の観測であり、認証の完了、同じ販売者アカウントでの接続成功、
認証後のツール発見の証明ではありません。

ブラウザー認証の開始や販売者アカウントの選択はありません。同じ販売者アカウントでのログインを試したものではありません。
認証後のネイティブ接続成功・ツール一覧取得は **BLOCKED / UNVERIFIED** のままで、別途許可された
本人による確認済みネイティブ経路の OAuth/同意が必要です。本スキルが黙ってサインインを開始したり、
ブラウザーを開いたり、アカウントを選んだり、同意を代行したりしません。
これはスキルの停止規則であり、未確認のホスト UI 挙動まで保証するものではありません。

### 公開 wire 観測（2026-10-28 報告、未認証）

以下は確認された HTTP 応答とメタデータの差です。Cowork がこの経路を実際に選択した、
またはその箇所で失敗した証明ではありません。origin の DCR 広告だけでクライアントが DCR を
発見・利用できるとは確定せず、実際の選択経路とクライアント/サーバーログが必要です。

| 確認した公開 URL / リクエスト | 応答 | 確認できた内容 |
| --- | --- | --- |
| `https://ingestion-mcp.marketplace-ingestion.mp.microsoft.com/.well-known/oauth-protected-resource` | 200 | `authorization_servers` は `https://login.microsoftonline.com/common/v2.0` を列挙 |
| `https://ingestion-mcp.marketplace-ingestion.mp.microsoft.com/.well-known/oauth-authorization-server` | 200 | `issuer` は上記 Entra URL、`registration_endpoint` は `https://ingestion-mcp.marketplace-ingestion.mp.microsoft.com/register`、PKCE は `S256`。この列挙した項目は 2026-10-27 と同じ |
| `https://login.microsoftonline.com/.well-known/oauth-authorization-server/common/v2.0` | 404 | この OAuth メタデータ経路では取得できない |
| `https://login.microsoftonline.com/common/v2.0/.well-known/oauth-authorization-server` | 404 | この OAuth メタデータ経路でも取得できない |
| `https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration` | 200 | OIDC メタデータ。issuer は `/{tenantid}/v2.0` のテンプレートで `registration_endpoint` なし |
| `/mcp` への未認証 `initialize` / `tools/list` POST | 401 | `copilot-cowork` と比較 User-Agent の双方。区別できる User-Agent 別応答は観測されない |

401 単独は保護された通常の挙動であり、根本原因ではありません。この比較から認証後のツール可視性や
ポリシーを断定しません。これらのプローブで認証、クライアント登録、販売者参照、書き込みは行っていません。
追加調査の実施者の報告を記録したもので、このスキルが接続ツール不在時に同じプローブを行う指示ではありません。

今回の検証は `wiqd plugin validate --mode deep` / AppValidationLibrary の実行ではありません。
`wiqd` は未導入です。既存 ATK 1.1.11 のパッケージ規則検証は M365 トークンとリモートのポータル呼び出しを
使うため、実行していません。オフラインの manifest ヘルパーはスキーマのみを確認します。
古い検証ツールのために 1.29 を下げたり、`None`、架空の OAuth 参照 ID、埋め込みシークレットで回避したりしません。

## 取り込み手順（サイドロード）

1. 配布元の `build-cowork-zip.ps1` で ZIP を生成（`manifest.json` がルートに来るように）。配布 ZIP の app version は、配布元の `cowork/manifest.json` と ZIP 内の `manifest.json` で確認。
2. Cowork の **カスタマイズ（Customize）** を開く。入口は UI により左ナビゲーション、または **+ ボタン → Customize** です。**プラグイン → プラグインの追加** からファイルを選び、ZIP をアップロード（公式ドキュメントの表記は **Upload plugin**）。通常の「チャット」ではなく「Cowork」を開いて操作します。
3. 共有画面で「自分のみ」または「組織内の特定のユーザー」を選び、公開する。特定ユーザーへの共有と、管理者による組織配布は別の経路です。
4. 対象アプリを追加し、**プラグインの詳細画面**、または会話の **Sources & Skills パネル**で有効化トグルを確認する。無効な場合は有効にしてから利用を確認してください。
5. **カスタマイズ → スキル（Skills）タブ → 自分のスキル（Your skills）** で、`partner-center-guide`、`troubleshoot-account-verification`、`marketplace-publishing` に対応する項目があるか確認する。これは一覧への登録・表示の確認であり、実際の会話や接続が動作することの確認とは別です。
6. 新しい会話で起動確認：「Partner Center に登録したい」「テナント関連付けができない」「Attestation が見つからない」などで発火します（Starter Conversations は `SKILL.md` 参照）。

### 共有されたプラグインを使う人

公開者が Cowork の共有画面で利用者を指定し、共有リンクを渡します。利用者はそのリンクまたは共有一覧からプラグインを追加・有効化してください。各利用者が同じ ZIP を再アップロードして公開する運用にはしません。

再公開時に所有権や同じアプリ ID に関するエラーが出た場合は、公開者の共有設定を確認します。エラー回避のために利用者ごとに ID を変更したり、既存の公開登録を削除したりしないでください。これは共有運用の案内であり、すべての配布経路に共通する ID 所有権の仕様を断定するものではありません。

### つまずき時に確認すること

| 症状 | 最初に確認すること |
|---|---|
| 「カスタマイズ」が見つからない | 「Cowork」を開き、左ナビゲーションまたは **+ ボタン → Customize** を確認する。画面構成や利用権も確認する |
| プラグイン追加の操作が見つからない | 現在の UI 表記、利用権、組織ポリシー。ボタンがない理由を一つに決めつけない |
| 追加したのに回答に使われない | 詳細画面または **Sources & Skills** の有効化トグル、**カスタマイズ → スキル → Your skills** の表示、新しい会話での起動条件 |
| ZIP が拒否される | エラー本文と `manifest.json` の ZIP 直下配置、参照フォルダー、スキルの検証条件。配置以外の原因もあり得る |
| Marketplace Ingestion が「利用可能」だが、会話に server/ツールがなく、可視のサインイン/同意 UI もない | `BLOCKED: 接続ツールが会話に出ていない` のみを返して停止。確認済みの画面と未確認のバックエンドを区別し、認証失敗や権限不足と断定しない。未確認のサインイン画面へ誘導せず、H2/H3/H4/H5 は追加証拠待ち。知識ガイドは継続できる |
| 実際に呼べる接続ツールから明示的なエラーが返る | 実際の応答と確認済みの範囲を示して停止する。認証/権限/スキーマ等はその証拠に沿って切り分け、未検証の前提は未確認のまま扱う。`None` や架空の OAuth 参照へ変更しない |
| カタログの項目が組織ポリシーでブロックされている | その項目の利用制限として確認する。別の ZIP の追加可否まで同じとは推測しない |

### 用語

- **プラグイン**: スキルや外部サービス接続をまとめる配布単位。この配布物では ZIP がそのパッケージです。
- **スキル**: プラグインに含まれる知識・手順。アカウント案内2つと任意の発行者ワークフロー1つを含みます。
- **コネクタ**: 任意の発行者ワークフロー用の接続宣言。同梱・利用可能表示・実行時のツール発見・認証・操作承認は別の段階です。

## 更新と再共有

1. ZIP の `id` と同じ公開登録の最新バージョンを確認する。ファイル名やアンインストール状態だけでは判定しない。表示や登録情報が食い違う場合は、公開前に確認する。
2. 既存プラグインの更新では `id` を維持し、公開済みより高い `version` にする。`manifestVersion` は書式の仕様番号であり、製品の版番号ではありません。
3. ソースから ZIP を再生成し、GitHub の配布版と ZIP 内の版をそろえる。番号を飛ばす場合は、その理由・確認済みの事実・未解明の点をリリースノートとコミット履歴に残す。
4. 新版をアップロードした後、詳細画面の **Re-share（再共有）** で既存の共有先へ最新版を届ける。対象者の変更・拡大は別の明示的な判断とし、更新のために変更しない。GitHub を更新するだけでは Cowork に反映されません。

アンインストールと公開登録の削除は別です。更新のために旧登録を削除したり、毎回新しいアプリ ID に変更したりしないでください。

公式手順: https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-customize#share-skills-and-plugins

有効化・無効化の案内: https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugins#manage-your-plugins

配布元の版番号変更履歴: https://github.com/MamoruKuroda/marketplace-skills/blob/main/plugins/partner-center-onboarding/dist/README.md

## 同梱物

- `SKILL.md` … 本体（実行ルール・トリアージ・§1〜§6・Starter Conversations）
- `pc_flow_*.png` … 公開パス／本人確認／登録／テナント関連付けのフロー図
- `REO_MPO_CSP_tax_cheatsheet_JP.md` … 商流（REO/MPO/CSP）・Agency Fee・日本税務（JCT）チートシート

## 保守

- Partner Center の UI・用語・URL は変わるため、提示前に Microsoft Learn を再 fetch するルールを `SKILL.md` 実行ルールに明記済み。
- 図・チートシートの再生成スクリプトは配布元フォルダ（`sdc/partner-center-guide/`）の `_make_flows*.py` を参照。
- 追加手順の補足には、2026-08-13 のローカル修正 `bff66bb` に残された実機観察を参照し、現在の公式共有手順と合わせて統合しました。当時の画面やトグルの初期状態が現在も同じとは限らないため、有効状態を都度確認してください。
