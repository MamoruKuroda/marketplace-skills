# REO / MPO / CSP・商流・日本税務（MoR）チートシート

> 公開 Microsoft Learn のみを根拠にした、営業/支援者向けの切り分け表。個別税務・契約・価格判断は専門家/契約担当へエスカレーションする。
> 最終 fetch: 2026-09-12。回答時は該当 URL を再確認する。

## 0. 30秒サマリ（営業がまず押さえる3点）

1. **三者を分ける**: ISV/Publisher、CSP/Channel Partner、Customer/Buyer。誰が価格を設定し、誰が Microsoft から請求され、誰が顧客へ請求するかで答えが変わる。
2. **Microsoft が常に顧客から回収するわけではない**: ISV-to-customer private offer、REO private offer、MPO では Marketplace が顧客購入/請求に関与する。一方 CSP private offer では CSP partner が Microsoft から wholesale price で請求され、CSP が顧客価格と顧客請求を Marketplace 外で管理する。
3. **日本税務は慎重に**: Japan は tax-details の Microsoft-managed/reseller 表に出ないため、公開 docs の定義上 Publisher/Developer-managed と扱うのが安全な整理。JCT 登録・計算・徴収・納付・適格請求書は ISV/Developer 側責任として税務専門家に確認する。

回答テンプレ:
- Who: ISV / CSP Direct Bill / Indirect Provider / Indirect Reseller / Customer / Azure billing admin
- Surface: Partner Center Marketplace offers / CSP Pricing / Azure portal private offer / Cost Management + Billing
- 根拠区分: 公開事実 / 公開事実からの推論 / 未確認
- publicSources: フル URL と fetch 日

## 1. 商流モデル比較

| モデル | 主な売り手 | 顧客/相手への請求 | Microsoft からの支払/請求 | 注意点 |
| --- | --- | --- | --- | --- |
| ISV-to-customer Private Offer | ISV | Customer は Azure portal で受諾/購入し Microsoft から請求 | Microsoft が ISV に支払う | customer billing account ID が必要。受諾と購入は別ステップ |
| REO（Resale Enabled Offer） | 認可 Channel Partner | private offer または MPO 経由で customer が購入 | Microsoft は channel partner に支払い、channel partner が ISV と Marketplace 外で精算 | authorization は特定 offer、1 partner、1つ以上の customer market に紐づく |
| MPO（Multiparty Private Offer） | Channel Partner | Customer が Azure portal で受諾/購入 | Microsoft は channel partner と ISV に別々に支払う（partner 側 no agency fee、ISV 側 agency fee） | supported countries と partner tax profile を確認 |
| CSP Private Offer | Direct Bill または Indirect Provider | CSP が customer price と請求を Marketplace 外で管理 | CSP は Microsoft から wholesale price で請求される。ISV は wholesale price から agency fee 差引で支払われる | Indirect Reseller へ ISV が直接 margin を出せない |

### 補足（公開事実）

- REO は software company が Partner Center で authorization を作る。対象は public transactable SaaS、Azure VM with reservation pricing (VMSR)、Dragon Copilot offers。複数 software company の製品を1つの REO private offer に束ねるのは不可。
- MPO は customer と channel partner の supported country/tax profile を見る。Japan は 2026-09-12 fetch 時点の supported countries 表で customer/channel partner とも対応。
- CSP private offer の対象は SaaS、Azure Virtual Machines、Azure Applications、Dragon Copilot offers、Dynamics 365 Business Central apps。Margins は software charges に適用され、関連 Azure infrastructure hardware charges には適用されない。
- Private offer は time-bound pricing/customized terms。顧客は offer を accept した後、含まれる product を purchase/subscribe して billing を開始する。複数 product は product ごとの購入が必要。

publicSources:
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/isv-customer
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/resale-enabled-offers-overview
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/multiparty-private-offers-overview
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/isv-csp-reseller
- https://learn.microsoft.com/en-us/marketplace/private-offers-purchase

## 2. Agency Fee / Store Service Fee（手数料）

