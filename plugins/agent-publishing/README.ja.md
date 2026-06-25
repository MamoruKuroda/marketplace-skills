# agent-publishing（Copilot エージェント公開スキル）

> **実験的（EXPERIMENTAL）プロジェクトです。** 本番運用向けの製品ではありません。提出可能な状態のパッケージとチェックリストを準備するためのガイド付きスキル集であり、Partner Center への提出を代行することはなく、明示的な承認なしに Azure リソースをデプロイすることもありません。

[Git-Ape](https://github.com/Azure/git-ape) のプラグインです。社員やパートナーが **Microsoft 365 Copilot エージェント**を **Microsoft Commercial Marketplace** に公開する作業を、対話形式でガイドします。**リンクした SaaS オファー**による収益化（任意）にも対応します。バックエンドの実際の Azure デプロイは `@git-ape` に委譲します。

> このドキュメントは日本語版です。正本は英語版 [README.md](README.md) です。内容に差異がある場合は英語版を優先します。

## 対象範囲

Marketplace に到達できるエージェントの公開経路は次の3つです。

1. **宣言型エージェント**（Microsoft 365 Agents Toolkit）
2. **カスタムエンジン エージェント**（Microsoft 365 Agents Toolkit）
3. **Copilot Studio マルチテナント** カスタムエージェント

対象外（現時点）: Cowork プラグイン、Copilot コネクタ／プラグイン、および組織カタログ止まりの経路（Agent Builder、Copilot Studio の宣言型、SharePoint エージェント）。

## 2つの独立した判断軸

- **agent_type（エージェント種別）** … **実行バックエンド (A)** が必要かどうかを決めます（必要なのはカスタムエンジンのみ）。
- **monetize（収益化するか）** … **収益化バックエンド (B)**（＝リンクした SaaS オファー）が必要かどうかを決めます（エージェント種別とは独立）。

## ペルソナ別クイックスタート

| ペルソナ | こんな方 | 最初に実行 |
| --- | --- | --- |
| P1 スタートアップ ISV | pro-code のスタートアップ。収益化したい | `/triage-agent-type` → 宣言型／カスタムエンジン＋収益化 |
| P2 パートナー／SI | 顧客のエージェント公開を代行 | `/triage-agent-type` → 全経路（ガバナンス重視） |
| P3 Microsoft 社員 | パートナー伴走（デモ・教育） | `/triage-agent-type` → 全経路 |
| P4 ローコード メーカー | ローコード／GUI 志向 | `/triage-agent-type` → Copilot Studio |

## 前提条件

必要なものは、**どこまでやりたいか**で変わります。まずは小さく（L1）始め、進むにつれてツールを追加してください。

### クライアントの選び方（VS Code 推奨）

エンジニアはエディタで開発し、Microsoft 365 Agents Toolkit / Azure のサインインは **VS Code では GUI に統合**されています（アカウント選択・ブラウザ OAuth・ステータスバー表示）。これは CLI より滑らかです。CLI は Windows では OS の WAM ダイアログにフォールバックし、検証用テナントでのサインインが扱いづらくなります。したがって:

| クライアント | L1 ガイド | L2 パッケージング | L3 Azure デプロイ |
| --- | --- | --- | --- |
| **VS Code Copilot Chat**（推奨） | ✅ | ✅ GUI サインイン | ✅ Azure MCP・GUI サインイン |
| **Copilot CLI** | ✅ 完結 | ⚠️ 限定的 — サインイン不要の手順（`new`／`package`／validation-rules）は動作。M365/Azure サインインが必要な手順は WAM ダイアログになる | ❌ 非推奨 |

結論: **L1（とサインイン不要のパッケージング）は Copilot CLI**、**L2〜L3 は VS Code** を使ってください。

| レベル | できること | クライアント | 追加ツール | アカウント |
| --- | --- | --- | --- | --- |
| **L1 ガイド** | triage、提出前チェックリスト、Partner Center 提出ワークシートの生成 | VS Code Copilot Chat（または Copilot CLI） | — | GitHub Copilot |
| **L2 パッケージング** | 宣言型エージェントの scaffold／検証／パッケージング | VS Code | Node.js LTS、`atk`（`@microsoft/m365agentstoolkit-cli`） | ＋ Microsoft 365 テナント（sideload／検証）。**knowledge で grounding するエージェントを*使う*には、テナントに M365 Copilot ライセンス（または Copilot Studio の従量課金）が必要——sideload だけではインストールはできても回答が空になります。** |
| **L3 Azure デプロイ** | カスタムエンジンの実行ランタイム／リンクした SaaS オファーのバックエンド | **VS Code**（Azure MCP） | ＋ Azure CLI（`az`）、**Windows では git-bash**、`gh`、`jq`、`git` | ＋ Azure サブスクリプション |
| **L4 提出** | 生成されたワークシートに沿って Marketplace へ提出 | ブラウザ | — | ＋ Partner Center（Microsoft 365 & Copilot **および** Microsoft Marketplace の両プログラム） |

> **セットアップの境界線：** **L1 はセットアップ不要**（Copilot へのログインだけ。何もインストールせず triage とチェックリスト／ワークシート生成が動く）。**L1 より上は各レベルでツールが増えます**——L2 で Node.js＋`atk`、L3 で Azure CLI＋git-bash＋Azure サブスクリプション。実際に到達したレベルが必要とするものだけを入れればよく、最初に全部揃える必要はありません。

**ハード制約**

- **Git-Ape の Azure デプロイは VS Code 前提です。** Azure アクセスは Azure MCP サーバー経由で、VS Code 設定で構成します（[Azure setup](https://azure.github.io/git-ape/docs/getting-started/azure-setup)）。L3 を行うなら VS Code Copilot Chat を推奨します。
- **Windows で L3 を行うには Bash 互換シェル（git-bash）が必要です。** Git-Ape は他のシェルは未検証と明記しています（GitHub 連携のため既に git-bash を導入済みの開発者も多いです）。
- **VS Code Copilot Chat では `chat.plugins.enabled` 設定が必要**で、これは組織管理者が管理します。
- L4（Marketplace への提出・審査）は常に**手動**です。本プラグインはコピペ可能な提出ワークシートを生成しますが、提出操作は人間が Partner Center で行います。

> まず試すだけなら、**L1 は Copilot へのログインだけで動きます。** `atk` や Azure CLI、サブスクリプションが無くても、triage のヒアリングやチェックリスト生成を実行できます。

## インストール

まず Git-Ape をインストールします（本プラグインの前提です）。

```bash
copilot plugin marketplace add Azure/git-ape
copilot plugin install git-ape@git-ape
```

次に [`marketplace-skills`](https://github.com/MamoruKuroda/marketplace-skills) マーケットプレイス経由:

```bash
copilot plugin marketplace add MamoruKuroda/marketplace-skills
copilot plugin install agent-publishing@marketplace-skills
```

または、このプラグインを直接インストール:

```bash
copilot plugin install MamoruKuroda/marketplace-skills:plugins/agent-publishing
```

確認したうえで、最初のヒアリングを試します。

```text
copilot plugin list          # agent-publishing@marketplace-skills が表示される
copilot
> /triage-agent-type スタートアップで、宣言型の人事ポリシー エージェントを作っていて、課金したいです。
```

## スキル一覧

| スキル | 役割 |
| --- | --- |
| `triage-agent-type` | 入口。ペルソナ＋種別＋収益化を判定し、適切な経路へ振り分け、台帳（ledger）に記録 |
| `path-declarative-atk` | 宣言型エージェントの app package を scaffold・検証・パッケージング |
| `path-custom-engine-atk` | カスタムエンジン エージェントの scaffold ＋ (A) 実行バックエンド |
| `path-copilot-studio` | Copilot Studio マルチテナント公開のガイド |
| `backend-agent-runtime` | (A) エージェント実行ランタイムを Azure に構築（カスタムエンジンのみ）→ `@git-ape` |
| `monetization-saas-offer` | (B) リンクした SaaS オファーのバックエンドを構築（スキル内で自己完結）→ `@git-ape` でデプロイ |
| `validate-package` | manifest スキーマ／ルール、Store テストケースのローカル検証 |
| `submit-readiness` | プログラム登録の確認、ブロッキング チェックリスト、Partner Center 提出ワークシート（コピペ用）の生成 |

## 使い方の例

```text
# まずは triage から。ペルソナ・種別・収益化を判定し、適切な経路へ案内します:
@git-ape /triage-agent-type スタートアップで、宣言型の人事ポリシー エージェントを作っていて、課金したいです。

# 特定の経路スキルを直接実行（上級者向け。通常は triage が振り分けます）:
@git-ape /validate-package env dev で ./appPackage/manifest.json を検証して
@git-ape /submit-readiness Partner Center に提出できる状態か確認して
```

## 一連の流れ（宣言型エージェント・無償の場合）

1. `@git-ape /triage-agent-type ...` を実行すると、`publishing-ledger.json` に `agentType=declarative`／`monetize=false` を記録し、`path-declarative-atk` へ振り分けます。
2. `path-declarative-atk` が scaffold とパッケージングを実行します。
   ```bash
   atk new --capability declarative-agent --app-name my-hr-agent --interactive false
   # manifest・instructions・knowledge／actions を編集
   atk package --env dev
   ```
3. `validate-package` がパッケージを検証（ゲート）します。`--env` の指定が必須です。
   ```bash
   atk validate --env dev --manifest-file ./appPackage/manifest.json --validate-method validation-rules
   atk validate --env dev --package-file ./appPackage/build/appPackage.dev.zip --validate-method test-cases
   ```
4. `submit-readiness` がブロッキング チェックリスト（法務・プライバシー・テスト手順・Responsible AI）を実行し、Launch Gate レポートと、**Partner Center 提出ワークシート（10ステップを台帳の値で事前入力したコピペ用）**を出力します。
5. **最後はご自身で** Partner Center ポータルから提出し、審査フィードバックに対応します。

## 一連の流れ（宣言型／カスタムエンジン・収益化する場合）

上記に加えて、`submit-readiness` の前に次を実行します。

- `monetization-saas-offer` が **リンクした SaaS オファー**のバックエンド（Entra マルチテナント アプリ、SaaS フルフィルメント エンドポイント、ライセンス DB、必要に応じてメータリング）を、スキル内で定義し `@git-ape` でデプロイします。**Microsoft 365 and Copilot プログラム**に加えて **Microsoft Marketplace プログラム**への登録が必要です。
- カスタムエンジン エージェントの場合は、さらに `backend-agent-runtime`（`atk provision`／`atk deploy`）を実行し、エージェント自身のランタイムを Azure に構築します。

## 自動化できる範囲と手動が必要な範囲

| 工程 | 自動化（CLI） | 手動 |
| --- | --- | --- |
| scaffold／検証／パッケージング | ✅ `atk new/validate/package` | |
| カスタムエンジンの provision／deploy | ✅ `atk provision/deploy` | |
| 組織カタログへの提出 | ✅ `atk publish` | Teams 管理センターでの管理者承認 |
| **Marketplace への提出・掲載・審査** | | ❌ Partner Center ポータル＋人手審査 |
| Responsible AI／認定審査 | | ❌ 提出後の人手審査 |

> **補足（2026-04 / preview）**: 新しい **Product Ingestion API**（`https://graph.microsoft.com/rp/product-ingestion`）が「AI Apps and Agents」カテゴリと SaaS オファー構成を **preview** で扱えるようになりました。ただし公開時には標準の認定フローと手動の **Go-live** を経るため、API の価値は実質的に「構成・ドラフトの自動化」までです。本スキル集は確実なポータル手順を主経路とします。

## テナントの安全性

スキルはテナント ID やシークレットをハードコードしません。テナント情報は triage 時に収集し、`publishing-ledger.json`（シークレットは含めない）に保存します。台帳は実行者・ワークスペースごとに管理されます。

## 参考資料（一次ソース）

- https://learn.microsoft.com/ja-jp/partner-center/marketplace-offers/add-in-submission-guide
- https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/publish
- https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agents-overview
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/artificial-intelligence-app-agent-publish-release
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/monetize-addins-through-microsoft-commercial-marketplace

## ライセンス

デュアル ライセンスです。コード・構成は **MIT**（[`LICENSE-CODE`](../../LICENSE-CODE)）、ドキュメント・コンテンツは **Creative Commons Attribution 4.0（CC-BY-4.0）**（[`LICENSE`](../../LICENSE)）。著作権は Mamoru Kuroda。
