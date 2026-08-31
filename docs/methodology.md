# Methodology

## Unit of analysis

The analytical table uses one row per bidder per project. This long format makes competitor overlap, head-to-head wins, bid margins, and filtered segment summaries explicit and testable.

## Entity standardization

Bidder names are normalized by converting text to uppercase, removing punctuation, and collapsing whitespace. Any remaining entity aliases must be reviewed and supplied through an explicit mapping; the workflow does not perform opaque fuzzy matching.

## Competitor metrics

For a focal bidder and competitor `c`:

```text
CoBid Projects(c) = distinct focal projects containing competitor c
Overlap(c) = CoBid Projects(c) / total focal projects
Win Pressure Index(c) = competitor wins on shared projects / CoBid Projects(c)
Impact Score(c) = Overlap(c) × Win Pressure Index(c)
```

Impact Score balances exposure and head-to-head strength. A competitor that appears often but rarely wins is different from a competitor that appears less often and wins consistently.

## Relative bid margins

For focal wins:

```text
Win Margin = (second-lowest bid - focal bid) / focal bid
```

For focal losses:

```text
Loss Margin = (focal bid - winning bid) / winning bid
```

Relative margins are comparable across differently sized projects and are easier to interpret than absolute currency differences alone.

## Segmentation

The project-level margin table can be grouped by region, season, project type, project size, or another authorized field. Each segment reports project count, wins, win rate, and median relative margin.

## Interpretation guardrails

- Impact Score is descriptive; it does not establish that a competitor caused a loss.
- Sparse segments should not drive strategy without reviewing sample size.
- Bid differences can reflect scope, timing, risk, or material assumptions not represented in the analytical table.
- Results should support commercial judgment, not replace it.