- Store Service Fee / agency fee は Marketplace transaction に関係する手数料。率や契約条件は最新の Microsoft Publisher Agreement / Partner Center docs を確認し、古い率を暗記で断定しない。
- Customer private offer と multiparty private offer の renewal では agency fee discount が使える場合がある。renewal self-attestation は private offer 作成時だけで、後から Partner Center/support で retroactive に付けられない。
- CSP private offer margin は CSP partner 向けで、customer には見えない。Provider/Direct Bill が顧客条件をどう設定するかは Marketplace 外の関係。
- Indirect Provider が Indirect Reseller へ discount を渡すかは任意。ISV から reseller への自動 passthrough と言わない。

publicSources:
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/agency-fee-discount-for-renewals
- https://learn.microsoft.com/en-us/partner-center/customers/csp-commercial-marketplace-margins
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/isv-csp-reseller

## 3. 日本税務 / MoR（最重要・誤解多）

### 国区分の3類型

| 区分 | Microsoft の立場 | Transaction Taxes の整理 |
| --- | --- | --- |
| Publisher/Developer-managed | agent | Publisher/Developer が Offer Taxation の登録、計算、徴収、納付、顧客税務インボイス等に責任 |
| Microsoft-managed | agent/commissionaire | Microsoft が一部税の計算、徴収、納付等を管理 |
| Reseller | reseller | Microsoft が顧客への再販売側 Offer Taxation を担う。Publisher/Developer は Microsoft への販売側税務を確認 |

### 日本の扱い

- tax-details の Microsoft-managed countries、Reseller countries、commercial/consumer differences の表に Japan は表示されない。したがって「Microsoft-managed/reseller に明記されていない supported country は Publisher/Developer-managed」という同ページの定義から、Japan は Publisher/Developer-managed と整理する。
- これは Marketplace tax responsibility の公開 docs に基づく整理であり、個別 JCT 登録、適格請求書、B2B/B2C、CSP/authorized partner を含む契約全体の税務結論を代替しない。
- 「Microsoft が顧客に請求書を出す」ことと「消費税インボイス/納税責任を誰が負う」ことは別。Japan では ISV/Developer 側の税務確認を必ず促す。
- REO authorized partner や CSP を含む全チェーンの税務責任まで一般化しない。tax-details は Publisher/Developer、Authorized Partners、Developers の責任に触れるが、各契約・国・取引形態の最終判断は専門家確認。

publicSources:
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/tax-details-marketplace
- https://learn.microsoft.com/en-us/legal/marketplace/msft-publisher-agreement

## 4. FX / 通貨 / 請求

### 価格入力と3つの換算先を分ける

| 通貨 | 決まり方 | 典型質問 |
| --- | --- | --- |
| Offer input currency | Partner Center で ISV がまず USD 価格を保存し、必要に応じ market pricing を上書き | 「USD で入れたら円価格は変動する?」 |
| Market currency | customer の legal business address/market に基づく。Japan market は JPY | 「日本の顧客に何通貨で表示?」 |
| Billing currency | customer agreement/billing account の通貨 | 「請求時に追加 FX がある?」 |
| Payout currency | Partner Center の payout 設定 | 「ISV 受取額が為替で変わる?」 |

### 正しい説明

- USD 価格を初回保存すると、Microsoft が monthly exchange rate で market currency 価格を作る。この market/local price は publisher が価格変更するまで自動追随しない。
- **顧客請求が取引月レートになるのは、market currency と billing currency が異なる場合。** 同じなら追加の market-to-billing FX はない。
- payout currency が billing currency と違う場合、Microsoft から publisher への支払時に別の換算が起こり得る。
- Japan market は marketplace-geo page で JPY。Japan market + JPY billing currency なら追加 FX なしと説明できるが、数量、metered usage、税、invoice timing、renewal/private offer 条件まで固定とは言えない。
- Microsoft は WMR FX Benchmarks / London 4pm Closing Spot Rates を monthly に使う。customer doc は「前月末の3営業日前」の rate と説明する。具体日付例は年/月で変わるため、回答では原則日付をハードコードしない。

### Private Offer の currency mismatch

- Customer doc では、customer billing currency が market currency と異なる場合、private offer purchase が supported でない旨が説明されている。
- Publisher FX FAQ では、同じ場面で absolute pricing private offer は supported でなく、製品によって percentage-only discount や private plan が選択肢になる場合があると説明される。
- したがって「private offer は必ず不可/必ず可」と短絡せず、offer type、pricing model、absolute price か percentage discount か、private plan 可否を確認する。

