# 已确认分类口径与证据示例

适用背景：startrise management民宿业务。用户于2026-09-13确认简化人工分类，2026-09-14要求保存本技能。最新用户指示优先；下列案例用于判断方法，不是按姓名永久匹配的Bank Rule。

## 2026-09-14新增：电商金额阈值与公用事业/保险GST

以下为用户明确指定的账套处理口径，直接用于后续Pending准备；取代此前对电商采购泛泛地“根据商品再决定用品或资产”的做法，不自动重写已Post凭证。

| 条件 | 用户指定处理 |
|---|---|
| 各类电商平台网站的购买金额 < A$300 | Materials & Supplies，Expense |
| 各类电商平台网站的购买金额 ≥ A$300 | Inventory Asset；包括恰好A$300，不再选Furniture等expense类别 |
| Water / 水费 | No GST / GST Free |
| Electricity / 电费、Gas / 燃气 | 通常GST on Expenses；核对本笔invoice，明确例外按票据处理 |
| Insurance / 保险 | 必须按invoice实际列出的GST金额，不自动按整笔10%；stamp duty等非GST项目分开核对 |

- 阈值比较使用对应购买的澳元金额；银行支出的负号只表示方向。A$299.99归Materials & Supplies（Expense），A$300.00和A$300.01均归Inventory Asset。分期或合并交易先对应实际购买金额，不能为绕过阈值随意拆成小额费用。
- 用户名称Materials & Supplies可能在当前账套中显示为Supplies and materials；使用实时科目表核实同一费用科目和ID，不猜账号或另建同义账户。Inventory Asset须核实是资产科目。
- 电商金额规则适用于已确认的购买支出，不包括收到退款、平台佣金、住宿收款或代转资金。Binbin本人合并开具的服务与代购发票仍按其特定Contractor口径；不能把给Binbin的服务付款误认成直接电商购买。
- 已确认电商购买及金额达到阈值时，即使具体房源仍待核，也可以先按指定档位选Category并把房源问题单列；不能因尚未知道买的是哪种家具而继续留下错误expense类别。
- No GST / GST Free、GST on Expenses需映射当前账套实际税码，例如GST free purchases (0%)、GST on purchases (10%)。不要把Out of Scope当作所有No GST的同义词。
- 保险核对总额、保费、GST金额、stamp duty和其他列项；如需拆分或准确填写税額，按invoice保留各组成并验证总额。没有原票或无法确定实际GST时只标待核，不通过整笔10%估算，也不假称税项已核准。

## 用户已确认的业务规则

### 2026-09-14再确认：Pillow Talk、床品品牌与跨账套电商口径

- 用户在 KEWARRANEST PTY LTD / Richard & George business acc 复核时明确：“我们没有furniture”“Pillow Talk……电商品牌卖被品床品的……同理和别的电商平台”。电商采购口径包括床品、家居零售品牌及其官网，不局限于综合购物平台，也不局限于先前 Startrise 信用卡批次。
- 采购支出仍按用户已确认阈值：< A$300 归用品费用，≥ A$300 归 Inventory Asset；不因床品或家居商品而使用 Furniture & equipment。该账套当前用品费用名称为 Printing, stationery & supplies（Expense）；若以后科目变动，先查实际科目。
- 本笔 Pillow Talk，2026-08-06，A$32.70 支出，用户确认床品电商采购，归 Printing, stationery & supplies。GST仍需独立核验，用户确认商品用途不等于税额已核准。
- 对已确认电商品牌的入账退款，沿用用户“打进来的钱都是refund”的口径；未知个人转账、住宿收款及转出退款须按完整备注和实际用途单独核对。不得把现有 Furniture 建议当作电商购买证据。
- 2026-05-19，A$129.90 入账，完整银行描述 Return SP IN2LINEN LARA AU, Card xx7998, Value date: 14/05/2026，支持床品商户退款，使用本账套现有 refund（Other Income）；页面自动带入 Out of Scope (0% Sales)，须在结果中披露，原购买税额仍待原单核对。
- 本账套两笔 Stayz 出款备注分别明确 vrbo comm may 15 与 platform fee march，应为 Platform fee（Expense），不属于商品采购、Furniture 或按金额归 Inventory。
- 本账套2026-04-17 BDGC Tribbeck A$4,564.87是转出，备注 refund feb 20 Gail tribbeck；不能仅凭旧 Furniture 分类改成 Inventory，须核清退款用途及原入账归属。

### 2026-09-14信用卡批次补充：Bunnings与付款单位

