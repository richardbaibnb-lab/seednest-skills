# 入口、已有成果与生成器说明

来源：用户2026-10-15提供四张截图及业务要求；当日通过Codex内置浏览器只读核实飞书房东信息表、AI汇总表及Seednest Reporter界面。截图历史月份、房东、房源数量均为示例，不是未来固定配置。

## 飞书与归档路径

| 用途 | 入口/定位 | 执行时核对 |
|---|---|---|
| 民宿管理表/SEEDNEST民宿总表 | https://cn06o0gh8t.feishu.cn/base/E1aBb4oCKaV51RsMVoZcNnb4n9e | 左侧表名与房源，不以当前打开的表推断用途 |
| 房东信息表 | https://cn06o0gh8t.feishu.cn/base/E1aBb4oCKaV51RsMVoZcNnb4n9e?table=tblOwML4TewFxOEw&view=vewhRDtPe3 | 已实读列：房东编号、房东名、房源地址、联系方式、结算方式；用户补充截图还明确折扣类型、生效/终止日期、给推荐人比例及推荐人关联，需横向展开读取 |
| AI 汇总表 | https://cn06o0gh8t.feishu.cn/base/E1aBb4oCKaV51RsMVoZcNnb4n9e?table=tblU2bldAVOwxypk&view=vewnajUWAb | 选备注“月度reporter，excel转pdf，也可以转化excel成报价单report”的记录；不要误用Invoice generator或出库invoice |
| 代管房源云盘 | https://cn06o0gh8t.feishu.cn/drive/folder/JqlYfRlDJlcN5edvOJxccsXRnic | 进入`Monthly report`再进月份文件夹；同名快捷方式以实际父目录为准 |
| Monthly report总目录 | https://my.feishu.cn/drive/folder/Xs49f6vc2lD9MFdSKzMcg35Nnxg | 从代管房源中的`Monthly report`实际点击取得，执行前回读面包屑与标题 |
| 月报Excel | 云盘 → 代管房源 → Monthly report → YYYYMM | 用户截图4是202608示例，文件名如`2026-08 Report - 完整地址`；不是房源各自的发票月份文件夹 |
| 支出原始凭证 | 自管房源或代管房源 → 完整地址 → 日常维护发票 → 年份 → 目标月 | 按当月实际目录和已有归档惯例定位，不把月报文件夹与发票文件夹混用 |

收费表实查存在不同计费文字：按总流水15%（包括清洁费）、扣平台费后总流水15%（包括清洁费）、总流水减清洁费后16.5%（包括平台费），以及软件费另付等附加约定。这些是需要区分的计费类型，不是任何房源的永久费率。每次读取该房源当月适用原文；不能把括号内的“包括平台费”等措辞忽略，也不能机械推导GST。

房东信息表与Guesty可能有显示名差异、同一房东多房源及历史条目。以完整地址和关联关系交叉匹配；房东编号与Guesty owner ID分别保存，不混为同一ID。

用户同日补充截图显示：部分折扣有起止日期，部分为空；标签有`1% off`、`2% off`、`5% off`；推荐人比例有`0%`、`5%`，另有单独的推荐人分组。截图不能确定折扣算法、空日期的含义或推荐分成基数，需与相应房源历史公式/备注核对。有推荐分成不意味着可以向房东新增同额收费。不要把截图上的2025/12/01—2026/12/01等示例日期推广为全部房源的有效期。

## 月度AI生成器

经飞书AI汇总表第一条月度链接实际打开：

https://copy-of-seednest-reporter-854716730753.us-west2.run.app/

页面标题`Seednest Reporter`，主标题`Seednest Report Generator`。实查上传页：

1. `1. UPLOAD LOGO (OPTIONAL)` / `UPLOAD`：本工作流仍必传logo。
2. `2. Monthly Earnings Report` / `Rental revenue & expenses` / `Owner Statement (.xlsx)`：选此入口。
3. `3. Purchase Excel Report` / `Purchase List (.xlsx)`：不是房东月报入口。

实查月报预览提供`Property Address`、`Statement Period`、`Download PDF`，空地址时提示先填写。主要输出区：

- `Rental Activity`：Guest、Dates、Channel、Gross、Cleaning (paid by guest)、Platform Fee、PM Commission、Payout及Subtotals。
- `Expenses & Extras`：Concept、Note、Amount；费用可切换Expense (-) / Credit (+)，可Add Item。
- `Net Distribution`：Rental Revenue、Total Expenses、Total Payout。

