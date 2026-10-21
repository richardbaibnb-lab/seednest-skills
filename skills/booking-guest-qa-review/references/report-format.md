# 报告数据约定

运行 `scripts/build_report.py INPUT.json OUTPUT.pdf`。输入UTF-8 JSON来自实际采集，不用默认值推断业务结果。输入顺序决定报告顺序，先由执行者按紧急程度排列。

- `title`、`report_id`、`date`、`checked_at`：标题、报告版本、Asia/Shanghai日期、实际采集时间/区间。
- `coverage_complete`：布尔，仅全部账号和房源已枚举且读完才true。
- `summary`：中文短摘要。
- `accounts`：数组，每项 `account`、`group`、`expected_properties`（未知null）、`checked_properties`、`status`、`note`。
- `properties`：数组，每项 `account`、`property_id`（草稿可空）、`name`、`address`、`status`、`question_count`（未查null）、可选 `note`。完整状态只用 `checked` 或 `not_applicable`；`unscanned/login_required/access_failed`不可算完整。
- `questions`：数组，每项 `review_id`、`account`、`property_id`、`property`、`address`、`original`、`translation`、`status`（`needs_facts/awaiting_approval`等）、`draft`（无最终稿可空）、`draft_translation`、`evidence`数组、`unknowns`数组、`source_url`（不含会话参数）、`draft_version`。可选 `visibility`（默认公开）、`question_time`（未显示省略）。
- `changes`：可选字符串数组，记录团队已回答等变化。
- 跨日尚未重读Booking时，设置 `question_count_label`（如“8条历史待办”）及 `scan_notice`，明确原问采集日、今日实际工作和问答当前状态未复查。不得把历史未答数表述为今日新查结果。审阅编号保留原编号日期，生成脚本按实际编号输出页脚前缀。
- 首页表格可选字段（每条问题）：`action_rank`（执行者给出的建议顺序，非平台时限）、`action_label`（如先回复/优先核实/后续核实）、`short_question`、`recommendation`、`next_step`、`evidence_summary`。不提供时按状态及原有译文/依据生成；不要在排版脚本中推断业务紧急程度。
- `display_group`：可选，完全相同的原问、译文、回复、译文、状态、账号与房源可合并显示。脚本核对这些字段一致，保留全部独立编号、数量及对应链接；仅减少重复排版，不合并状态或发布动作。
- 优先采用“首页一页决策表 + 分状态完整回复表 + 房源覆盖附表”。✅表示准备好等用户批准；🔴和🟡分别表示优先/后续核实；⏸表示访问待办。用矢量图标避免PDF缺字，同时配中文状态文字，不能只依赖颜色。

遵守当前PDF技能的创建标记，使用bundled runtime。脚本只排版，无抓取/批准/发布/消息发送功能。生成后文本核对且渲染全部页检查，未验收不得发送。测试数据放work，测试PDF不得当真实日检报告发送。
