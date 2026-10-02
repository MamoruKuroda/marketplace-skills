# Cowork へのセットアップ（partner-center-guide）

このスキルは **知識・対話ガイド型**で、外部接続（コネクタ）も認証も不要です。Cowork はクラウドで動作し、`SKILL.md` の知識と同梱の図・チートシートだけで完結します（pmx-query と違い MCP サーバーや `az login` は不要）。

## 取り込み手順（Cowork の「カスタマイズ」から追加）

> ⚠️ Teams の「カスタムアプリのアップロード」ではなく、Cowork 内の「カスタマイズ」画面から追加します（UI は変わるため実際の画面で確認）。

1. このフォルダ一式を ZIP 化（`manifest.json` が **ZIP 直下**に来るように。フォルダを1段挟むと読めません）。配布 ZIP の app version は `cowork/manifest.json`（現在 1.3.0）で確認。
2. <https://m365.cloud.microsoft/cowork> を開く（または Microsoft 365 Copilot で「チャット」→「Cowork」に切り替え）。
3. 左メニューの **「カスタマイズ」** → **「プラグインの追加」** → ZIP を指定。
4. 「インストール済み」に現れた項目の **トグルを ON**（追加直後は OFF のことがある）。
5. 起動確認：「Partner Center に登録したい」「テナント関連付けができない」「Attestation が見つからない」などで発火します（Starter Conversations は `SKILL.md` 参照）。

### 配布と更新

- 他の人へは ZIP を配るより、所有者が Cowork 上で **共有** する方が確実です（共有先の「インストール済み」に現れ、トグル ON で利用可能）。
- 更新時は **app ID を変えずに version を上げた ZIP** を所有者が追加し直し、共有先には更新した旨を案内します。

| 症状 | 原因 |
|---|---|
| 「カスタマイズ」が無い | 「チャット」タブのまま。「Cowork」に切り替える |
| 「プラグインの追加」が無い | テナントポリシーでカスタムプラグインが禁止されている可能性 |
| 追加したのに反応しない | トグルが OFF |
| ZIP が弾かれる | `manifest.json` が ZIP 直下にない／SKILL.md の frontmatter・文字数制限 |

## 同梱物

- `SKILL.md` … 本体（実行ルール・トリアージ・§1〜§6・Starter Conversations）
- `pc_flow_*.png` … 公開パス／本人確認／登録／テナント関連付けのフロー図
- `REO_MPO_CSP_tax_cheatsheet_JP.md` … 商流（REO/MPO/CSP）・Agency Fee・日本税務（JCT）チートシート

## 保守

- Partner Center の UI・用語・URL は変わるため、提示前に Microsoft Learn を再 fetch するルールを `SKILL.md` 実行ルールに明記済み。
- 図・チートシートの再生成スクリプトは配布元フォルダ（`sdc/partner-center-guide/`）の `_make_flows*.py` を参照。
