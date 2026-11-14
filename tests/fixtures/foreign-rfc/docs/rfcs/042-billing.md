# RFC 042: Billing events

## Summary

Emit one billing event per invoice state change so finance can rebuild a ledger.

## Proposal

- `invoice.created`, `invoice.paid` and `invoice.voided` go to the `billing` topic.
- Each event carries the invoice ID, the amount in cents and the time of the change.

## Open questions

- How long does the topic keep events?
