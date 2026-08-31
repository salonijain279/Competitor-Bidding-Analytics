# Private input data contract

The public repository does not include a dataset. The analysis functions expect an authorized, private bid-level table with one row per bidder per project.

## Required fields

| Field | Type | Meaning |
|---|---|---|
| `project_id` | string or integer | Stable project identifier |
| `bidder` | string | Bidder name or reviewed standardized identifier |
| `bid_amount` | positive numeric | Submitted bid value |
| `won` | boolean-like | Whether the bidder won the project |

## Optional analytical fields

- `date`
- `season`
- `region`
- `project_type`
- `project_size`
- other approved segmentation fields

## Validation rules

- A bidder may appear at most once per project.
- Bid amounts must be positive and numeric.
- Project and bidder identifiers cannot be missing.
- The focal bidder must appear in at least one project.
- Client and competitor names should be anonymized before any portfolio use.