### ISV の一般的な FX 対策（公開 docs の範囲）

- market price を export/import で見直す、USD base price を更新する、specific market で販売停止する、private offer を活用する。
- upfront one-time payment、customer billing profile USD、multi-year を年次 private offer に分ける等は、ISV の FX exposure を小さくするための docs 上の選択肢。顧客総額を必ず固定する万能策とは言わない。

publicSources:
- https://learn.microsoft.com/en-us/marketplace/currencies
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/commercial-marketplace-fx-faq
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/marketplace-geo-availability-currencies

## 5. CSP Private Offer 実務切り分け

### ステータス/ID の混同防止

- Active CSP program は CSP 側が margin を受ける資格（Direct Bill または Indirect Provider であること）を確認する入口であり、Marketplace publisher enrollment、seller ID、tax/payout profile は ISV/publisher 側の前提として別に確認する。
- CSP 側は Partner Center > Account settings > Legal Info / Account management の Reseller tab / Program info で Microsoft Cloud Solution Provider status を確認する。ISV が相手を選ぶときは CSP partner name / tenant ID を使う。
- ISV が +Add CSP partners で探す対象は CSP partner name / tenant ID。Seller ID、Publisher ID、Partner One ID、buyer tenant ID、Entra application ID ではない。
- ISV が直接 private offer margin を延ばせるのは Direct Bill または Indirect Provider。Indirect Reseller は Indirect Provider と連携する。

### 契約

- CSP agreements を既に締結済みの partner は、Microsoft Marketplace offers を売るためだけに再署名は不要と Learn は説明する。
- ただし一部 Marketplace offers は partner、ISV、customer 間の追加 agreement を必要とし得る。Microsoft commerce platform は当事者間の追加 legal terms を成立させる仕組みを提供しない、という説明もある。
- したがって「MPA さえあれば顧客契約不要」「どのケースも追加手順なし」とは言わない。

publicSources:
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/isv-csp-reseller
- https://learn.microsoft.com/en-us/partner-center/customers/csp-commercial-marketplace-margins
- https://learn.microsoft.com/en-us/partner-center/customers/csp-commercial-marketplace-contracting
- https://learn.microsoft.com/en-us/partner-center/enroll/microsoft-partner-agreement

## 6. SaaS / subscription / consumable credits の境界

- SaaS offer では publisher が顧客利用の infrastructure を支え、Marketplace の landing page、fulfillment APIs、operations APIs、webhook、subscription state によって activation/update/cancel と billing が連動する。
- 「追加クレジットを売りたい」は、既存 subscription の renewal、quantity update、metered usage、別 plan/SKU、新しい private offer、別 product purchase のどれかを先に切り分ける。望む商業効果だけで実装方式を決めない。
- Marketplace の SaaS fulfillment は license grant/account mapping を自動的にすべて処理する魔法ではない。publisher 側 SaaS アカウント、SSO、provisioning、entitlement/meter usage 管理を設計する。
- customer-hosted / publisher-hosted / hybrid のような hosting 形態だけで即「SaaS 不可」と断定しない。誰が運用し、何を顧客が購入し、どの Marketplace policy/technical requirement に当たるかを確認する。
- installed PC app、任意コード配布、物理 hardware、単なるサポート契約などは別 offer type/policy の可能性があるため、1000 SaaS policy と publisher guide を確認して未確認なら「要追加確認」とする。

publicSources:
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/plan-saas-offer
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/create-new-saas-offer
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/create-new-saas-offer-plans
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/create-new-saas-offer-technical
- https://learn.microsoft.com/en-us/partner-center/marketplace-offers/pc-saas-fulfillment-life-cycle
- https://learn.microsoft.com/en-us/legal/marketplace/certification-policies

## 7. Procurement / cost attribution / PO

### まず分けるオブジェクト

| オブジェクト | 何を表すか | 混同しやすい点 |
| --- | --- | --- |
| Offer / product | Marketplace の公開製品 | 部署/予算ではない |
| Private Offer | 個別価格・期間・terms | purchase/subscribe 完了までは billing 開始ではない |
| Azure subscription | Azure resource scope | 必ずしも部署/請求先そのものではない |
| SaaS subscription | Marketplace SaaS の契約/利用状態 | Azure subscription と同名でも別概念 |
| Purchase Order | 顧客内部の予算/発注管理 | Microsoft invoice を置換しない |
| PO mapping | charge を PO に割り当てる rule | private offer 別割合や部署自動判定ではない |
| Invoice / supplemental documents | Microsoft からの請求・補助資料 | PO は支払期限や請求額を変えない |

