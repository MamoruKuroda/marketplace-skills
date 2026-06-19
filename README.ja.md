# marketplace-skills

[GitHub Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli) の
**プラグイン用マーケットプレイス**です。**Microsoft Commercial Marketplace** への公開作業をガイドするスキルを提供します。

> このドキュメントは日本語版です。正本は英語版 [README.md](README.md) です。内容に差異がある場合は英語版を優先します。

> **実験的（EXPERIMENTAL）プロジェクトです。** 本番運用向けの製品ではありません。提出可能な状態のパッケージとチェックリストを準備するためのガイド付きスキルであり、Partner Center への提出を代行することはなく、明示的な承認なしにクラウド リソースをデプロイすることもありません。

## 収録プラグイン

| プラグイン | 役割 |
| --- | --- |
| [`agent-publishing`](plugins/agent-publishing/README.ja.md) | Microsoft 365 Copilot エージェント（宣言型／カスタムエンジン／Copilot Studio マルチテナント）の公開・収益化 |
| [`partner-center-onboarding`](plugins/partner-center-onboarding/README.ja.md) | Partner Center アカウント検証（識別／ロール、テナント、会社実在、状況可視化）のトラブルシュート |

今後の予定: `saas-publishing`、`container-publishing`、`managed-app-publishing`。

## クイックスタート（約5分で試す）

> Copilot エージェントを Microsoft Marketplace に公開したいけれど、どこから始めればいいか分からない——
> そんな方向けに、これらのスキルが対話形式でヒアリングし、適切な経路を選び、提出可能な状態のパッケージとチェックリストを生成します。Partner Center の手順を覚える必要はありません。

**前提ツール**

- [GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli)（`copilot --version` で確認）。VS Code の Copilot Chat でも利用できます。
- フル実行（Azure デプロイ・パッケージング）には Azure CLI（`az`）、GitHub CLI（`gh`）、Microsoft 365 Agents Toolkit CLI（`npm install -g @microsoft/m365agentstoolkit-cli`）が必要です。ガイド・triage 系のスキルはこれらが無くても動きます。

**1. Git-Ape をインストール（本プラグインの前提）**

```bash
copilot plugin marketplace add Azure/git-ape
copilot plugin install git-ape@git-ape
```

**2. 本プラグインをインストール**

```bash
copilot plugin marketplace add MamoruKuroda/marketplace-skills
copilot plugin install agent-publishing@marketplace-skills
```

**3. 確認**

```bash
copilot plugin list          # agent-publishing@marketplace-skills が表示される
```

対話セッション（`copilot`）内で `/skills list` を実行すると、8つのスキルが表示されます。

**4. 最初のヒアリングを試す**

```text
copilot
> /triage-agent-type スタートアップで、宣言型の人事ポリシー エージェントを作っていて、課金したいです。
```

triage スキルがいくつか質問し、経路を判定し、次に実行すべきスキルを案内します。詳しい流れは
[`agent-publishing` プラグインの README（日本語）](plugins/agent-publishing/README.ja.md) を参照してください。

## インストール（リファレンス）

このリポジトリ自体が Copilot CLI のプラグイン用マーケットプレイスです（`.github/plugin/marketplace.json` を含みます）。上記のマーケットプレイス経由のほか、サブディレクトリから直接インストールもできます。

```bash
copilot plugin install MamoruKuroda/marketplace-skills:plugins/agent-publishing
```

## ライセンス

デュアル ライセンスです。コード・構成は **MIT**（[`LICENSE-CODE`](LICENSE-CODE)）、ドキュメント・コンテンツは **Creative Commons Attribution 4.0（CC-BY-4.0）**（[`LICENSE`](LICENSE)）。著作権は Mamoru Kuroda。
