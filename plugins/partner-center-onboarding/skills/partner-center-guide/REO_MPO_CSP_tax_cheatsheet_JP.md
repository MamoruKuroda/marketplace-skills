# REO / MPO / CSP・商流・日本税務（MoR）チートシート

> `partner-center-guide` スキルの §3「公開パスの判断」から分離した詳細リファレンス。
> すべての記述は Microsoft Learn 一次ソースを **2026-06-29 に fetch 検証済み（200・404なし）**。UI/対象国は頻繁に変わるため、利用前に各リンクを再確認すること。

---

## 0. 30秒サマリ（営業がまず押さえる3点）

1. **誰が誰に請求するか**で商流が決まる：直販＝**Private Offer**、ISVが販売店に再販許可＝**REO**、販売店経由で顧客販売＝**MPO**、CSP経由＝**CSP Private Offer**。
2. **Microsoft は常に顧客から代金を回収**し、ISV／販売店へ Store Service Fee（取引手数料）を引いて支払う。販売店→ISV の精算は **Marketplace 外**。
3. **税金の責任は「国の区分」で激変する。日本は Publisher-Managed＝消費税(JCT)は ISV 自己責任**（Microsoft は代理人）。ここが日本パートナー最大の誤解ポイント。

---

## 1. 商流モデル比較

| モデル | 誰が顧客に売る | 代金回収 | Agency/Store Fee | ISVへの支払 | 販売店→ISV 精算 | 主用途 |
|---|---|---|---|---|---|---|
| **Private Offer（ISV直販）** | ISV 自身 | Microsoft | あり（ISVから差引） | Microsoft→ISV | — | 既存顧客へ個別価格・期間 |
| **REO（Resale Enabled Offer）** | 認可された Channel Partner | Microsoft | あり | Microsoft→**Channel Partner**（手数料差引） | Channel Partner→ISV（Marketplace外） | ISVが販売店に自社Offerの再販を委任 |
| **MPO（Multiparty Private Offer）** | Channel Partner（ISVが作成→Partnerが顧客へ） | Microsoft | **Channel Partnerには手数料なし／ISVには適用** | Microsoft→Partner（手数料なし）＋ Microsoft→ISV（手数料あり） | — | 共同販売・チャネル主導 |
| **CSP Private Offer** | CSP パートナー（Direct Bill / Indirect Provider） | Microsoft→ISV は wholesale price | あり（agency fee） | Microsoft→ISV（wholesale − agency fee） | CSPが顧客価格を設定・請求（Marketplace外） | CSP チャネル経由・マージン設定 |

### 補足（検証済み）
- **REO**：ISV が Partner Center で「authorization（特定Offer×1販売店×販売可能市場）」を作成 → 販売店が独立して Private Offer / MPO を作成・販売。出典: resale-enabled-offers-overview。
  - **対象Offer種別**：公開取引可能な **SaaS** と **Azure VM（予約価格付き＝VMSR）** のみ。複数ISV製品を1つのPrivate Offerに束ねるのは不可（別々に作成）。
  - **対象市場**：Microsoft Marketplace 全対応地域で購入可。**除外8カ国＝Belarus / Brazil / China / India / Mexico / Russia / Singapore / South Korea**。→ **日本は対象**。出典: resale-enabled-offers-overview#supported-customer-markets。
  - **[推論注記]** 素の従量課金(PAYG)のみのVMが REO 対象かは公式が明言していない＝**要確認**。公式が明記する確実な対象は **VMSR（予約価格付き）構成**のみ。
  - **[推論注記]** REO の実取引は Private Offer（2者間）または MPO（3者間・Reseller 介在）で行う。日本では **2者間 Private Offer 経由は現在利用可**だが、**3者間 MPO 経由は MPO 日本提供の 2026-07-15 以降**になる見込み（REO概要＋MPO概要の複数ページからの整理）。

> 凡例：**[推論注記]** ＝ 公式ページに明記がなく、複数ソース／文脈から整理した推定。パートナーへ断定提示せず「要確認」「複数ページからの整理」と添えること。
- **MPO の日本提供**：2026-05-27 に欧州30カ国へ拡大、**Australia / Japan / South Africa は 2026-07-15 提供開始**と明記。Channel Partner は Partner Center の税務プロファイル完了が必要。出典: multiparty-private-offers-overview。
- **CSP**：マージンは CSP パートナー向けで顧客には非開示。**CSP Private Offer は顧客の MACC（Azure 消費コミット）には充当されない**。対象＝SaaS / Azure VM / Azure App / D365 Business Central。出典: isv-csp-reseller。
- **Private Offer**：時限割引・契約PDF添付・15分で購入可能。対象＝SaaS / Professional service / Azure VM / Container / Azure App。出典: isv-customer。

---

## 2. Agency Fee / Store Service Fee（手数料）

