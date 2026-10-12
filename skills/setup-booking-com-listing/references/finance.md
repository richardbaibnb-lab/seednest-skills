# 银行与收款流程

仅在实际执行 Finance 设置时读取。本文件包含用户要求记住的银行配置，供其 richardbaibnb@gmail.com 的 Booking Extranet 上架流程使用，不用于付款、汇款或其他账号。一般进度与最终汇报只显示银行名称、户名及账号尾号。

## 用户指定的账户

用户明确要求 **Receiving 和 Direct 都按其截图填写**。资料来自图 17，并在图 22 的确认页再次出现：

| 字段 | 值 |
|---|---|
| Bank / Institution | Australia and New Zealand Banking Group Limited（ANZ） |
| BSB | `013189`（如页面要求带分隔符则 `013-189`） |
| Branch | Doncaster |
| Account Number | `652698504` |
| Account holder name | `STARTRISE MANAGEMENT PTY LTD` |
| Account holder street address | `4 Annan Pl` |
| Account holder city | `Templestowe` |
| Account holder postcode | `3106` |
| Account holder country | `Australia` |
| 教学短信号码 | 页面显示 `+61*****3717`（仅为示例掩码，不补全手机号） |

BSB 和账号作为字符串处理，保留 BSB 的开头 0。银行输入框需从页面搜索结果选择准确的 BSB/机构/分行，不只输入文字后假定已选中。不得为了满足长度提示补零或改账号。

账户持有人地址由用户在 2026-09-23 执行 16 Gorman 时明确补充，用于 Direct debit 的 Account holder's details；不以房源地址代替。账户仍相同且用户未更新地址时可沿用。银行分行地址是另一组字段，由选中 BSB 后的平台记录自动填入，不使用账户持有人地址覆盖。

若当前账户信息已完全匹配则保留，不重复提交。若目标已有另一家收款方或不同户名，先核对是否打开了错误的房源/账号；确有与本次授权冲突的旧收款关系时，整理差异供用户决策，不能把参考房源账户当成另一业主的授权。没有冲突且用户已要求本技能设置时，无须再询问是否可以使用上述账户。

## 短信验证：Receiving 和 Direct debit 均遵守

1. 先核对目标 Booking ID、账号与本次编辑的是哪一项银行设置。进入对应编辑入口，读取实际认证页面。
2. 到达 **Select phone number / Send verification code** 时，显示当前页面提供的掩码号码并问用户是否已准备好收短信；等明确回复后再发送。示例话术：“已到 Receiving 银行验证页，短信将发到尾号 3717。你准备好接收了吗？”号码以当前页面为准。
3. 用户确认准备好后发送一次，告知已发送并等待其发来验证码，或由其自行在页面完成后通知。验证码仅用于本次验证，不写入技能、笔记或交付物。
4. 未收到回复不自动重发、不尝试猜码、不用旧码重试。过期或失败时先说明页面结果，等用户同意重发或提供新码，再继续。
5. Direct debit 如果再次要求认证，同样先确认准备状态。用户已明确本次两项均已准备好且授权仍适用时不重复询问；平台复用有效验证、不再要求验证码时也不强行重新认证。

上述等待来自用户明确要求“确定我准备好了”后再发送，不是对整个上架任务额外加审批。等待期间可处理其他独立房源设置。

## Receiving payouts from Booking.com（图 13–17）

1. **Finance → Finance settings → Bank details → Receiving payouts from Booking.com → Edit bank details**。
2. 完成页面要求的短信验证。
3. 在 **Receiving Payouts from Booking.com / New Bank Details** 中搜索 BSB，选定上表银行，填写账号与户名。
4. 检查字段与目标 ID，点击 **Update bank details**。若出现确认页，核对后完成本次已授权的保存。
5. 回到 Finance settings 检查已保存值或审核提示。截图曾提示更新处理需五天，这是历史页面信息；实际按当前页面显示的处理期限与日期汇报。

## Direct debit payments to Booking.com（图 14）

1. **Finance settings → Bank details → Direct debit payments to Booking.com → Edit direct debit**。
2. 若提示认证，按上面的短信流程完成。
3. 使用同一 BSB、账号和户名。用户提供的截图仅显示编辑入口，没有完整 Direct debit 表单；根据实际页面标签填写，不虚构后续控件或把 Receiving 页面当作 Direct debit 成功证据。
4. 核对当前房源及常规 Booking 佣金自动扣款用途，按本次授权保存。若页面要求的声明、授权人信息或新条款超出已知资料，保留已准备好的表单并只询问缺少事项，不猜填或擅自签名。
5. 单独验证 Direct debit 成功/待处理状态。该设置不授权另行发起付款、结清旧账或操作其他账户。

已验证的澳洲页面（2026-09-23，16 Gorman）：Account holder's details 要求户名、Street Address、Zip Code、City、Country/region、Account Number；Bank Details 通过 Select your bank from the list 搜索 `013189` 并选中银行，自动填入 BSB/银行名称/银行地址。该页的 ANZ 记录显示 SHOP 36, THE PINES SHOPPING CENTRE、3109、MELBOURNE；Receiving 页显示 Doncaster，两者 BSB 均为 013189。保存按钮为 Save changes，成功返回 Finance settings 并显示 “Direct debit payments to Booking.com: Your details were saved.”。当时表单提示批准最多需 3 个工作日；后续以实时页面为准，不把保存等同于已完成所有银行审批。

## Payments by Booking.com（图 18–23）

用户教学演示的配置为 **Bank transfer + Weekly (every Thursday)**。

1. 在 Finance settings 查看 **Payments by Booking.com status**。已 active 且配置匹配就保留；pending 时记录状态，不重复激活。
2. 如 eligible，进入 **Learn more** 或当前对应加入入口。
3. 选择 **Choose bank transfer**，随后选择 **Weekly (every Thursday)**，Continue。若当前仅提供其他频率或方式，先说明差异，不擅自改成月付或虚拟信用卡。
4. 读取 Payment process 页面，Continue；PMS/Channel Manager 下拉仅为页面信息时不修改渠道连接。
5. 在 **Confirm your details** 核对 Bank transfer、Weekly、BSB、账号和户名，匹配后按用户教学流程 **Save and activate**。
6. 页面若显示 **Payments by Booking.com is pending** 或银行正在验证，报告“已提交，待平台处理”；只有实际 active 才报告已启用。不要把截图中的 September 28, 2026 当成本次预计日期。

图 19 曾显示服务费 1.9% / reservation；这只是教学时的页面数据，不保证当前费率。实际执行需读取当前页面，按本次已有授权处理；若发现新收费或条件与已知教学方案有实质差异，完成可准备的内容后说明差异，再请用户决定是否接受。

## KYP 与其他提醒

KYP 由用户填写：不因为 Payments pending 就替用户完成 Partner verification。Short stay levy、GST、Invoice details 等提示也不是银行设置指令，不根据截图宣称税务身份或自动提交。需要这些事项才能继续时，准确说明具体阻塞，不夸大为整个流程失败。