- 用户本次明确：“bunning的和电商平台道理相同”。Bunnings采购也适用A$300阈值：低于A$300为Supplies and materials（Expense），达到A$300为Inventory Asset；不再默认一律Repairs and maintenance。该确认针对Bunnings，不自动扩展到所有未知实体或服务商。
- 用户此前圈出Temu的A$1,429.22及A$1,209.28，要求同归Inventory。对这种平台一次合并扣款，以整笔已确认购买付款准备Category，不为套用阈值而按平台内部子订单拆成小额费用；Temu A$1,429.22已整笔改Inventory，旧的742.62资产＋686.60用品拆分方案已撤销。A$81.11及A$49.63仍按原小额口径归Supplies。
- 退款单独核对原购买及资金方向，冲回原购买应属的类别；不能把退款视作新购买机械套阈值。若已Post的原购买科目不符合新确认口径，标出需人工检查的原凭证，本技能不擅自修改Posted。
- 2026-09-14补充：本信用卡批次中，电商平台（包括 Bunnings、Temple & Webster、Kmart、Amazon、Woolworths 等）的正数入账均为采购退款。对 QuickBooks 的 money-in 行，不可选 Inventory Asset；使用账套现有的 **refund** 银行往来账户，页面自动使用 **Out of Scope (0% Sales)**。该规则只适用于已确认平台退款的本批正数入账，不延伸至住宿收入、其他商户收款或未来未知入账。
- 本批所有餐饮、超市、打车、停车、珠宝、电影与钓鱼相关消费，用户已明确确认为公司业务支出。此确认只适用于本批，不等于确认具体商品、GST抵扣、房源或未来所有同商户消费。

| 对象/用途 | 条件和分类 | 不能扩展到 |
|---|---|---|
| 外包人工 | 已确认的安装、组装、维修、园艺、现场协助、跑腿、垃圾清运统一 Contractor Expenses (non salary) | 未知人名、退款、借还款、普通实物采购 |
| 清洁 | 明确房源清洁/洗衣选 Cleaning | 只因发票模板写Service就归人工，或只因银行写Banking就归清洁 |
| Binbin Yao | 用户说明服务与代购合并开成一笔服务发票，此类统一 Contractor Expenses (non salary)，不再要求仅为Category而拆服务和采购 | 其他供应商、用途不同的Binbin付款；GST仍独立核对 |
| Booking.com向外付款 | 用户确认本账户该平台出款为平台佣金，使用 booking platform fee；核对实际商户与付款性质 | 所有包含Booking字样的转账或客人退款 |
| Booking.com/其他平台住宿入账 | 公司同时经营自营及代管；先对房源、订单和结算，再决定平台收入或代收往来 | 将代管全额自动视作公司收入 |
| Stripe住宿款 | 用户希望实际Stripe收入使用 Direct Booking (this one)（Income）。历史存在 Direct Booking（Bank）同名近似科目及自动规则；只做本次Pending判断 | 自动修改用户要求暂时保留的Stripe旧规则，或将同名文字都视作Stripe |
| BP加油 | 实际BP燃油采购用 Fuel & oils | BPAY支付渠道 |
| Ran Bai转入 | 用户说明普通转入基本是借给公司；按对应贷款/往来核对 | 带管理费、代购还款、错转等特定备注的例外；不能仅凭姓名建无限制借款规则 |
| 公司转出给BOQIN TRUST | 用户确认是房东每月净租金结算，核对房源月报及代垫扣款 | Contractor、公司承租租金费用、未经核实的贷款 |
| 代管清洁/维修/采购 | 公司先付，与房东结算时扣除后支付余额。此为已确认现金流程 | 仅凭公司先付款就确定全部属公司损益，仍需账套现行总额/净额或代收代付口径 |

正常个人用餐不是公司外包服务。即便商户已确认是餐饮，也先区分业务支出和个人往来；不把消费地点或个人姓名推成某一房源。

## 已对票案例（2026-09资料）

- 2026-09-14补充，KEWARRANEST PTY LTD：QuickBooks Invoice 1905（txnId=392，客户Louise，19/05/2026）原始行项目写明230 Olinda-monbulk Road, Monbulk VIC 3793，住宿22/06/2026—27/08/2026，总额A$23,664.96。用户提供Fast Transfer From DAVID WHITE, Inv1905 (Louise White)可归属此住宿账单。四笔同名银行入账A$2,000、A$10,000、A$7,000、A$4,664.96合计同额，为匹配线索；逐笔仍核完整备注及收款登记，不将所有未来David White汇款永久归该房。存在原Invoice，应检查匹配而非重复记收入，本技能不实际Match/Post。

