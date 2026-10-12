---
name: seednest-order-tracker
description: Track Seednest setup-purchase orders across retailer accounts, match shipments to properties, normalize delivery states, identify exceptions, and prepare read-only status updates. Use for recurring Amazon or multi-platform delivery monitoring, historical setup-order audits, or property arrival summaries. Do not use to place, cancel, return, refund, or modify orders.
---

# Seednest Order Tracker

Monitor purchase fulfillment without changing retailer orders.

For screenshot-driven Feishu purchase-status updates, screenshot-to-row reconciliation, or adding missing 1688 products from an order export, use `setup-order-updater` instead.

## Operating boundary

- Treat retailer, carrier, email, and Feishu data as read-only unless the user separately authorizes an exact write.
- Never place, cancel, return, refund, reorder, change an address, contact a seller, or change payment details under this skill.
- Never request, read, store, or reproduce passwords, one-time codes, payment-card data, or full delivery addresses in reports. Let the user complete passwords, OTPs, and CAPTCHAs.
- Use existing signed-in browser sessions when available. A login session is not permission for an order-changing action.
- Prefer account order pages or carrier pages as delivery evidence. Treat email and screenshots as secondary evidence.
- Do not mark an order delivered solely because its estimated date passed.

## Workflow

1. Determine the monitoring scope: active setup properties by default; include historical properties only when the user asks for a backtest such as 4 Roseberry.
2. Read [references/order-schema.md](references/order-schema.md) before producing or syncing structured records.
3. For each applicable platform, read [references/platforms.md](references/platforms.md) and use the narrowest signed-in order-history or open-orders view.
4. Extract only the fields needed for monitoring. Normalize the retailer state to one of: `ordered`, `not_dispatched`, `dispatched`, `in_transit`, `out_for_delivery`, `delivered`, `delayed`, `cancelled`, `return_started`, `returned`, `refunded`, `unknown`.
5. Match an order to a property using, in priority order: an existing purchase-row link or order number; exact normalized delivery address; explicit property name/reference; then a human-confirmed mapping. Never guess when multiple properties match.
6. Compare with the prior snapshot. Report only new orders, meaningful status changes, overdue deliveries, cancellations, refunds, split shipments, address mismatches, or unmatched orders. A scheduled run with no changes should produce a compact `no changes` result.
7. Calculate property progress from line-item quantities where available. Keep `ordered`, `dispatched`, and `delivered` quantities separate; do not infer whole-order delivery from one package.
8. If a write to Feishu is requested, prepare the exact proposed changes and obtain confirmation immediately before transmitting order, address, recipient, cost, or tracking data. Preserve existing linked records and update by stable order/line identifier rather than inserting duplicates.

## Feishu accuracy gate

For property-scoped Feishu updates, treat linked-property filters as record references, not ordinary address text.

1. Select the existing value from the linked property field (for example `已下单房源`). Before writing, verify that the visible group/property label changed to the intended property and record the displayed row count. A search result click alone is not evidence that the filter changed.
2. Run a read-only preflight using the same linked value and compare its count with the visible filtered count. Stop on any mismatch; do not substitute a fuzzy address match for a linked-record write.
3. Apply changes only to the verified filtered record set. Preserve explicit refund, cancellation, return, out-of-stock, damage, or authorized offline-substitution exceptions unless the user explicitly resolves them.
4. Run an independent read-only post-write query using the same linked value. Reconcile `matched = completed + retained exceptions + other unresolved` and report the actual changed count.
5. Never report completion from an assistant/task success banner alone. Completion requires the post-write status distribution to confirm the intended values. If the write tool reports zero while the preflight found records, report a write failure and leave the task incomplete.

## Go-live signal

Order tracking supplies evidence to setup readiness; it does not approve a property by itself. Mark procurement ready only when all mandatory line items are delivered or an authorized person records an accepted substitute/waiver, and no blocking cancellation, refund, damage, or address mismatch remains.

## Reporting

Lead with exceptions and changed statuses. Group results by property, then platform. Avoid exposing full order numbers or addresses in ordinary summaries; use masked identifiers and property short names.

For a historical backtest, distinguish `operational result` from `record completeness`. Missing historical updates must not be presented as evidence that physical setup failed.
