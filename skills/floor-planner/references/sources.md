# 数据入口和使用依据

此文件保存导航线索，不是本次房源的实时数据。每次建模重新读取采购和项目内容。

## 飞书新采购表

- [（新）采购总表](https://cn06o0gh8t.feishu.cn/base/E1aBb4oCKaV51RsMVoZcNnb4n9e?table=tblZG1eOOC1JvTYs&view=vewr2po9Zt)
- 来源：本地 `seednest-presign-procurement/references/sources.md` 中2026-09-08核对的入口；2026-09-17创建本技能时读取了该入口记录，未重新核实本表所有实时记录。
- 原已知字段包括：采购编号、英文名、中文名、购买量、所属分类、购买进度、链接、平台、单包装物品数量、总计购买数量、备注、已下单房源、是否补货、父记录。以本次打开的实际字段为准，不固定列字母。
- 当前视图可能带有其他房源过滤条件；既往入口曾按16 Gorman过滤。视图中看不到目标地址不能直接得出“没有采购记录”。优先使用不影响共享视图的搜索/个人过滤。
- 网格读数不便时，可从界面导出“（新）采购总表 / current table”的 Excel/CSV 再按地址筛选。核实导出范围是否受视图过滤，避免误把当前视图当全表；无需导出其他表或无关附件。不要为读取而改写采购行或共享筛选。
- 地址可以有缩写、大小写、unit等差别，结合完整房源信息归一后匹配；同名街道、同楼不同unit、多地址共用行不能混合。
- 其他技能中的历史预算或本地历史快照只能辅助查找，不能代替当前地址本次采购清单。

## Floorplanner 已观察到的项目入口

2026-09-17浏览器标签中观察到以下项目，不代表用户已把它们指定为唯一参考案例：

| 项目 | 链接 | 观察范围 |
|---|---|---|
| 16 the parkway, templestowe | https://floorplanner.com/projects/189532099/editor | 标签标题及链接可见；读取项目内容超时，尚未核实完成度与风格。以后能打开并确认已布置后才可作为案例。 |
| 26 Marianne Way Mount Waverley, VIC 3149 | https://floorplanner.com/projects/189650563/editor | 已打开，页面显示 Room wizard / Upload 2D floorplan / Empty plan 起始选项；本次未创建或修改模型，不能当成熟布置案例。 |

开始实际建模时，从已登录账户项目列表继续查找用户其他已完成案例。根据当前项目内容选取，不预设固定案例名单。用户以后指定的参考项目优先。

新项目起始页已实见 `Upload 2D floorplan` 入口；不同状态/版本的界面可能变化，操作前读取当前页面，不能机械复用坐标。

## 网上2D图与操作文档

- [realestate.com.au](https://www.realestate.com.au/)：按用户当前给的完整房源地址查找具体房源页面和楼层图。记录最终实际使用的页面，不猜图片地址，不把另一套房源图当目标。
- [Floorplanner 官方个人使用介绍](https://floorplanner.com/personal)：说明可上传、缩放已有平面图并通过数值输入调整建筑元素。2026-09-17检索核对。
- [Floorplanner 官方编辑器手册](https://cdn.floorplanner.com/static/brochures/FloorplannerManualEN.pdf)：需要核对背景图比例或尺寸线功能时参考；旧版按钮位置可能不同，以当前编辑器为准。尺寸线可单独编辑，因此显示数字一致不能证明实际墙体尺寸一致。

只在操作需要时读官方说明；不要把第三方教程中的按钮、套餐限制或默认尺度当作已验证的本账户状态。
