# marketplace-skills

[GitHub Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli) の
**プラグイン用マーケットプレイス**です。**Microsoft Commercial Marketplace** への公開作業をガイドするスキルを提供します。

> このドキュメントは日本語版です。正本は英語版 [README.md](README.md) です。内容に差異がある場合は英語版を優先します。

> **実験的（EXPERIMENTAL）プロジェクトです。** 本番運用向けの製品ではありません。提出可能なパッケージとチェックリストを準備します。アカウント案内はサインイン・提出を代行しません。Partner Center Onboarding には任意の発行者向け MCP ワークフローもあり、本人による認証と、変更ごとの対象・変更前後の確認・個別承認が必須です。明示的な承認なしにクラウド リソースをデプロイしません。

## 想定ユーザー (Who this is for)

Microsoft Commercial Marketplace への公開を目指して Partner Center を進めている方の
ために作られています。

- **はじめて Partner Center と Marketplace にオンボードするソフトウェア企業・
  スタートアップ (SDC/ISV)。**
- **そうしたチームの立ち上げを手伝う人** — 例えば、複数の企業を同時に支援する
  パートナーマネージャー・ソリューションアーキテクト・コンサルタントなど。

内容はすべて **公開されている Microsoft のドキュメント**（内部ツールや非公開情報は
不使用）に基づいています。公開する企業側でも、公開を手伝う側でも、自由に読み・共有し・
活用できます。

### 想定していないユーザー (Who this is not for)

すでに Partner Center にオンボード・サインアップされていたり、Marketplace に Offer を
公開されている企業や、その Microsoft 担当者にはアカウント案内が不要かもしれません。権限のある発行者は
Partner Center Onboarding の Marketplace Ingestion ワークフローを別途選択できます。公開を支援するパートナーにも
参照資料として役立つはずです。

コンテンツは、すべてを一つの大きなドキュメントにまとめるのではなく、意図的に小さく
焦点を絞ったスキルに分割しています。見落としがちな作業時のポイント——Partner Center の
各審査ステップで実際に求められる物や、国ごとの会社確認（日本であれば、登記簿謄本の提出と
登録住所の完全一致 など）——を織り込んでいます。

## 収録プラグイン

| プラグイン | 役割 |
| --- | --- |
| [`agent-publishing`](plugins/agent-publishing/README.ja.md) | Microsoft 365 Copilot エージェント（宣言型／カスタムエンジン／Copilot Studio マルチテナント）の公開・収益化 |
| [`partner-center-onboarding`](plugins/partner-center-onboarding/README.ja.md) | ガイド専用の登録・検証と、任意の Marketplace Ingestion MCP 発行者ワークフロー（変更は操作ごとに承認、Cowork 実機認証は未検証） |

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
