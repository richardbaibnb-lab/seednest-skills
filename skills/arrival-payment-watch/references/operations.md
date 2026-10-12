# 入口、通知及状态

## 2026-10-07 已核实的入口

- Guesty：`https://app.guesty.com/`，用户菜单显示 Richard Bai、Startrise Management Pty Ltd。
- 订单：`https://app.guesty.com/reservations`，左侧有 Upcoming unpaid reservations。建立时默认打开的 Sample - In-House Pending Payment 实际只有 Check-out in future、Status Confirmed 两个筛选，包含已入住和余额为零的订单；不能把它当已经筛好的清单。
- 飞书：`https://cn06o0gh8t.feishu.cn/next/messenger/`，2026-10-07 已成功读取消息页和 Sabrina 单聊，标记“外部”。会话中有 `Breezeway周度检查-20260928.pdf`、9 月 21–27 日周报说明、9 月 29 日 11 分 54 秒通话。历史身份线索还有红色“吴”头像。发送前核对会话身份，不按同名猜测。未取得专属会话链接，不编造。
- 两个网页入口当前登录可用不代表将来永不失效。浏览器初始化错误不能当作退出登录；只有读到真实登录页才能判断需登录。
- 2026-10-09 用户授权遇到 Guesty 登录页自行点 Continue：当前记住的账号为 online@seednest.com.au，密码可能在页面初次出现后才自动填入。沿用已填凭据点击 Continue，不读取密码；登录后仍须核对 Richard Bai / Startrise Management Pty Ltd。当天实测点击后进入 SMS authentication，需用户提供验证码或在页面完成；不要自行勾选“Do not challenge me on this device again”。
- 用户明确不需要微信。本流程不启动、不读取、不发送微信。
- 用户于 2026-10-07 明确 Airbnb 默认 OK，以后不进入检查记录或提醒。按真实订单渠道排除，不能把非 Airbnb 订单的 Stripe 账户名 `zh.airbnb` 误当订单渠道。

## 持久状态

本流程状态保存在：

`C:/Users/Administrator/Documents/Codex/2026-10-07/new-chat-3/work/arrival-payment-watch/state.json`

此文件属于运行数据，不是技能模板。每轮先读，原子写入并保留已有记录；同一个 heartbeat 串行运行。需要迁移时先复制完整状态再更新这里的路径，避免去重记录丢失。运行资料留在 work，不写入可分享的技能包。

顶层字段：

- `schema_version`：1。
- `automation_id`：automation_update 返回的真实 ID；创建后补入。
- `schedule`：频率、用户时区、是否已启用；不得仅凭文件写了 enabled 就声称调度成功。
- `source`：来源、账号、付款口径及是否为已披露默认；`excluded_channels` 包含 `Airbnb`，默认正常是业务排除口径，不是实际到账证据。
- `last_complete_date` / `last_complete_at`：只在全量覆盖后更新。
- `coverage`：窗口起止、账号、筛选、预期及已核对数、是否完整。
- `orders`：仅保存当前范围内的非 Airbnb 订单，以账号加真实订单 ID 为 key，每笔保存最近观察、风险分类、是否解决、通知版本及 `feishu` / `codex` 独立发送状态与时间、可取得的消息 ID/证据。旧 Airbnb 条目退出该集合及补发队列；历史扫描快照不覆盖改写。
- `blocker`：原因、首次出现、最近尝试、是否已报告；同一阻塞无变化不反复刷屏。

消息版本含订单 ID、未收金额/币种、付款分类、入住日期及紧急等级。点击发送或工具返回不明不是已送达。平台成功响应/聊天中消息出现才记录 sent；Codex 提醒已实际输出后才能记录对应时间。不得填入假的扫描结果和发送成功状态。

## 2026-10-08 复核口径

- `alert_eligible` 单独表示是否进入预警；正常非 Airbnb 订单可以有扫描记录，但不进入风险笔数、金额与提醒。撤警使用 `resolution_reason: reclassified_normal_channel_flow`，不能伪造付款完成。
- 保留上一版本渠道发送结果至 `notification_history`，本次更正和后续新风险分别记账。需核实金额不计入确认未收金额。
- Guesty [付款状态说明](https://help.guesty.com/hc/en-gb/articles/31041914823709-Finding-a-reservation-s-payment-status)：平台为收款方时，付款状态可能不同步，平台已经向客人收费，Guesty 仍可显示未付。
- Guesty [Booking.com 结算说明](https://help.guesty.com/hc/en-gb/articles/27810859878685-Understanding-Booking-com-reservation-payouts)：Payments by Booking.com 的打款按账户周期，通常在退房后。不能将入住前尚未结算自动当异常。
- Guesty [确认平台代收记录](https://help.guesty.com/hc/en-gb/articles/18095574251549-Confirming-a-payment-for-Payments-by-Booking-com-reservations)：手动确认收款会改变 Balance due；本技能不执行该操作。
- 实测 `Platform` 的 Trip.com 选项不能覆盖 `tripCom2`。完整核查使用日期筛选及 `Source` 栏排除 Airbnb，暂加的列/筛选结束后 Discard，不保存业务视图。

## 建立状态与触发说明

- 2026-10-07 用户已接受每 15 分钟尝试、每天完整检查一次的近似开机检查方案。不是操作系统开机钩子，也不是全天持续扫描。
- 调度提示必须显式调用 `$arrival-payment-watch` 并引用状态文件。保持静默于无变化/无风险；异常、通知完成、失败或需要用户处理时才输出。
- 仅调度工具成功返回后记录 automation_id 和 enabled。重复配置先按已存 ID 查看和更新，不创建第二个监控。
- 官方能力说明：`https://learn.chatgpt.com/docs/automations?surface=app`。本地流程需要电脑和 Codex 可用；发送依赖 Guesty 与飞书的有效登录。系统通知外观及声音不在本技能已验证范围内。
