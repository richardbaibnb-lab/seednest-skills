# 已核实入口与覆盖基线

建立日期：2026-10-10。下列是首次实查和已存在月度技能的线索，不是未来固定配置，不包含密码。

| 来源 | 入口/定位 | 已知事实与每次必查项 |
|---|---|---|
| QuickBooks | https://qbo.intuit.com/app/banking?jobId=accounting | 实查公司 `startrise management`。银行feed卡片有 `ANZ Business Acc`、`Transaction`；后者科目表Account type为Cash and cash equivalents、Detail type为Transaction，实际银行尾号与收入路径仍需核实，不能因负余额推定信用卡。首次两张卡都有 `Migration required`，不得自行迁移；应检查数据连续性。 |
| QuickBooks George合作 | 同一官方银行入口，切换登录至richardxgeorge2025@gmail.com | 已完成登录，抬头`KEWARRANEST PTY LTD`。银行feed名称`Richard & George business acc`，选择器及列表明确CommBank / Business richard x george (0504)，Open Banking。不能把该银行流水归入Startrise账套。 |
| Airbnb | https://zh.airbnb.com/hosting → 主导航菜单 → 收入；实查链接 `/users/transaction_history` | 四个飞书邮箱均已登录并确认各自出租账号ID，详见account-inventory。已支付页有打款日期、预计到账信息、净额、目的银行尾号、收款编号及订单确认码。不要使用猜测的 `/hosting/earnings` 路径。 |
| Guesty支付处理商 | https://app.guesty.com/financial/payment-processors | 首次实查下列3账户，均Stripe、Active。名称是Guesty显示名称，不证明Stripe法定主体或银行映射。 |
| Guesty付款报告 | https://app.guesty.com/financial/payment-reports/recorded | `Guest payments → Recorded payments`，可见Export、Filters、Columns。字段包括Payment Id、Status、Recorded Date、Payment Comment、Guest Name、Payment Method、Amount、Confirmation Code、Reservation Id、Source、Listing Nickname。首次列表含历史Scheduled/Cancelled，不能把页面标题Recorded payments理解成全部成功实收。 |
| Guesty订单 | https://app.guesty.com/reservations | 用订单支付详情补processor交易ID、房源、收退款。Recorded Date不能替代实际银行到账日期。 |
| Booking.com Extranet | https://admin.booking.com/ → Finance → Financial reports | 实读 `KEWARRANEST PTY LTD / Primary account` 的5房源集团；账户菜单已核实为`manage@seednest.com.au`，不是另一个richard登录账号。已导出2026年9月payout报告。此集团不是全部Booking覆盖。银行转账逐房源核实目的银行，不用集团法人推定统一收款银行。 |
| Vrbo | https://www.vrbo.com/ → 房东入口（以实际可见导航为准） | 用户明确要求覆盖。飞书有自营、代管、George合作、ARG合作4个不同邮箱的记录；详见account-inventory。2026-10-10初次打开首页返回Too Many Requests，尚未读取房东后台；不绕过限流，不把访问限制说成密码错误。 |
| Stripe | https://dashboard.stripe.com/ → 账户切换 → Transactions → Payouts | 切换器5账户均已进入，3个正式商户及旧账户、测试账户情况见下表。Guesty别名与Stripe ID尚未全部建立一对一关系。 |
| Trip.com | https://au.trip.com/list-your-property/ → Sign in → https://ebooking.trip.com/login/index?channel=15 | 已用online账号登录。财务结算含财务首页、现付对账、预付对账、收款记录、VCC管理。按实际收款模式核查，不能点击支付/提现来验证。当前房源的银行资料不完整和提现暂停见account-inventory。 |
| 飞书 | https://cn06o0gh8t.feishu.cn/base/E1aBb4oCKaV51RsMVoZcNnb4n9e | 已实读`公司银行表`和`所有账户`；2026-10-10已导出月度收支表并只读交叉核查。按使用场景定位平台账号，不能把同邮箱的邮箱密码当平台密码，也不批量导出密码库。 |

Guesty首次实查：

