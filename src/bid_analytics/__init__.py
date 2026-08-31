"""Reusable analytics for sealed-bid competitor analysis."""

from .cleaning import normalize_bidder_name, standardize_bidder_names, wide_bids_to_long
from .metrics import (
    add_target_margins,
    build_competitor_scorecard,
    summarize_segments,
)

__all__ = [
    "add_target_margins",
    "build_competitor_scorecard",
    "normalize_bidder_name",
    "standardize_bidder_names",
    "summarize_segments",
    "wide_bids_to_long",
]
