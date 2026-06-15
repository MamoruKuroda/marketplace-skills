# marketplace-skills

[GitHub Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli) の
**プラグイン用マーケットプレイス**です。**Microsoft Commercial Marketplace** への公開作業をガイドするスキルを提供します。

> このドキュメントは日本語版です。正本は英語版 [README.md](README.md) です。内容に差異がある場合は英語版を優先します。

> **実験的（EXPERIMENTAL）プロジェクトです。** 本番運用向けの製品ではありません。提出可能な状態のパッケージとチェックリストを準備するためのガイド付きスキルであり、Partner Center への提出を代行することはなく、明示的な承認なしにクラウド リソースをデプロイすることもありません。

## 収録プラグイン

| プラグイン | 役割 |
| --- | --- |
| [`agent-publishing`](plugins/agent-publishing/README.ja.md) | Microsoft 365 Copilot エージェント（宣言型／カスタムエンジン／Copilot Studio マルチテナント）の公開・収益化 |

今後の予定: `saas-publishing`、`container-publishing`、`managed-app-publishing`。

## インストール

このリポジトリ自体が Copilot CLI のプラグイン用マーケットプレイスです（`.github/plugin/marketplace.json` を含みます）。使い方は2通りあります。

### A. マーケットプレイスを登録してからプラグインをインストール

```bash
copilot plugin marketplace add MamoruKuroda/marketplace-skills
copilot plugin install agent-publishing@marketplace-skills
```

### B. プラグインをサブディレクトリから直接インストール

```bash
copilot plugin install MamoruKuroda/marketplace-skills:plugins/agent-publishing
```

確認:

```bash
copilot plugin list
# 対話セッション内では: /skills list
```

## ライセンス

デュアル ライセンスです。コード・構成は **MIT**（[`LICENSE-CODE`](LICENSE-CODE)）、ドキュメント・コンテンツは **Creative Commons Attribution 4.0（CC-BY-4.0）**（[`LICENSE`](LICENSE)）。著作権は Mamoru Kuroda。
