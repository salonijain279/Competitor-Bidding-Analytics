# Competitor Bidding Analytics

An anonymized, analysis-only framework for understanding head-to-head competition in sealed-bid markets.

## Project overview

This repository is a portfolio-safe reconstruction of a team-based MSBA live case. The original engagement examined bidding behavior for a regional construction company and translated bid-level records into competitor, margin, regional, and seasonal decision support.

The source engagement was governed by a confidentiality agreement. For that reason, this repository contains **no client data, company or competitor names, exact results, dashboard packages, screenshots, reports, or presentation files**. It focuses on the reusable analytical design and code.

## Business questions

- Which competitors appear most often in the same bidding opportunities?
- Which competitors win most frequently in head-to-head situations?
- Which competitors combine high overlap with high win pressure?
- How close are wins and losses relative to the winning bid?
- How does performance change by region, season, project type, and project size?

## Analysis projects

### 1. Bid data preparation

Standardize bidder names, reshape wide bidder columns into one-row-per-bid format, clean numeric bid values, and create a consistent analytical contract.

### 2. Competitor threat scorecard

Rank competitors using three interpretable measures:

- **Overlap:** share of focal-company projects on which a competitor also bids
- **Win Pressure Index:** competitor wins divided by shared bidding opportunities
- **Impact Score:** overlap multiplied by Win Pressure Index

This distinguishes frequent competitors from competitors that are both frequent and consistently successful.

### 3. Win and loss margin analysis

Measure the relative distance between the focal bid and the relevant benchmark:

- **Win margin:** `(second-lowest bid - focal bid) / focal bid`
- **Loss margin:** `(focal bid - winning bid) / winning bid`

The result helps separate comfortable wins, close wins, recoverable losses, and structurally uncompetitive losses.

### 4. Segment and season decision support

Summarize win rate and bid margins across business dimensions such as region, season, project type, and project size. These outputs are designed for downstream dashboard filters and bid-strategy conversations.

## What the framework can reveal

- Competitor threat is not determined by frequency alone.
- Repeated close losses may indicate recoverable pricing or selection opportunities.
- Competitive pressure can vary meaningfully across region, season, and project segment.
- A small set of explainable metrics can make bid-review conversations more consistent.

These are analytical interpretations, not disclosures of the confidential client results.

## Repository structure

```text
src/bid_analytics/
  cleaning.py        # bidder normalization and wide-to-long reshaping
  metrics.py         # threat, margin, and segment metrics
  pipeline.py        # command-line analysis workflow
notebooks/
  01_analysis_workflow.ipynb
docs/
  data_contract.md
  methodology.md
tests/
  test_cleaning.py
  test_metrics.py
```

## Run the analysis

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

To run the command-line workflow against an authorized private file:

```bash
python -m bid_analytics.pipeline \
  --input /path/to/private/bids.csv \
  --target-bidder "FOCAL COMPANY" \
  --output /path/to/private/output
```

The input file is expected to follow the schema in [`docs/data_contract.md`](docs/data_contract.md). Local data and generated outputs are ignored by Git.

## Tools and methods

Python · pandas · data cleaning · entity standardization · wide-to-long reshaping · competitor benchmarking · margin analysis · segmentation · Tableau-ready output design

## Confidentiality boundary

The code is reusable and client-neutral. All examples in tests use invented identifiers and values. Nothing in this repository should be interpreted as an original client record or result.