| Account name | Processor | 状态 | 关联房源数 | 备注 |
|---|---|---|---:|---|
| kewarranest pty ltd | Stripe | Active | 3 | 不推定与Startrise同一银行 |
| SEEDNEST X ARG | Stripe | Active | 1 | 不推定合作方款均进入用户银行 |
| zh.airbnb | Stripe | Active | 10 | Default；名称不代表Airbnb官方打款账户 |

Stripe与目的银行（只代表已查样本所用账户，历史或其他币种目的账户仍要逐笔核实）：

| Stripe显示名称 | Stripe账户ID | 样本目的银行 | 飞书公司银行表对应主体 |
|---|---|---|---|
| Startrise management（切换器备注Guesty） | `acct_1QN3uaHBiPMGmu2Q` | ANZ / 8504 / AUD | STARTRISE MANAGEMENT PTY LTD |
| SEEDNEST X ARG | `acct_1QzUheEpCKCsmwm0` | CBA / 4484 / AUD | APEX REALTY GROUP PTY LTD |
| kewarranest pty ltd | `acct_1SMnGjG3NAXAK642` | CBA / 0504 / AUD | Kewerranest pty ltd（飞书原拼写） |
| (old not using anymore)（Guesty For Hosts） | `acct_1OIQDaFy1K2pVhAC` | 历史打款8504 / AUD | All payouts实读4笔，均2024年；尚未检查所有活动与未结余额 |
| New business（Guesty [Test mode]） | `acct_1SMmKGH9Q2ZQBP8C` | Sandbox无测试打款 | 页面要求Verify business后才可进入正式账户；本次未进行认证 |

不要仅凭名称将Guesty `zh.airbnb` 自动绑定Startrise；应以订单payment/charge和processor连接资料交叉验证。旧账户的All payouts结果不能单独排除其他未结活动；测试交易应与真实交易分离，每轮复查账户是否已启用正式收款。

Booking集团首次可见房源ID：15783588（Monbulk）、15481965（Hoppers Crossing）、15149443（Kewarra Beach）、15096339（Brisbane City）、14781220（Tanunda）。当时两处关闭，不代表目标期间一定没有尾款。下载报告中15149443打往0504，15783588却打往8504；集团Legal name相同。公司名与收款公司不一致时记录映射依据，并在正式对账确认委托/归属关系。

飞书同一base内已观察的表ID：`公司银行表=tblGxvhMvOHhxKgd`、`所有账户=tblunQRKzGaqSywI`、`（新）每月收入支出表=tblnfgG1sMLVBCrN`、`房源信息表=tblqnyXrZbhCYsrD`。入口可带对应table参数；执行前核验表标题。

QuickBooks主页同时出现 `Direct Booking`、`refund`、`settlement funds`，仅显示In QuickBooks金额；本次没有它们的连接银行余额证据。应核实账户类型，不能直接用这些账面数据证明收款。

## 现有流程关系

- `seednest-property-monthly-finance`：从飞书账户表定位4个Airbnb出租账号，按订单退房月份录入收入；提供账号覆盖和订单桥接线索，不替代银行验证。
- `feishu-startrise-monthly-finance`：公司费用与房源management fee的月度记录；管理费实际银行收付应与对应主体、期间相连，不和住宿平台总流水混计。
- `quickbook-reconciliation-category`：Pending用途和Category准备。其允许分类的授权不延伸到本只读到账对账流程。
- `arrival-payment-watch`：入住前未收款检查；其排除Airbnb的规则不适用于本技能，本技能必须检查Airbnb打款。

## 首次实查的有用现象

