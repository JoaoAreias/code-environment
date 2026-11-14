# LESSONS - auto-maintained by scripts/lessons.py

> Machine-owned. Do NOT hand-edit. Changes are overwritten on the next `lessons.py` write.
> Canonical state lives in `.specs/lessons.json`. Edit lessons only via the script.
> promote_threshold=2 distinct features · window_days=45 · quarantine_threshold=2

## Confirmed (author lessons load at Specify/Design; reviewer lessons load at each review)

Corroborated across multiple features. Safe to apply as guidance.

_none_

## Candidates (under observation - do NOT load as guidance yet)

Seen once or not yet corroborated. Tracked, not trusted.

### L-001 - Name shared per-feature files under .specs so two branches cannot pick the same name silently
- audience: author · signal: `spec_review_finding` · recurrence: 1 feature(s) · scope: `.specs` · harmful: 0
- features: integrate-skills
- evidence: .specs/features/integrate-skills/spec-review-1.md SR1-F3 (.specs) (+1 more)
- last seen: 2026-11-14T17:26:43Z

### L-002 - Make every write to an external tracker resumable and never create the same item twice
- audience: author · signal: `spec_review_finding` · recurrence: 1 feature(s) · scope: `trackers` · harmful: 0
- features: integrate-skills
- evidence: .specs/features/integrate-skills/spec-review-1.md SR1-F4 (trackers)
- last seen: 2026-11-14T14:16:40Z

### L-003 - When a validator makes a field required for every task, cover the fix tasks that reviews and the Verifier append
- audience: author · signal: `spec_review_finding` · recurrence: 1 feature(s) · scope: `scripts` · harmful: 0
- features: integrate-skills
- evidence: .specs/features/integrate-skills/spec-review-1.md SR1-F6 (scripts)
- last seen: 2026-11-14T14:16:40Z

### L-004 - Validators read markdown table cells by header name, never by position
- audience: author · signal: `spec_review_finding` · recurrence: 1 feature(s) · scope: `scripts` · harmful: 0
- features: integrate-skills
- evidence: .specs/features/integrate-skills/spec-review-1.md SR1-F8 (scripts) (+1 more)
- last seen: 2026-11-14T17:26:43Z

### L-005 - Do not ask for a graphify stub in tests; this repo requires the real graphify on purpose
- audience: reviewer · signal: `review_rejection` · recurrence: 1 feature(s) · scope: `tests` · harmful: 0
- features: integrate-skills
- evidence: .specs/features/integrate-skills/spec-review-1.md SR1-F9 (tests)
- last seen: 2026-11-14T14:16:40Z

### L-006 - Delete from a shared directory only what this repo put there, never by name alone
- audience: author · signal: `spec_review_finding` · recurrence: 1 feature(s) · scope: `install` · harmful: 0
- features: integrate-skills
- evidence: .specs/features/integrate-skills/spec-review-2.md SR2-F7 (install)
- last seen: 2026-11-14T17:26:43Z

### L-007 - Keep fixture specs as md files under tests/fixtures, never as text inside a test function
- audience: author · signal: `spec_review_finding` · recurrence: 1 feature(s) · scope: `tests` · harmful: 0
- features: integrate-skills
- evidence: .specs/features/integrate-skills/spec-review-2.md SR2-F3 (tests)
- last seen: 2026-11-14T17:26:43Z

## Quarantined (failed when applied - ignore)

A confirmed lesson that recurred alongside failure. Kept for the maintainer to review.

_none_
