"""Command-line workflow for an authorized private bid-level file."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .metrics import add_target_margins, build_competitor_scorecard


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--target-bidder", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bids = pd.read_csv(args.input)
    scorecard = build_competitor_scorecard(bids, args.target_bidder)
    margins = add_target_margins(bids, args.target_bidder)

    args.output.mkdir(parents=True, exist_ok=True)
    scorecard.to_csv(args.output / "competitor_scorecard.csv", index=False)
    margins.to_csv(args.output / "target_bid_margins.csv", index=False)


if __name__ == "__main__":
    main()