- Airbnb的一笔2026-09-28发出A$995.40，订单入住9月27日/退房10月2日；详情显示目的银行尾号8504，净额组成房费960+清洁费240−服务费204.60。QuickBooks ANZ Business Acc在9月29日有A$995.40的PAYONEER AUSTRAL银行入款。飞书8504归属Startrise，但该Airbnb款没有共享银行参考号证据，保留候选匹配。具体订单和打款ID存入当次报告，不作为永久规则。
- Startrise的Stripe A$4,677.32与ANZ 2026-09-24入款金额、日期及追踪号一致（银行将大小写统一）。净额还包括独立的Invoicing Starter费用；不能仅减刷卡费后报少到账。首次检查未做完整退回/冲正扫描，样本到账证据不等于整月或最终留存结论。
- Booking样本A$2,467的报表Statement Descriptor与ANZ 2026-09-04银行摘要前缀对应，银行摘要截掉末位。必须记录截断事实，不称完整参考号一致；结合目的8504、金额、付款方及唯一候选判断证据强度。
- 银行摘要可显示PAYONEER AUSTRAL而非Airbnb；QBO的自动Airbnb类别是线索，不是平台批次证据。
- George合作QuickBooks登录对应KEWARRANEST PTY LTD、CommBank 0504；2026-09-04的Booking 1496和2026-10-05的Stripe 1911.65均已见实际银行入款样本。前者参考号末位截断，后者追踪号完整一致。两笔却均被自动规则归为Airbnb Income / AIRBNB；报告来源与分类差异，不在本技能内改账。具体摘要、页面证据和未完成的退回检查保留在当次报告。
- 实查银行Money in同时有 `FUNDS RETURNED`、`INVALID CREDIT ACCOUNT`、`Wrong payment`、管理费和客人转账。正数不能全部汇总成平台收入。
- Airbnb已支付列表仍有“已发出/最晚到账时间”，预计到达日期不能抄成实际银行到账日期。实际银行交易可能更早。
- 自营Airbnb842.77样本在银行9月30日有候选，同月9月21日另有同额；必须保留不同银行交易，不能同额去重。代管2的4411.86样本在银行9月28日有唯一同额候选，但两例均缺共享参考号，报告仍保留批次待核。所有日期金额查询的唯一性不能代替全链核查。

本文件只保存脱敏的账户结构和工作入口；不保存动态余额、密码、验证码、完整银行账号或把旧交易计数写成新批次总数。

## 2026-10-11补充操作经验

- Booking Financial reports的Custom date range：先选择范围，再点日期输入框获得焦点，以ISO日期填写并移焦后核验显示日期。未聚焦直接fill可能被日期控件重置；生成前必须核验。
- 新报表与历史文件按Statement Descriptor去重，保留新来源。下载事件超时时先查本机Downloads，避免重复生成或重复下载。
- ARG财务概览的收款方式必须逐行读取：关闭房源仍可能采用VCC；不能把集团的每周银行转账扩展为所有房源规则。页面初始占位状态与加载后可能不同。
- Booking登录条款及境外信息处理由用户按当次账号授权；记录已获授权的账号并沿用同一确认，不因恢复上下文重复请求。验证码只用于当次页面，不写入技能或报告。
- 缺共享批次号不必机械地永久留为候选。仅有Payoneer名称或QBO自动分类不够；继续取得Airbnb完整父子组件、目的银行、实际发放和最晚到账日期，核对两个账套同额候选、付款方交叉证据及全范围一对一分配、退回情况。组合证据充分时可核实到账并标“综合证据匹配（无共享参考号）”；银行明确AIRBNB PAYMENTS及直接共享编号分别记录，不把三类证据强度混为一谈。
- Airbnb已支付列表/CSV的日期与“详细信息→发放时间”可能不同（实查4411.86列表9/28、实际发出9/26、最晚10/5）。保留两个原始日期，银行日期单独记录；不能把预计日或列表日当实际银行到账日。

### 2026-10-11追加核对结果（取代上文样本的未结状态）

online、manage、revenue重新登录并下载完整原生字段，原47项订单涉及的43批次均逐个打开。两个QuickBooks重新登录导出ANZ72笔与CBA23笔Payoneer入款；完整原生组成与95笔银行入款一对一相符。43个目标批次为91,325.71 AUD，含8/10月跨月追查；9月原37个候选批次70,501.64全部已完成。842.77两笔与148.48两笔按各自实际窗口分配不同银行行。单次检查证据在该月报告，不将本例推成所有Payoneer款自动属于Airbnb。

9月83项为75银行验证＋8APEX规则通过＋0待核；另发现10月4日manage批次2,306.63的最晚到账日10月9日，现有QBO未找到，单列10月跟进。ANZ仍有Migration required提示，未拿独立银行整月对账单来证明feed绝对完整。