### PO mapping の範囲

- Purchase order を作っただけでは charge は紐づかない。mapping を作り、active/effective/expiration に合う future charge が該当すると割り当てられる。
- Mapping scope は broad（all purchases, all Marketplace products 等）から specific（publisher ID、publisher ID + offer ID）まで。もっとも specific な mapping が優先される。
- Product mapping には publisher ID と offer ID が必要。reseller/services partner 名ではなく、Marketplace product の publisher/product ID を使う。
- Reapply mappings は過去 invoice/supplemental documents に影響し得る。EA では rebilling と invoice void/new invoice が起こり得るため、実行前に billing admin/finance が影響確認する。

publicSources:
- https://learn.microsoft.com/en-us/marketplace/billing-invoicing
- https://learn.microsoft.com/en-us/marketplace/purchase-orders
- https://learn.microsoft.com/en-us/marketplace/purchase-order-mapping
- https://learn.microsoft.com/en-us/marketplace/private-offers-purchase

## 8. 営業向け早見（症状→指す先）

| 症状 | まず聞くこと | 指す先 |
| --- | --- | --- |
| 「販売代理店経由で売りたい」 | ISV が partner に再販委任したいのか、channel partner が顧客に売る MPO か、CSP 経由か | §1, §5 |
| 「CSP で顧客に値引きしたい」 | 相手は Direct Bill/Indirect Provider か。Indirect Reseller ではないか | §5 |
| 「日本円の価格が為替で変わる?」 | market currency、billing currency、payout currency、public/private/plan | §4 |
| 「日本の消費税は Microsoft がやる?」 | 対象国、取引形態、tax-details の分類 | §3 |
| 「Private Offer 受諾後に請求が始まらない」 | accept だけか、purchase/subscribe/activate 済みか。auto activation は on/off か | §6 |
| 「追加クレジットを売りたい」 | renewal、quantity、meter、new plan/product のどれか | §6 |
| 「PO を部署ごとに分けたい」 | billing account type、Azure/SaaS subscription、publisher ID/offer ID、mapping scope | §7 |

## 参照（一次ソース・fetch 検証済み 2026-09-12）

- ISV-to-customer private offers: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/isv-customer
- Resale enabled offers: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/resale-enabled-offers-overview
- Multiparty private offers: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/multiparty-private-offers-overview
- CSP private offers: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/isv-csp-reseller
- CSP margins: https://learn.microsoft.com/en-us/partner-center/customers/csp-commercial-marketplace-margins
- CSP contracts: https://learn.microsoft.com/en-us/partner-center/customers/csp-commercial-marketplace-contracting
- Microsoft Partner Agreement for CSP: https://learn.microsoft.com/en-us/partner-center/enroll/microsoft-partner-agreement
- Agency fee discount for renewals: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/agency-fee-discount-for-renewals
- Tax responsibilities: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/tax-details-marketplace
- Marketplace currencies: https://learn.microsoft.com/en-us/marketplace/currencies
- FX FAQ: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/commercial-marketplace-fx-faq
- Geographic availability and currency support: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/marketplace-geo-availability-currencies
- Plan SaaS offer: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/plan-saas-offer
- Create SaaS offer: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/create-new-saas-offer
- Create SaaS offer plans: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/create-new-saas-offer-plans
- SaaS technical configuration: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/create-new-saas-offer-technical
- SaaS subscription lifecycle: https://learn.microsoft.com/en-us/partner-center/marketplace-offers/pc-saas-fulfillment-life-cycle
- Marketplace policies: https://learn.microsoft.com/en-us/legal/marketplace/certification-policies
- Billing and invoicing: https://learn.microsoft.com/en-us/marketplace/billing-invoicing
- Purchase orders: https://learn.microsoft.com/en-us/marketplace/purchase-orders
- Purchase order mapping: https://learn.microsoft.com/en-us/marketplace/purchase-order-mapping
- Private offer purchase: https://learn.microsoft.com/en-us/marketplace/private-offers-purchase
