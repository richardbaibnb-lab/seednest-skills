# 按实际资金路径核对

## Airbnb

逐出租账号读取Earnings的Paid、Upcoming以及相关退款/调整。Paid原生导出保留全部可用字段，并对差异打开单笔详情，获取收款编号、目的银行、批次内订单/调整。Upcoming用于发现应付但尚未发出的款，不以Paid导出当完整应收清单。

账户、listing、确认码、支付事件/分期ID、打款ID建立关联。一次打款可能有多订单、多房源、退款或共同房东分配；不能将汇总打款行和订单子行一起累加。0元批次先查净额抵扣组成，不期待0元银行入账。长住每个实际分期保留，未来尚未到期分期不列逾期。

平台发出≠银行到账。以本笔显示的预计日期为准；只有一般帮助说明时注明估计，不写死统一到账天数。首次实查可见PAYONEER付款方；须逐账号核实路径。

本机中文日期输入使用页面接受的YYYY/MM/DD；导出CSV日期可能是MM/DD/YYYY，先核实表头和实际样本再转换。分别核对Paid父行金额与带符号子行；Upcoming按全部日期检查后才筛目标月，不把未来分期金额当本期漏款。

## Booking.com

进入Extranet，按实际有业务的房源/子账户检查Finance、payout statement、付款明细、佣金及调整。不能只查一个酒店ID或集团汇总。逐房源确认：

- **平台银行转账**：订单归入哪个打款批次、payout date、bank transfer reference、币种、目的银行、净/毛结算方式。佣金另付与已扣佣金分开处理。
- **虚拟信用卡VCC**：可用余额/激活日/到期日/已扣款状态只说明VCC阶段；核实处理商实际扣款及其银行打款。本技能只查，不执行扣卡，也不导出卡号/CVC。
- **物业自行收款**：追Guesty/Stripe或直接银行付款，不等待一笔本就不会由Booking发出的银行款。

检查取消费、退款、扣款抵销及到期仍未兑现的VCC。Booking发票证明费用，不能单独证明平台已向银行付款。

首次实查的集团Financial reports可按Last month/起止日期生成CSV。只生成本次报告；不要勾选Get recurring reports via email或发送报告。2026年9月样本字段包括`Type/Transaction type`、`Statement Descriptor`、`Reference number`、`Property ID`、`Legal name`、`Payout type`、`Payable amount`、`Payout amount`、`Payout currency`、`Payout date`、`Bank account`。`(Payout)`是批次父行，`Reservation`是订单子行；按Statement Descriptor等批次键关联，银行打款总额只汇总父行Payout amount，不能把父子两行重复相加。样本Payout type为Gross：银行匹配按报表Payout amount，佣金另查发票/扣费证据，不自行再次扣佣金。字段和导出形式可能变化，先查实际表头。

同一Legal name的不同房源可向不同银行尾号打款。摘要若被银行截断，保留平台完整值与银行原文，只能按有说明的前缀对应结合其他证据，不随意删字符制造相等。

## Guesty

先看Payment processing清单与房源分配，再读取订单Payments和Recorded payments报告。Scheduled、Pending、manual recorded、Succeeded、Refunded分别保留原状态；手动确认或Balance due=0不能单独证明现金进入银行。

记录订单来源、房源、Guesty reservation/payment ID、支付方式、处理商账户及原支付ID。Airbnb/Payments by Booking.com由平台收款时，以原平台为结算证据，不能把Guesty同步延迟造成的未付余额当平台欠款。银行转账或现金的人工记录要有银行/其他原始收款证据。

只有实际启用GuestyPay才追GuestyPay payouts；不要看到产品宣传就新增一条虚构收款路径。处理商为Stripe则沿Stripe继续。

订单退房月导出须涵盖全部状态，再区分confirmed、canceled、inquiry和declined。询价里的Balance Due是报价，不能作为确定应收；取消后0元也可能存在已经发生的直接银行入款，反查取消前金额、订单尾号与实际住宿。Recorded payments可能仅覆盖Booking人工/同步记录，须看实际Source/Method分布，不能当全部处理商收款报表。

Guesty显示Not paid时，先查原payment，再查同客人的独立Stripe发票或直接转账。历史失败可与后来另开发票成功并存，不同支付ID不要混为同一次重试。逐一追到payout与银行，不能因Guesty未同步而误报欠款。银行毛额与飞书扣除佣金、税费后的净收入允许口径不同，差额必须有原报表组成。

本机Reservations列选择需点列菜单内Save才应用，随后Export CSV可能异步出现“Your CSV is ready / Download”提示；检查实际下载文件行数与字段。该原生导出当前会自动给账户邮箱发副本，不另点Email report。最终Discard临时视图修改，不保存为共享业务视图。飞书导出仅选（新）每月收入支出表，不能连同整库密码表一起导出。

## Stripe

