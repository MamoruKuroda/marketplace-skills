# Cowork へのセットアップ（partner-center-guide）

このスキルは **知識・対話ガイド型**で、外部接続（コネクタ）も認証も不要です。Cowork はクラウドで動作し、`SKILL.md` の知識と同梱の図・チートシートだけで完結します（pmx-query と違い MCP サーバーや `az login` は不要）。

## 取り込み手順（サイドロード）

1. このフォルダ一式を ZIP 化（`manifest.json` がルートに来るように）。
2. Copilot / Teams の **アプリ管理（カスタムアプリのアップロード／サイドロード）** から ZIP をアップロード。
3. Cowork で対象アプリを有効化すると、`manifest.json` の `agentSkills` 経由で本スキルが読み込まれます。
4. 起動確認：「Partner Center に登録したい」「テナント関連付けができない」「Attestation が見つからない」などで発火します（Starter Conversations は `SKILL.md` 参照）。

## 同梱物

- `SKILL.md` … 本体（実行ルール・トリアージ・§1〜§6・Starter Conversations）
- `pc_flow_*.png` … 公開パス／本人確認／登録／テナント関連付けのフロー図
- `REO_MPO_CSP_tax_cheatsheet_JP.md` … 商流（REO/MPO/CSP）・Agency Fee・日本税務（JCT）チートシート

## 保守

- Partner Center の UI・用語・URL は変わるため、提示前に Microsoft Learn を再 fetch するルールを `SKILL.md` 実行ルールに明記済み。
- 図・チートシートの再生成スクリプトは配布元フォルダ（`sdc/partner-center-guide/`）の `_make_flows*.py` を参照。
