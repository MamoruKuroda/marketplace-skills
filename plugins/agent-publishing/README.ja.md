# agent-publishing（Copilot エージェント公開スキル）

> **実験的（EXPERIMENTAL）プロジェクトです。** 本番運用向けの製品ではありません。提出可能な状態のパッケージとチェックリストを準備するためのガイド付きスキル集であり、Partner Center への提出を代行することはなく、明示的な承認なしに Azure リソースをデプロイすることもありません。

[Git-Ape](https://github.com/Azure/git-ape) のプラグインです。社員やパートナーが **Microsoft 365 Copilot エージェント**を **Microsoft Commercial Marketplace** に公開する作業を、対話形式でガイドします。**リンクした SaaS オファー**による収益化（任意）にも対応します。SaaS バックエンドの構築は [`azure-saas-skills`](https://github.com/dawright22/azure-saas-skills) と `@git-ape` に委譲します。

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

## インストール

[`marketplace-skills`](https://github.com/MamoruKuroda/marketplace-skills) マーケットプレイス経由:

```bash
copilot plugin marketplace add MamoruKuroda/marketplace-skills
copilot plugin install agent-publishing@marketplace-skills
```

または、このプラグインを直接インストール:

```bash
copilot plugin install MamoruKuroda/marketplace-skills:plugins/agent-publishing
```

あわせて Git-Ape とその前提ツール（Azure CLI、GitHub CLI、Microsoft 365 Agents Toolkit CLI / `atk`）の利用を推奨します。

## スキル一覧

| スキル | 役割 |
| --- | --- |
| `triage-agent-type` | 入口。ペルソナ＋種別＋収益化を判定し、適切な経路へ振り分け、台帳（ledger）に記録 |
| `path-declarative-atk` | 宣言型エージェントの app package を scaffold・検証・パッケージング |
| `path-custom-engine-atk` | カスタムエンジン エージェントの scaffold ＋ (A) 実行バックエンド |
| `path-copilot-studio` | Copilot Studio マルチテナント公開のガイド |
| `backend-agent-runtime` | (A) エージェント実行ランタイムを Azure に構築（カスタムエンジンのみ）→ `@git-ape` |
| `monetization-saas-offer` | (B) リンクした SaaS オファーのバックエンドを構築 → `azure-saas-skills` ＋ `@git-ape` |
| `validate-package` | manifest スキーマ／ルール、Store テストケースのローカル検証 |
| `submit-readiness` | プログラム登録の確認と、提出前チェックリスト（ブロッキング ゲート） |

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
   atk new --capability declarative-agent --app-name my-hr-agent --programming-language typescript --interactive false
   # manifest・instructions・knowledge／actions を編集
   atk package --env dev
   ```
3. `validate-package` がパッケージを検証（ゲート）します。`--env` の指定が必須です。
   ```bash
   atk validate --env dev --manifest-file ./appPackage/manifest.json --validate-method validation-rules
   atk validate --env dev --package-file ./appPackage/build/appPackage.dev.zip --validate-method test-cases
   ```
4. `submit-readiness` がブロッキング チェックリスト（法務・プライバシー・テスト手順・Responsible AI）を実行し、Launch Gate レポートと Partner Center の手動提出手順を出力します。
5. **最後はご自身で** Partner Center ポータルから提出し、審査フィードバックに対応します。

## 一連の流れ（宣言型／カスタムエンジン・収益化する場合）

上記に加えて、`submit-readiness` の前に次を実行します。

- `monetization-saas-offer` が **リンクした SaaS オファー**のバックエンド（Entra マルチテナント アプリ、SaaS フルフィルメント エンドポイント、ライセンス DB、必要に応じてメータリング）を、`azure-saas-skills` と `@git-ape` に委譲して構築します。**Microsoft 365 and Copilot プログラム**に加えて **Microsoft Marketplace プログラム**への登録が必要です。
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
