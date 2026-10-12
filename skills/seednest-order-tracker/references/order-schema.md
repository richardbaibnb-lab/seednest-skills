# Order tracking schema

Use one record per retailer order line or shipment line. Preserve platform-specific identifiers privately; mask them in user-facing summaries.

Required fields:

| Field | Meaning |
|---|---|
| platform | Amazon, IKEA, Kmart, Temu, 1688, Taobao, or another retailer |
| order_id | Stable retailer order identifier |
| line_id | Stable line or shipment identifier when available |
| property | Linked Seednest property record |
| product | Concise product name |
| quantity_ordered | Quantity purchased |
| quantity_delivered | Quantity confirmed delivered |
| normalized_status | One allowed normalized status |
| retailer_status | Original retailer wording |
| estimated_delivery | Current estimated date or range |
| actual_delivery | Confirmed delivery date when available |
| exception | Delay, cancellation, damage, refund, split shipment, mismatch, or blank |
| source_checked_at | Timestamp of the latest authoritative check |

Optional fields include tracking number, carrier, amount, currency, purchase-row link, delivery evidence, and notes. Do not require cost or personal delivery details when they are unnecessary for fulfillment monitoring.

Deduplicate by `platform + order_id + line_id`. When no line identifier exists, use a stable product/shipment discriminator and flag ambiguity rather than silently merging lines.
