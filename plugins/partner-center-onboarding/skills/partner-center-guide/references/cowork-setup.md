# Cowork へのセットアップ（partner-center-guide）

アカウント登録・テナント関連付け・本人確認は引き続き **知識・対話ガイド型**で、コネクタや認証は不要です。
`partner-center-guide` と `troubleshoot-account-verification` は同梱の知識・図・チートシートで案内し、
サインイン、ロール付与、Entra 編集、提出は代行しません。

4.2.0 では別の任意スキル `marketplace-publishing` と公式 Marketplace Ingestion MCP 接続を追加しました。
発行者がこの接続の利用を明示した場合だけ別契約で進めます。接続・認証が使えなければ公開操作は **BLOCKED**、
既存の案内は **DEGRADED: guidance only** と明示して継続します。ホストがパッケージ自体を読み込めない場合は、
その互換性エラーを報告し、接続済み・利用可能と偽りません。

## 任意の発行者接続：認証と確認済みの範囲

- 公式エンドポイント: `https://ingestion-mcp.marketplace-ingestion.mp.microsoft.com/mcp`
- パッケージ: manifest **1.29** / app **4.2.0**。`agentConnectors` の ID は `market-ingest`。
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
- **実機未検証**: メタデータは DCR の広告を示すだけで、Cowork による登録・認証・同意・ツール検出、
  ファイル転送や販売者アクセスの動作証明ではありません。サーバー公式文書が挙げる対応クライアントは現在
  **VS Code / GitHub Copilot CLI**。Cowork の互換性・組織ポリシー・実際の接続状態は別途確認が必要です。

利用するときは、本人が販売者に関連付いたテナントのアカウントでネイティブの安全な認証画面にサインイン・同意し、
適切な Partner Center ロールと Marketplace submission API アクセスを確認します。他テナントは利用できません。
パスワード、MFA コード、クライアントシークレット、トークンを会話や設定ファイルへ入力させません。
案内だけの利用で認証を完了する必要はなく、認証を代行したり開始したりしません。

最初はツールの入力スキーマと `getSchema`、許可された最小範囲の `fetch` のみです。
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
| Marketplace 接続・認証・ツール検出が失敗する | 公開操作を停止。販売者テナント、必要ロール/API アクセス、DCR 対応、Cowork/組織ポリシーを個別に確認。`None` や架空の OAuth 参照へ変更せず、知識ガイドを継続する |
| カタログの項目が組織ポリシーでブロックされている | その項目の利用制限として確認する。別の ZIP の追加可否まで同じとは推測しない |

### 用語

- **プラグイン**: スキルや外部サービス接続をまとめる配布単位。この配布物では ZIP がそのパッケージです。
- **スキル**: プラグインに含まれる知識・手順。アカウント案内2つと任意の発行者ワークフロー1つを含みます。
- **コネクタ**: 任意の発行者ワークフロー用に追加した外部接続。パッケージへの同梱は、認証成功や操作への承認ではありません。

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
