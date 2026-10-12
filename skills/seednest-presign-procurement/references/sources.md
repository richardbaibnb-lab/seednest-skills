# 来源与历史快照

核对日期 2026-09-08。内部参考，不直接复制到房东 PDF。

## 飞书入口

- [（新）采购总表](https://cn06o0gh8t.feishu.cn/base/E1aBb4oCKaV51RsMVoZcNnb4n9e?table=tblZG1eOOC1JvTYs&view=vewr2po9Zt)
- [SEEDNEST库存表](https://cn06o0gh8t.feishu.cn/base/E1aBb4oCKaV51RsMVoZcNnb4n9e?table=tbl8chZFFuvizzmi)
- [SEEDNEST出库表](https://cn06o0gh8t.feishu.cn/base/E1aBb4oCKaV51RsMVoZcNnb4n9e?table=tblHIi2N95jPO5zL)
- [setup发票表](https://cn06o0gh8t.feishu.cn/base/E1aBb4oCKaV51RsMVoZcNnb4n9e?table=tblCtO6NBcof8tK9)
- [最终汇总表](https://cn06o0gh8t.feishu.cn/base/E1aBb4oCKaV51RsMVoZcNnb4n9e?table=tbl3icJSYwtNKO2r)

本次通过界面导出采购当前表，3,729 条。其他入口来自侧栏核对，没有逐行核实库存/出库/发票，不得宣称到仓已确认。

优先用可用连接器，否则用已登录浏览器。画布读数不便时，顶栏更多 → Export → Excel/CSV →「（新）采购总表 / current table」。不选 all tables，不勾附件。下载后本地筛选，不为读数更改共享视图/记录。初始视图按 16 Gorman 过滤，当前视图导出不等于全表。

初始字段：A 采购编号；B 英文名；C 中文名；D 购买量；E 澳币；F 人民币；G 所属分类；H 购买进度；I 总额；J 链接；K 平台；L 单包装物品数量；M 总计购买数量；N 货源情况；O 国内外；P 通常需要单量；Q 备注；R 已下单房源；S 购买日期；V 是否补货；W 通常送达时间；Y 父记录。以后按字段名重新映射，不盲用列字母。

## 随技能数据

JSON 仅为数据。列已缩减，不含发票附件、账号和个人联系方式。价格保留原值，异常标记不代表已修正。按 SKU/采购编号/物品名检索，不必整份读入。

- [au-high.json](data/au-high.json)：920 条初始高档候选。用户工作簿「各房源分账对比表」自营七房源匹配飞书：302 Toogood Rd 169；30 John Harris Drive 141；2 Colehurst Cresent 5；2 Lena Close Swan Hill 3；30 Para Road, Tanunda 222；18 Plaintain Street, Kewarra Beach 226；230 Olinda-monbulk Road 154。记录少的房源不能反推完整开业成本；这不是自管/合买全量分类名单。
- [au-low.json](data/au-low.json)：16 Gorman 227 条，139 已下单、87 未开始、1 状态空白。用户说已买好与表内状态并存，标记状态未必及时，不擅改表。
- [mixed.json](data/mixed.json)：151 Parry 190 条，34 已下单、154 未开始、2 状态空白。有列值冲突，不能整表相加作最终成本。
- [china-supplier-catalog.json](data/china-supplier-catalog.json)：国内商品库 94 个 SKU、43 个供应商，人民币预算价，不证明付款和到仓。
- [china-parry-detail.json](data/china-parry-detail.json)：用户附件「3.151 Parry St, Perth」明细、房间配置，用于数量、床型及去重。
- [snapshot-manifest.json](data/snapshot-manifest.json)：源文件名称/SHA-256、日期、计数和状态分布。

源文件为用户上传的 `全房源组合采买Master清单_10套房源 (15).xlsx` 与飞书导出的 `SEEDNEST民宿总表_（新）采购总表 (1).xlsx`。原始位于 Downloads；技能已独立保存所需数据，不依赖下载文件永久存在。

## 样本价格，仅作历史参考

302 Toogood：King 床垫 A$950（采购商品254，已下单），Queen A$500（255，已下单），冰箱 A$1,040（541，已完成）。16 Gorman：King 床架 A$309（4674，已下单），King 床垫 A$334.20（4675，未开始），Queen 床垫 A$249（4677/4923，未开始），沙发床 A$449.80（4722，已下单）。未逐笔核对付款发票与当前价格。

## 已发现的问题

1. Excel 53 个表存在重复展示；CNY 49,536.17 覆盖 10 个组合对象，其中「墨尔本仓库1」CNY 19,246.74、502 件，不是十套全新空房的完整配置均价。
2. 多个自营房源为日常补货，床单/床笠量为 0，不能当新房配置。
3. Excel 151 Parry 标为5房2卫、5床、9人。有价明细 CNY 9,273.80、264 件；另有 SKU-1012 鲨鱼小熊 2 件价格未定，展示总件数266。因此金额不含全部物品，更不含全房家具及运费。
4. 国内 SKU-9003 白色贵族面包机一处分类为家电，材质木质、供应商玩具厂、供应商分表分类儿童玩具；不是真家电。飞书 4895 英文亦为 Wooden pretend coffee machine。
5. 飞书 `3.22采购商品4005` 英文 Bed frame double、中文 A6台卡、AUD229/CNY25，冲突未解决前不作为有效价格。
6. `3.22采购商品4072` 平台/链接1688却标澳洲，且中文备注待替换；渠道及最终型号待核。
7. `3.22采购商品4174` 英文洗衣机，中文和链接是烘干机；不能计作洗衣机。
8. 16 Gorman `4844` 冰箱、`4845` 洗烘一体数量0；新房需求独立判断，价格为计划参考。
9. setup/二版数据及状态空白可能混有计划、替换和实际采购；预筛标记不代表未标记行已全面核验。
10. 2026-10-12复核：26 Marianne的`4997`等「枕头（软）」记录链接指向`hypoallergenic-microfibre-junior-pillow`，不能作为成人睡眠枕规格。成人枕可另核16 Gorman的`4938`等相符规格；不要仅因中文标签相同直接套用价格。

以后获取新数据再更新快照及日期，保留三档定义；取得真实入库与可用数量后才能把仓库货切换为可用。
