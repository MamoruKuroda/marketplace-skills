# partner-center-onboarding（Partner Center オンボーディング）

> **実験的（EXPERIMENTAL）プロジェクトです。** ガイド専用です。本プラグインは Partner Center への
> サインイン、ロール付与、Microsoft Entra の編集、提出のいずれも**代行しません**。ポータル上の操作は
> すべてユーザーが行います。パスワード・確認コード・シークレットを尋ねたり保存したりすることもありません。

> このドキュメントは日本語版です。正本は英語版 [README.md](README.md) です。内容に差異がある場合は英語版を優先します。

ISV・パートナーが **Microsoft Marketplace** へ公開する際の **Partner Center オンボーディング**（アカウント登録
〜テナント関連付け〜本人確認〜 **Microsoft 365 Copilot エージェント**／**SaaS Offer** の公開）を自走できるよう
案内するスキル集です。

## なぜ必要か

つまずきの多くはオンボーディングの**入口**で起きます——登録、テナント関連付け、本人確認の順序、公開パスの選択
（宣言型 vs カスタムエンジン、Offer 種別、課金）、商流・税務（REO/MPO/CSP、日本の消費税）。とりわけ
**アカウント検証**はエージェント作成ではなく頻出のブロッカーです（サインイン／ロール混乱、テナント・App ID の
不一致、発行元・会社実在の証明、「今どの段階？」の不安）。これらを実際のパートナーサポートのやり取りから抽出し、
**ひとつの入口トリアージ＋検証の専門スキル**に集約しました。

## 2スキル構成：入口は1つ、専門家は1つ

- **`partner-center-guide`（入口・`user-invocable: true`）** — 広域トリアージ：登録、テナント関連付け、
  公開パス（エージェント種別／Offer 種別／課金）、商流・税務（REO/MPO/CSP、日本 MoR）。意思決定フロー画像4枚と
  日本税務チートシートを同梱。
- **`troubleshoot-account-verification`（内部・`user-invocable: false`）** — アカウント*検証*が実際の
  ブロッカーのとき入口から委譲。4条件へ収束させ `verification-ledger.json` を出力。

ユーザーは常に入口（guide）から入り、検証の深掘りは委譲で到達します。「どのスキルを使う？」の迷いをなくす設計です。

## 試しに聞いてみる（スターター）

- 「Partner Center にこれから登録したい。何から始めればいい?」
- 「テナント (Entra ID) の関連付けができない。」
- 「Copilot エージェントを公開したい。宣言型とカスタムエンジン、どっち?」
- 「Publisher Attestation の項目が見当たらない。」
- 「Developer 審査が通らない (登記簿と表記が違う)。」
- 「代理店 / CSP 経由で売りたい。REO と MPO の違いと、日本の消費税は?」

> 全リストとルーティングは
> [`skills/partner-center-guide/SKILL.md`](skills/partner-center-guide/SKILL.md) を参照。

## 収録スキル

| スキル | 起動 | 役割 |
| --- | --- | --- |
| [`partner-center-guide`](skills/partner-center-guide) | 入口 (true) | 広域オンボーディングのトリアージ＋公開パス＋REO/MPO＋日本税務。フロー画像＋チートシート |
| [`troubleshoot-account-verification`](skills/troubleshoot-account-verification) | 内部 (false) | アカウント検証の深掘り診断。4条件収束＋`verification-ledger.json` |

## `agent-publishing` との関係

`agent-publishing` は「**何を作り、どう提出するか**」（エージェント種別／収益化／提出ワークシート）を扱います。
`partner-center-onboarding` はその**直交する課題**——提出できるように**アカウント自体を検証済みにする**ことを
扱います。作成ではなく検証が止まっているときに使ってください。

## 配布先（CLI＋Cowork）

本スキルは移植性のある **Agent Skill**（`SKILL.md`、オープン標準）です。**GitHub Copilot CLI** ではそのまま
動作し、`skills/` フォルダーを Microsoft 365 アプリ パッケージ（`manifest.json`＋アイコン入りの `.zip`）に
すれば **Microsoft 365 Copilot Cowork** 用に配布できます
（[パッケージング手順](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development)）。
スラッシュコマンド専用の起動やサブエージェントには依存せず（Cowork 未対応のため）、説明文の自然言語トリガーで
発火します。

## インストール

```bash
copilot plugin marketplace add MamoruKuroda/marketplace-skills
copilot plugin install partner-center-onboarding@marketplace-skills
```

## 参考資料（引用前に必ず確認——表記は変わり得ます）

- Partner Center のロールと権限: https://learn.microsoft.com/en-us/partner-center/account-settings/permissions-overview
- 配布オプション: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/publish
- アプリ提出ガイド: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/add-in-submission-guide
- 開発者アカウントの開設: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/open-a-developer-account
- Cowork プラグイン開発: https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development

## ライセンス

デュアル ライセンスです。コード・構成は **MIT**、ドキュメント・コンテンツは **CC-BY-4.0**。
著作権は Mamoru Kuroda。