| 银行对象/金额 | 对应业务 | 可复用判断 |
|---|---|---|
| Shuping Li $105 | 74 Cobbora Road，BBQ安装、测量、现场反馈，15/04发票 | 人工服务→Contractor |
| Yucan Yu $164.50 | 4 Roseberry，装凳$34.50＋垃圾清运$130 | 本笔→Contractor；同日另一笔$121.80未对票，不重复用同一发票 |
| Zhipeng Zhou $195 | 4 Roseberry现场协助工时 | Contractor |
| CQ Brokerage $170.50 | DEP Mowing，4 Roseberry园艺/绿化垃圾清运，INV00396 | 依用户简化口径→Contractor，而非仅凭brokerage字样判断金融费用 |
| Robert G Taylor $420 / $150 | 302 Toogood：17/08清洁，22/08挂窗帘 | 同一人两种用途：$420 Cleaning；$150 Contractor |
| Wanchai Chang $180 / $332.54 / $120 | 4 Roseberry：垃圾清运、线下采购报销、30%服务订金 | $180 Contractor；$332.54按商品/资产/代垫核；$120须核履约和预付款，不把供应商三个金额全当已结清人工 |
| Washworks $236.28 | 4 Roseberry高压清洗楼梯和BBQ区域，INV1015 | Cleaning |

发票与银行参考号/日期见 source-map 中的原始对照表和证据索引。

## 平台记录可直接回答什么

- **Sheridan Kovac**：台账TXN-5034，74 Cobbora Road，Booking客人，2026-07-01至07-04，订单总额$907；银行07-01同名入账$907。足以说明对应住宿收款。该房为代管；若现行政策代收后结算房东，Rental Clearing是候选，最终科目依实际账务口径，不能作商品销售。
- **Phillip Wheatley**：TXN-4552，5 Scorpio Road代管Booking订单，2026-06-05至06-07，总额$668；银行07-06同名入账$668。说明住宿收款候选与日期差异，核对代收/收入口径。
- **Sandy Iyngkaran**：TXN-5274，2 Colehurst Crescent，Booking客人，2026-07-07至07-09，总额$1,499.72；银行07-08是同额**转出**。可以对上客人/房源线索，不能从订单单独证明已退款，不归Cleaning/Contractor。
- **Mr and Mrs R Logan $1,599转出**：4 Roseberry月报是Richard Logon，订单$1,959减清洁费$360等于$1,599；拼写不同，金额计算只是线索，不能宣布退款已证实。

## 暂选不是确认

- Hasting Varfis $220：历史Cosy Air发票证明供应商及3904/70 Mary地址，七月月报有空调检查$220；缺本笔原票，Contractor为有依据的暂选。
- Massimo/Bonetti $150和$180：302 Toogood维修供应商身份有历史原票支持，但6月两笔具体服务未找到；不能用9月修围栏$250发票冒充两笔凭证。
- Aquatrip $765：TXN-3973为2 Colehurst漏水检测装置，附件名Invoice504836；需要原票和设备/代垫归属，不应按Cleaning。
- ESR Group Holdings为Early Settler的历史家具供应商线索，不证明本笔$395是电商购买或属于哪个房源；若确认本笔为电商购买，按新增阈值归Inventory Asset。Kogan $533.99若已确认是本笔电商购买，则按新口径归Inventory Asset，房源/收据仍可另列待核；不能匹配另一笔历史$1,603.99订单。
- Xu dong dong $70与Xudong Deng清洁发票有名字差异；QBO附着的2月Bunnings$70采购不是8月本笔的依据。
- Vanessa Heit/Helt姓名关联曾只获用户倾向判断；后续确有规则/用户Post也不能自动证明所有别名、服务内容或税务注册永久一致。

## 更新原则

- 2026-09-14执行反馈：用户在已授权批次处理中追问David/Louise White来源后，指出“为什么你没有填写”。在正在处理的批次中，来源查询是对原任务的补充；找到原Invoice和明确依据后，应继续完成已授权的Pending客户归属与匹配准备，不能仅回答来源后结束。仍区分准备与实际Match/Post；现有Invoice收款不要重复填收入类别。

登记新规则时区分“用户确认”“本笔票据/平台事实”“暂选推断”，记录生效日期、对象与用途、房源/主体、Category、GST依据和例外。历史《quickbooks-classification-rules.md》中旧的只读或小额自动Post说明已被当前“助手准备Category、人工Post”替代，不能沿用旧权限。
