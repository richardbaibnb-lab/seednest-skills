# PDF 输入

脚本用于已完成选品与币种换算的明细，不会自行从历史数据推断新房配置或更换档位。

运行：`python scripts/render_estimate.py input.json output.pdf`。用当前会话发现的 Python 路径；安装包需有 reportlab。中文字体默认检查 Windows 宋体，可用 `--font /path/to/CJK.ttf` 指定可嵌入字体。生成后按 PDF skill 用 Poppler 逐页渲染并目视检查。

输入 JSON：

```json
{
  "property": "待定房源",
  "date": "2026-09-08",
  "tier": "au-low",
  "configuration": "3房2卫；拟配置1张King、2张Queen",
  "assumptions": ["按空房完整配置估算，现场确认后扣除保留物品。"],
  "source_summary": "根据历史采购及当前核对资料估算。",
  "items": [
    {
      "category": "卧室家具",
      "name": "King床架",
      "quantity": 1,
      "unit": "张",
      "unit_price_aud": 309,
      "optional": false,
      "source_reference": "历史快照：采购商品4674；2026-09-08读取；已下单参考价",
      "note": "原木色，实际尺寸待确认"
    },
    {
      "category": "配送与安装",
      "name": "送货费用",
      "quantity": 1,
      "unit": "次",
      "unit_price_aud": null,
      "optional": false,
      "note": "地址确定后核价"
    }
  ],
  "exclusions": ["未包含装修工程和后续运营消耗。"]
}
```

以上是字段示例，不是默认户型或完整报价。不要直接给新房套用该示例。`items` 每行购买单位必须与单价一致；包价时 quantity 是包数，note 可说明总件数。不要再加入已经包含在行金额内的费用或合计行。

必需字段：property、date（ISO日期）、tier（三档代码之一）、configuration、items。每项 category/name/unit/quantity，quantity >=0；unit_price_aud 是有限非负数字或 null。脚本先将 AUD 单价按四舍五入归至分，再乘购买量，让印出的单价与小计一致。有价格的行需内部 `source_reference`；该字段不会打印，避免暴露历史房源。

可选项目设 `optional: true`，不进入必要采购合计。未知费用用 null，而不是0；只要必要项存在未知价，报告显示「已估项目合计」及缺项。零购买量表示本次无需采购，脚本忽略此行，不能用0掩盖缺失需求。

如果渠道为仓库，额外写 `supply_channel: "au-warehouse"`，并且 `warehouse_available: true` 与 `warehouse_price_confirmed: true`；它们必须来自本次库存与计价核实。未核实不得设为 true，改选其他渠道或将该费用留待核。

脚本会在 PDF 同目录保存同名 `.calculation.json` 作为内部核算结果；制作房东交付时先输出到 work/，检查后仅把 PDF 复制到 outputs/，核算文件留 work/。PDF 文本字段都面向房东，不填内部地址、纠错记录或供应商账号。