逐商户/connected account在Live模式读取Payments、Balance transactions、Payouts以及失败、退款、disputes/chargebacks和准备金。按实际权限和报表入口取数据，不创建密钥或连接新金融账号。

关联顺序：Guesty payment/reservation → Stripe payment intent/charge → balance transaction → payout ID → destination bank → bank transaction。

自动打款可使用Payout reconciliation报表/批次明细验证gross、fee、net、refund、adjustment和净额；只看Payments成功金额不能当银行实收。手动打款不强行声称系统具有逐charge归属，用平台余额滚动（期初余额+净变动−打款=期末余额）与单笔payout到银行验证，并明确订单到批次分配限制。

除每笔支付处理费之外，独立Stripe费用（例如Invoicing Starter）、相关税费等也可能进入打款净额。逐行使用带符号的Total求和，避免把Summary里的Gross、Fees和Total三个字段重复相加；明细、Summary与payout金额须相符。首轮实查样本为4779.90−81.55−19.12−1.91=4677.32 AUD，此例只解释核对方式，不是固定费率。

注意payments currency与settlement currency、automatic/manual、pending/in_transit/paid/failed/canceled、available与pending余额。若历史paid后来failed或银行退回，要更新原差异状态。

## Vrbo

用户2026-10-11另明确APEX / 19 Lugano / 尾号4484的银行流水无法读取：有平台或Stripe实际转款记录即可默认通过，单列“银行未验证”。该例外同时适用于此房源的Airbnb、Booking及Vrbo经Stripe转款；不再要求APEX网银或流水，不扩展到8504、0504或其他房源。仅有支付成功而无转款、已知失败/退回或金额差异不能默认消除。

用户2026-10-11确认本业务Vrbo全部经Stripe。当前默认从Guesty全量订单识别Vrbo/Stayz/HomeAway，逐单核实Stripe原支付（含早期失败后独立发票成功）、费用、退款/争议、payout及QuickBooks银行。按实际已核订单判断客人付款，不把Vrbo网站无法登录继续当作同一笔Stripe付款核查的阻碍，也不期待第二笔同额Vrbo银行款。网站未登录仍如实列示；仅当存在未同步渠道订单或具体业务差异时补Vrbo后台资料。其他新发现的资金路径以原始证据为准。

保留Vrbo预订标识与Guesty确认码，区分租金、清洁等收费、客人服务费、押金/预授权、税款、佣金、退款以及实际可付用户的净额；实际承担和代收方以订单/报表为准。核查分期、取消款和争议，平台订单显示已付不能替代银行证据。遇到限流或访问限制时保留具体阻碍，不换工具或端点绕过。

## Trip.com / eBooking

从已登录账户的财务结算读取财务首页、现付对账、预付对账、收款记录和VCC管理，先核实当前房源和可切换的其他房源范围。分别记录平台财务房源ID与公开房源ID，不假定编号相等。按页面确认的银行转账、VCC、Payoneer、酒店现收等方式追查，不能把现付订单视为平台欠付。

收款记录保留申请号、提现日期、支付日期、状态、支付类型、实际付款金额；写清所用日期筛选，空结果不能代替订单应收检查。财务首页的自动支付、支付周期、可提现时间等只代表当前页面设置，不能套给其他账户或历史订单。银行资料不全、预付暂停、KYP未完成单独列为配置/验证缺口；未找到相应应收订单前，不虚构被冻结金额或漏款。该流程只读，不执行支付、提现、VCC扣款或修改银行信息。

## 其他实际发现的收入

Vrbo、直接预订、延住/额外收费、取消费、赔偿及公司管理费，只有在订单来源、平台清单或银行流水中有证据时纳入，并追其实际收款方和银行路径。归还贷款、内部资金划转、垫付款退回等另列，防止住宿收入重复。

## 官方资料（核查日期2026-10-10）

平台规则变化或解释状态时，回查对应官方页面，以账户自身结算设置和单笔详情优先：

- [Airbnb：Find your earnings](https://www.airbnb.co.uk/help/article/304) — Paid/Upcoming、合并打款、收款编号与导出。
- [Airbnb：How you’ll get paid for hosting](https://www.airbnb.com/resources/hosting-homes/a/how-youll-get-paid-for-hosting-20) — 释放时点和到账时长属于不同阶段，长住可能分期。
- [Stripe：Payout reporting options](https://support.stripe.com/questions/payout-reporting-options?locale=en-GB) — 自动打款对账报表与手动打款的归属限制。
- [Stripe：Payout object](https://docs.stripe.com/api/payouts) — arrival_date、destination和状态；paid可能随后变failed。
- [Booking.com：Managing payment and payout details](https://developers.booking.com/connectivity/docs/payments-api/managing-payment-and-payout-details) — 银行转账日期/参考号与VCC不同状态。此处仅解释字段，不授权调用或开通API。
