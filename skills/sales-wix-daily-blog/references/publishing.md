# Seednest Wix发布参考

已确认网站ID和作者ID见 SKILL.md。2026-10-19首次核查：正式站有3篇已发布文章，没有未发布或预约文章；本技能的首篇另存于运行目录2026-10-20。

## 文档与接口

使用 WixREADME 和当前 wix-manage 技能；对不明确的字段用官方文档和schema核实，不凭记忆构造请求。

- [创建草稿](https://dev.wix.com/docs/api-reference/business-solutions/blog/draft-posts/create-draft-post)：POST https://www.wixapis.com/blog/v3/draft-posts 。body为 `{draftPost:{title,memberId,richContent,excerpt,seoSlug,seoData,media},publish:false,fieldsets:["URL"]}`。只发送核实的字段；首篇已验证这些字段。
- [列出草稿](https://dev.wix.com/docs/api-reference/business-solutions/blog/draft-posts/list-draft-posts)：GET https://www.wixapis.com/blog/v3/draft-posts ，响应 `draftPosts`、`metaData`。同一列表可包含 PUBLISHED、UNPUBLISHED、SCHEDULED 状态；预约时间字段 `scheduledPublishDate`。
- [更新及预约草稿](https://dev.wix.com/docs/api-reference/business-solutions/blog/draft-posts/update-draft-post)：PATCH https://www.wixapis.com/blog/v3/draft-posts/{draftPost.id} 。2026-10-19核实的请求为 `{draftPost:{id,richContent},action:"UPDATE_SCHEDULE",scheduledPublishDate:"<目标UTC时刻>",fieldsets:["RICH_CONTENT","URL"]}`，成功返回 `draftPost`。这是请求顶层的预约字段；草稿实体内部同名字段只读。首篇加图时已验证200、SCHEDULED及原预约UTC时刻。可优先用此接口预约，再预览核对；不要使用立即发布的 UPDATE_PUBLISH。
- [博客后台和读取接口](https://www.wix.com/skills/wix-manage/references/blog/blog-dashboard-navigation.md)：GET https://www.wixapis.com/blog/v3/posts ，响应 `posts`、`metaData`。此路径在本网站已返回200。注意“posts-stats”文档可能返回不同的 /v3/posts 路径，不能混用。
- [会员](https://dev.wix.com/docs/api-reference/crm/members-contacts/members/member-management/members/list-members)：GET https://www.wixapis.com/members/v1/members?fieldsets=PUBLIC&paging.limit=50 。只取作者所需的id、公开昵称。
- [发布现有草稿](https://dev.wix.com/docs/api-reference/business-solutions/blog/draft-posts/publish-draft-post)：POST https://www.wixapis.com/blog/v3/draft-posts/{draftPostId}/publish ，body为{}，响应 `postId`。此操作立即发布，只在用户明确要求即时发布时使用。
- [Ricos官方写作说明](https://www.wix.com/skills/wix-manage/references/rich-content/author-ricos-rich-content.md)：手工生成richContent前必须读。段落、标题和列表正确嵌套，节点之间保留适当空段落。CTA使用有效的BUTTON节点，正文站内链接使用LINK decoration。

首篇验证的SEO字段：
```json
{"seoData":{"tags":[{"type":"title","children":"SEO title | Seednest"},{"type":"meta","props":{"name":"description","content":"Page summary"}}]}}
```

自有图库封面已核实示例：`6e93f7_1b160e7ef49f4554bb133b6d4a780795~mv2.jpg`，2048×1360，木质天花和大窗客厅。来自 https://www.seednest.com.au/gallery 。仅作为通用图库照片，不推断地址。封面结构 `media.wixMedia.image.id`，同时设置 `displayed:true,custom:true,altText`。每篇应选相关图片，不长期机械复用一张。

正文使用Ricos `IMAGE`节点，`imageData.image.src.id`填真实媒体ID并附宽高，`imageData.altText`描述可见内容，`imageData.containerData`指定居中和CONTENT宽度。英文图注放入该IMAGE的CAPTION子节点，再嵌套TEXT；图片后保留一个空段落。首篇的完整有效请求及三个图文对应关系保存于运行目录 `2026-10-20/update-images.json` 与 `images.json`。后续编辑前先读原始richContent并按ID和图注去重，不反复追加。

## 预约发布

后台入口：https://manage.wix.com/dashboard/a35b6617-3600-4d66-9869-2906a9ae3fb5/blog/posts 。

优先使用上述UPDATE_SCHEDULE接口，明确传入目标UTC时间，核对响应的SCHEDULED及scheduledPublishDate，并在Chrome预览图片和文字。需要界面预约时：

1. 进入Drafts，按本次准确标题找到草稿并Edit，查看正文、封面、链接和SEO。
2. 从发布按钮旁的菜单选择Schedule。按实际界面选择日期、时间和时区。界面文案或控件变化时读取最新状态，不复用旧元素编号。
3. 计算目标日期Australia/Melbourne 09:00的UTC时刻，再核实界面显示时区。本机2026-10-19实际显示 `Timezone (GMT +08:00) Asia/Shanghai`，所以2026-10-20墨尔本09:00填为10月20日06:00 AM；标准时间期间通常对应上海07:00 AM。每次按目标日期转换，不固定填写06:00。点击日期，设置Time，再点击Time标签使输入失焦，读取最终值后点击Schedule。
4. 提交后从Scheduled列表及 `scheduledPublishDate` 核对目标；保留截图及草稿ID。
5. 草稿实体内的 `scheduledPublishDate` 只读，但Update Draft Post请求顶层支持该字段，须与UPDATE_SCHEDULE配套。不要拿 `firstPublishedDate` 冒充计划时刻，也不要使用社交媒体营销计划的ScheduleDrafts代替Blog预约。

发布后的URL以API或界面返回为准。创建响应的预览url可能与 `seoSlug` 字段不同，不能自行拼接一个链接当作已验证上线地址。

## 读取与恢复

ExecuteWixAPI内 `wix.request` 响应为 `{status,data}`；业务对象从 `data`读取。把可预知的读和写放在一次有条件执行中，写前查重复。发布前的生成和审核是实际依赖，允许独立只读准备。成功响应已经证明写入时不重复写；预约属于浏览器的另一步，读取预约结果可用于确认时区。

先记录目标日期和slug；创建后保存ID，再预约同一ID。中断后优先继续既有草稿。身份或权限变化时不要尝试其他同名网站。需要新增图片时按当前媒体文档上传，不能编造媒体ID。