- **Store Service Fee（取引手数料）= Microsoft が毎回の売上から差し引く店舗手数料**。MPA（Microsoft Publisher Agreement）に基づく。出典: marketplace-commercial-transaction-capabilities-and-considerations / marketplace-get-paid。
- **標準率：一般に 3%**（ISV Partner Price に適用、CP マークアップには非適用）。※正確な率は MPA / Store fees ページで都度確認（本チートシートでは Mamoru 検証メモに基づき 3% と記載）。
- **更新割引：Private Offer / MPO の更新は Agency Fee 50%off（→実効 1.5%）**。条件：
  - 更新の定義3種＝①既存 Private Offer/有償Marketplace取引の更新 ②Marketplace 外の既存有償契約の Marketplace 移行 ③既存有償顧客への Upsell。
  - **Private Offer 作成時に self-attest 必須**、自動適用。**遡及不可**。**2024-10-01 以降作成の Offer のみ対象**。
  - 出典: agency-fee-discount-for-renewals。
- **Flexible Billing Schedule**：SaaS（flat-rate）/ VM 予約 / Professional services の Private Offer で顧客の予算サイクルに合わせた請求が可能。出典: flexible-billing-schedule（commercial-transaction ページ内で参照）。

---

## 3. 日本税務 / MoR（最重要・誤解多）

### 国区分の3類型（出典: tax-details-marketplace）

| 区分 | Microsoft の立場 | 税（消費税/VAT/GST）の責任 |
|---|---|---|
| **Publisher/Developer-Managed** | **代理人（agent）** | **ISV（Publisher）が全責任**：登録・計算・徴収・納付・顧客への税務インボイス発行 |
| **Microsoft-Managed** | 代理人 or コミッショネア | **Microsoft が計算・徴収・納付**。Microsoft の登録番号でインボイス発行 |
| **Reseller** | 再販業者 | Microsoft が顧客への再販分の税を負担（ISV→MS 間の取引税は ISV） |

### ⚠️ 日本のステータス＝**Publisher-Managed**

- **日本は Microsoft-Managed リストに含まれていない**（同リストにある近隣＝South Korea / Taiwan / Singapore / Thailand / Australia / New Zealand 等。**日本は不在**）。Reseller 国は Brazil のみ。特例＝China / India / Mexico。
- したがって **日本での販売では、日本の消費税（JCT）の登録・計算・徴収・納付・適格請求書（インボイス）発行は ISV（Publisher）自身の責任**。Microsoft は代理人として Store Service Fee 等を差し引くのみで、**顧客への消費税インボイスは（場合により）Microsoft 側で発行できない**。
- 実務影響：日本のパートナー／ISV は **自社でインボイス制度（適格請求書発行事業者）登録と JCT 納付の体制**が必要。「Marketplace に出せば税は Microsoft が全部やってくれる」は**日本では誤り**。
- 出典: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/tax-details-marketplace

### 支払い・税フォーム（出典: set-up-your-payout-account / marketplace-get-paid）

- 有償Offer販売には **US の税フォーム（米国居住要件を満たせば W-9、それ以外は W-8）** の提出が居住国に関わらず必須。
- payout/tax プロファイルは Seller ID ごとに各1つ（国/通貨ごとに分けるなら Seller ID を複数作成）。検証に最大48時間。
- 支払いは月次・閾値到達時、通常 毎月15日目処、着金にさらに3〜10営業日。
- 必要ロール：**Owner / Financial Contributor**。
- FX：USD入力は「プラン初回保存時のレート」で各国通貨に静的換算。顧客請求は取引月のレート。出典: marketplace-geo-availability-currencies。

---

## 4. 営業向け早見（症状→指す先）

| パートナーの声 | 指すべき答え | 出典 |
|---|---|---|
| 「販売代理店経由で売りたい」 | 自社Offerを再販委任＝**REO**、共同販売＝**MPO** | resale-enabled-offers-overview / multiparty-private-offers-overview |
| 「MPO は日本でいつ使える？」 | **2026-07-15 提供開始**（Channel Partner は税務プロファイル要） | multiparty-private-offers-overview |
| 「CSP で売ると顧客の Azure コミットに乗る？」 | **乗らない**（CSP Private Offer は MACC 非充当） | isv-csp-reseller |
| 「手数料は何%？更新は安くなる？」 | 標準 Store Service Fee（一般に3%）、更新は **50%off（作成時 self-attest）** | marketplace-commercial-transaction…／agency-fee-discount-for-renewals |
| 「日本の消費税は Microsoft がやる？」 | **やらない＝日本は Publisher-Managed、JCT は ISV 自己責任** | tax-details-marketplace |
| 「米国の税フォーム要る？日本企業だけど」 | **要る（W-8）**。居住国問わず必須 | set-up-your-payout-account |

---

## 参照（一次ソース・fetch 検証済み 2026-06-29）

- REO 概要: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/resale-enabled-offers-overview ✅
- MPO 概要（日本7/15提供）: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/multiparty-private-offers-overview ✅
- Private Offer（ISV直販）: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/isv-customer ✅
- CSP Private Offer: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/isv-csp-reseller ✅
- Store Service Fee / transact 能力: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/marketplace-commercial-transaction-capabilities-and-considerations ✅
- Agency Fee 更新割引50%: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/agency-fee-discount-for-renewals ✅
- 税務 / MoR（国区分3類型・日本=Publisher-Managed）: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/tax-details-marketplace ✅
- payout / 税フォーム（W-8/W-9）: https://learn.microsoft.com/en-us/partner-center/account-settings/set-up-your-payout-account ✅
- Getting paid: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/marketplace-get-paid ✅
- FX / 対応141地域・通貨: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/marketplace-geo-availability-currencies ✅
