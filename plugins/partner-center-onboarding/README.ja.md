# partner-center-onboarding（Partner Center アカウント検証トラブルシュート）

> **実験的（EXPERIMENTAL）プロジェクトです。** ガイド専用です。本プラグインは Partner Center への
> サインイン、ロール付与、Microsoft Entra の編集、提出のいずれも**代行しません**。ポータル上の操作は
> すべてユーザーが行います。パスワード・確認コード・シークレットを尋ねたり保存したりすることもありません。

> このドキュメントは日本語版です。正本は英語版 [README.md](README.md) です。内容に差異がある場合は英語版を優先します。

ISV・パートナーが **Microsoft 365 Copilot エージェント**を **Microsoft Commercial Marketplace** に
公開しようとする際に、最もつまずきやすい **Microsoft Partner Center のアカウント検証**を前に進めるための
スキル集です。

## なぜ必要か

つまずきの多くはエージェントの作成ではなく**アカウント検証**で起きます——サインインとロールの混乱、
テナント／App ID の不一致、発行元・会社実在の証明、「今どの段階？」という不安。これらを実際のパートナー
サポートのやり取り（Teams＋Slack）から抽出し、ひとつのゴール状態に収束させました。

## 設計：終点から固める（converge-from-endpoint）

ゴールは**ひとつ**——「検証済みで公開可能な Partner Center アカウント」——で、次の4条件で定義します。

| # | 条件 | 完了の判定 |
| --- | --- | --- |
| 1 | **識別とロール** | 正しい人が、公開／ユーザー管理ができるロールでサインインできる |
| 2 | **法人と発行元アイデンティティ** | Microsoft App ID＝Entra アプリ（クライアント）ID、発行元の法的情報が整合。Partner Center とのテナント一致は**不要**（発行元確認の青バッジは「アプリ登録テナントが Partner Global Account に関連付け」） |
| 3 | **会社の実在証明** | 法人／在籍の検証完了、Microsoft 365 and Copilot プログラムに登録、Partner One ID（MAICPP、旧 MPN）と第一連絡先が揃う |
| 4 | **状況の可視化** | 保存→公開→送信の順序、4〜6週間の所要、詰まったら Support Request でエスカレーション、が分かる |

4つのつまずき分類は**同じ答えへ向かう triage（振り分け）の軸**であり、別々のゴールではありません。
1つの質問で、詰まっている条件のブロックへ誘導します。

## 収録スキル

| スキル | 役割 |
| --- | --- |
| [`troubleshoot-account-verification`](skills/troubleshoot-account-verification) | 詰まっている条件を診断し、状況チェックリスト・次の一手・`verification-ledger.json` を出力 |

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
