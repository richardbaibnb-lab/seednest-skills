# 账号、收件人与状态

## 当前浏览器连接验收

2026-10-20本机官方插件版本26.928.31416：没有独立的旧CUA工具名仍可连接。官方 `browser/scripts/browser-client.mjs` 提供 `setupBrowserRuntime`，其返回值就是Agent；必须接收返回值，不能假定调用后自动存在全局 `agent`。通过当前可用的 `node_repl` 调用官方客户端，再按 `agent.browsers.list()` 返回值选择Chrome扩展，读取该浏览器完整文档并命名会话。插件路径应按本机当前版本发现，不把此版本写成永久路径。

本次已实际读取Booking登录页与飞书所有账户表。首次绑定曾明确报告不可用，按官方文档重新取得同一Chrome配置的新绑定后继续成功；仅证明本次恢复，不保证永久稳定。旧“缺少入口”阻塞已经解决，后续先复用现有运行环境和可用绑定，勿重复要求用户选择Chrome或重新登录。

## 初始账号

依据本机既有 `operation-quickbook-monthly-bank-reconciliation/references/account-inventory.md`：2026-10-10实读飞书SEEDNEST民宿总表“所有账户”，2026-10-11登录核实。每轮重查全部Booking记录，历史数量不是上限。

| 登录邮箱 | 集团 | 覆盖基线 |
|---|---|---|
| richardbaibnb@gmail.com | STARTRISE MANAGEMENT | 2026-10-19实际读到账户身份与18个正式房源（2个关闭），另1个未命名中国注册草稿 |
| manage@seednest.com.au | KEWARRANEST PTY LTD | 历史5房源，本技能建立时未登录检查 |
| seednestxarg@gmail.com | APEX REALTY GROUP | 历史3房源，本技能建立时未登录检查 |

历史账号存在不等于今天已查，不可把未查账号写成无问题。使用官方登录与现有凭据，不保存密码/验证码/Cookie/ses/op_token。切换后在后台菜单核对邮箱。

2026-10-19主账号正式ID：17478584、17376634、17310320、17285461、17258768、16855123、16480425、16389553、16190361、16190359、15612324、15495774、15495607、15097778、13451315、13387080、11839232、11154640。仅作查漏基线。16389553/16855123同址，16190359/17258768同址，按不同ID各查。

## 吴的身份

- 入口 `https://cn06o0gh8t.feishu.cn/next/messenger/`。
- 用户2026-10-19指定紫色/粉紫底白字“吴”头像、标题“吴”的单聊。Sabrina是另一红色“吴”头像、带外部标签的聊天，不是本任务收件人。
- 建立时实际打开吴会话，读到10:15的 `hello`、`嗯嗯嗯`、40分56秒通话、`Breezeway周度检查-20261019.pdf`及13:59摘要。未取得稳定会话ID，不编造。
- 每次发前核对标题、头像和上下文，身份已明确不用重问。身份不明保留待发，不发给其他同名联系人。
- 发送授权限本任务问题与拟回复PDF，不包含无关聊天或整张凭据表。收件身份不等于批准Booking回复的权限。

## 持久状态

状态：`C:/Users/Administrator/Documents/Codex/2026-10-19/new-chat-6/work/booking-guest-qa/state.json`

证据/结构化运行数据在同一work目录；最终PDF在 `C:/Users/Administrator/Documents/Codex/2026-10-19/new-chat-6/outputs/`。运行数据不混入技能，原子保存，保留历史发送与批准记录。建立技能不代表扫描完成，不预填成功日期。

字段：

- `schema_version`、`automation_id`、`timezone`、`schedule_enabled`、`last_scan_complete_date`、`last_report_sent_date`。
- `runs[date]`：开始/截止时间、账号枚举完整性、每账号预期/已查数、逐房状态、完整/部分、未运行日、阻塞、报告版本。
- `accounts`：邮箱、集团、来源、身份核实时间、房源ID；历史数量与本轮数量分字段。
- `questions[local_key]`：审阅编号、真实问题ID（可空）、账号/房源/原问、语言、可见提问时间、采集时间、已清理URL、最新状态；draft精确文字/译文、依据、未知项、版本/hash。
- `approvals`：报告/版本、获批编号、文本hash、批准人、可验证原文/来源、时间、可见范围。不得套用到新版本/新问题。
- `reports`：日期/版本、路径/hash、覆盖快照、PDF验收；feishu状态 `pending/sending/sent/uncertain/failed`、真实时间及可得消息ID/截图。
- `publications`：问题/稿版本、批准引用、时间、状态 `not_submitted/submitting/uncertain/failed/submitted_pending_moderation/published/answered_by_other/archived_by_other` 和回读证据。
- `blockers`：首次/最近时间、失败阶段、上次提醒、下次可重试时间。初始化失败与登录失败分开。

所有问答页面已读完，但答案事实未知时，扫描可完成、回复仍待核实。账号无法访问则扫描不完整。PDF可报告部分覆盖，但不能将日检标为全完成。设置期间的一条真实样本不代表18套房已检查；正式日检重新查当前全量。
