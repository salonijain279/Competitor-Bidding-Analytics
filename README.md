# Competitor Bidding Analytics

I worked on this project to answer a practical question: **when a company loses a sealed bid, who is it really competing against—and how close was the loss?**

This began as a team live case during my MS in Business Analytics at the University of Minnesota. We worked with a regional road-construction company and analyzed its 2024–2025 bidding history. My work covered data cleaning, bidder-name standardization, analysis-ready table design, competitor metrics, bid-margin analysis, and dashboard-ready outputs.

The original engagement was confidential, so I have not published the client data, company names, exact findings, reports, or Tableau workbooks. Instead, I rebuilt the analytical logic as reusable Python code with invented test records.

## What I wanted to understand

I framed the analysis around five questions:

- Which competitors show up most often on the same projects?
- Which competitors win most often when both companies bid?
- Who combines frequent overlap with strong head-to-head performance?
- Were losses close enough to suggest a recoverable pricing opportunity?
- Did competitive pressure change by region, season, project type, or project size?

## What I worked on

### 1. Turning inconsistent bid files into an analytical table

The source files contained inconsistent bidder spellings, punctuation, spacing, and wide bidder columns. I standardized bidder names, created a reviewed alias layer, cleaned bid amounts, and reshaped the records into a long format with one bidder per project row.

That structure made the rest of the analysis much easier to audit: every competitor comparison and margin calculation could be traced back to a specific project and bid.

### 2. Measuring competitor pressure

Counting competitor appearances was not enough. A company could bid frequently without winning often, or appear less often and still be a serious threat. I used three interpretable metrics:

```text
Overlap = shared bidding projects / all focal-company projects

Win Pressure Index = competitor wins / shared bidding projects

Impact Score = Overlap × Win Pressure Index
```

Together, these metrics separate **frequency** from **head-to-head effectiveness**.

### 3. Measuring how close each result was

I calculated margins relative to the relevant benchmark instead of relying only on absolute dollar differences:

```text
Win Margin = (second-lowest bid - focal bid) / focal bid

Loss Margin = (focal bid - winning bid) / winning bid
```

This made projects of different sizes more comparable and helped distinguish a narrow loss from a structurally uncompetitive bid.

### 4. Preparing decision-ready segment views

I structured the outputs so performance could be compared across region, season, project type, and project size. The original team deliverable used these views in Tableau to support competitor review and bidding-strategy discussions.

## What I took away from the analysis

- The competitor seen most often is not automatically the most important competitor.
- Win rate becomes more useful when it is paired with overlap and sample size.
- Relative margins provide more context than a simple win/loss flag.
- Regional and seasonal cuts can expose patterns hidden by portfolio-wide averages.
- The most useful output is not a ranking by itself; it is a repeatable way to review where the company competes well and where a bid deserves a closer look.

These are analytical takeaways from the framework, not disclosures of the confidential client results.

## What is included here

```text
src/bid_analytics/
  cleaning.py        # bidder normalization and wide-to-long reshaping
  metrics.py         # competitor, margin, and segment metrics
  pipeline.py        # command-line workflow for an authorized private file
notebooks/
  01_analysis_workflow.ipynb
docs/
  data_contract.md
  methodology.md
tests/
  test_cleaning.py
  test_metrics.py
```

The public code includes:

- deterministic bidder-name normalization;
- explicit, human-reviewed alias mapping;
- competitor overlap and Win Pressure Index calculations;
- combined Impact Score and threat ranking;
- relative win/loss margin calculations;
- grouped win-rate and margin summaries;
- input validation and unit tests using invented companies and values.

## Running the code

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

To use the workflow with an authorized private dataset:

```bash
python -m bid_analytics.pipeline \
  --input /path/to/private/bids.csv \
  --target-bidder "FOCAL COMPANY" \
  --output /path/to/private/output
```

The expected schema is documented in [`docs/data_contract.md`](docs/data_contract.md), and the metric definitions and interpretation guardrails are in [`docs/methodology.md`](docs/methodology.md).

## Tools and skills

`Python` · `pandas` · data cleaning · entity standardization · wide-to-long reshaping · competitor benchmarking · margin analysis · segmentation · Tableau-ready metric design

## Confidentiality boundary

This repository contains only client-neutral code, documentation, and invented test records. The original data, identities, findings, dashboards, reports, and presentation materials remain private.
