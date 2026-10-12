---
name: setup-order-updater
description: Match a property's setup screenshots to Feishu purchase rows, correct ordered statuses, and add screenshot items missing from the purchase table using an official 1688 order export. Use for Seednest property setup-order updates; do not treat every property or 1688 row as a screenshot match.
---

# Setup Order Updater

Update a property's setup purchases from evidence, with the screenshot folder as the inclusion authority.

## Required evidence

- Use only PNG/JPG screenshots inside the exact property `setup 发票` folder unless the user names another folder. Do not include PDFs or neighboring folders.
- Inventory the screenshot filenames first and record the count.
- Filter Feishu by the existing linked value in `已下单房源`; verify the visible property label and row count before changing data.
- Narrow candidate rows by platform/link only after the property filter is verified.

## Matching gate

Never mark all property rows or all `detail.1688.com` rows as ordered.

For every screenshot, match the product title, selected variant/specification, quantity, and price against the purchase row. A broad category match is insufficient. Treat similarly named but materially different products as unmatched—for example, a real coffee maker is not a wooden pretend-play coffee machine.

Before writing, produce both sets:

1. screenshot items matched to existing purchase rows;
2. screenshot items missing from the purchase table, plus purchase rows that have no screenshot.

When one screenshot contains several SKUs or variants, represent each SKU as a separate purchase row. Multiple screenshots of the same offer do not automatically require duplicate rows; reconcile quantity and variant first.

## Status updates

- Change only verified matches to `已下单`.
- Restore or retain nonmatches as `未开始` unless an existing exception such as cancellation, refund, return, damage, out-of-stock, or an authorized substitute applies.
- Preserve user-entered exceptions and unrelated fields.
- If a write is authorized, update the smallest verified record set and inspect the saved cell value rather than relying on a success banner.

## Missing products

When screenshot items are absent from Feishu, request or use the user's official 1688 order-export workbook. Read [references/1688-export.md](references/1688-export.md) before adding records.

Add one row per distinct SKU/variant. Populate, when supported by the source and existing table conventions:

- English and Chinese item names;
- purchase quantity and single-package quantity;
- RMB unit price and AUD unit price only when it can be derived reliably;
- `购买进度 = 已下单`;
- canonical 1688 product link;
- the exact linked property record;
- category/platform fields when confidently known.

Do not invent product links, prices, exchange rates, quantities, or variants. If the order export does not contain an Offer ID, stop and request a reliable link.

## Verification

After changes, independently verify:

- total property/platform candidate rows;
- count of `已下单`, `未开始`, and retained exceptions;
- every newly added row has the intended linked property, status, quantity, and a nonblank canonical link;
- the matched and unmatched lists reconcile with the screenshot inventory.

Report actual counts and name any unresolved screenshot or purchase-row mismatch. Do not claim completion until the post-write distribution and new links are visible.