这些仅是页面字段，不证明Excel导入已正确。核对各订单列和费用符号，尤其`Payout`小计与`Net Distribution`是否取自同一已重算数据。创建技能时只查看了内置示例，未上传真实月报、未验证完整Excel解析/导出链路。示例里的日期、数值、名称和税率不得带入正式报告。

logo：[assets/seednest-logo.png](../assets/seednest-logo.png)。这是从本机既有`seednest-presign-procurement/assets/seednest-logo.png`复制的原始SEEDNEST深绿色金色品牌图，来源技能记载用户2026-09-09指定新版logo；本次创建时已目视核对。用户以后提供更新版本时采用更新版。不要继承采购PDF的预算布局或采购计算规则。

## Guesty上传入口（用户截图2、3）

- Owners列表：https://app.guesty.com/contact/owners
- 菜单：`Operations → Portfolio → Owners` → 目标房东 → `Documents` → `Add document`。
- 截图3展示的是George的Documents和多房源月报；不要硬编码示例owner ID作为上传目的地。
- 既有文件名为`YYYY-MM Report - 地址`，Document type为`Other`，Visible in Owners Portal为`Yes`，生效/到期日期显示为空。实际以目标owner当前惯例和用户要求为准。
- 这是用户确认PDF后才执行的步骤；创建本技能时未在Guesty上传任何文件。

## 可复用技能与成果边界

以下链接从本参考文件所在目录解析。只有需要其对应步骤或核查复用成果时才读取，不因关联就全量运行。

| 既有技能 | 可复用内容 | 不能自动继承的动作/结论 |
|---|---|---|
| [seednest-property-monthly-finance](../../seednest-property-monthly-finance/SKILL.md) | 目标房源当月收入支出记录、发票附件、Airbnb退房月归属与导出证据 | 存在记录不代表已收款；周期费用续用先核对房东承担条款；不为月报重复录飞书账目 |
| [operation-quickbook-monthly-bank-reconciliation](../../operation-quickbook-monthly-bank-reconciliation/SKILL.md) | 订单/平台/Stripe打款到QuickBooks银行的完整核查、覆盖清单、未结项及截止日；Vrbo经Stripe；APEX/19 Lugano限定例外 | 历史样本不等于当月全量；用户规则通过不等于银行验证；不照搬旧月份的完成数量 |
| [feishu-property-pdf-filer](../../feishu-property-pdf-filer/SKILL.md) | 已归档发票、服务期间、地址映射、清洁日期/数量与重复核验结果 | 本月报任务不自动触发向供应商/Sabrina发消息、移动原件或追加发票归档流程 |
| [operation-thursday-invoices](../../operation-thursday-invoices/SKILL.md) | 已下载的本地周度invoice附件及原始邮件来源线索 | 下载完成不等于费用已核实或已入账，不为一个缺项重跑所有邮箱 |
| [feishu-startrise-monthly-finance](../../feishu-startrise-monthly-finance/SKILL.md) | 房源Management fee与公司管理费的交叉检查；既有规则会从Monthly report的PM Commission取数 | 不能以该下游金额证明本报告计算；本流程不回写公司账、不删除重复账目；旧Chrome偏好不覆盖当前默认内置浏览器 |

需要新取账目证据时可继续读银行对账技能的[account-map](../../operation-quickbook-monthly-bank-reconciliation/references/account-map.md)和[platform-reconciliation](../../operation-quickbook-monthly-bank-reconciliation/references/platform-reconciliation.md)。动态账户/房源范围每次核对；不要把用户名、密码或完整银行账号复制到本技能。

## 复用/续做最低记录

一行对应一个房源和报告月，至少能回答：

- 采用哪个上月Excel、哪条房东收费规则、什么月份口径；
- 哪些支出/平台导出/银行核查已经完成，原证据在哪里、截止何日，哪些需补查；
- 新Excel和PDF的文件名、版本标识、飞书月份目录及文件直达链接；
- 用户确认了哪些房源/月份/版本，何时确认，是否之后又修改；
- Guesty目标owner及其房源关联、是否有同月文件、是否上传且回读核验。

这份记录用于避免重复作业与串房源，不作为房东PDF正文。房东报告保留有用财务明细；账号覆盖、原始银行证据、计算审计和用户确认记录留作内部资料。
