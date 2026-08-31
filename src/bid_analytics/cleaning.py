"""Client-neutral cleaning utilities for bidder-level records."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping, Sequence
from typing import Any

import pandas as pd


def normalize_bidder_name(value: Any) -> str | pd._libs.missing.NAType:
    """Return an uppercase, punctuation-free bidder identifier.

    The function intentionally avoids fuzzy matching. Entity aliases should be
    reviewed by a person and supplied explicitly to ``standardize_bidder_names``.
    """

    if pd.isna(value):
        return pd.NA

    text = unicodedata.normalize("NFKD", str(value))
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.upper().strip()
    text = re.sub(r"[^A-Z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text or pd.NA


def standardize_bidder_names(
    values: pd.Series,
    aliases: Mapping[str, str] | None = None,
) -> pd.Series:
    """Normalize a bidder series and apply a reviewed alias dictionary."""

    normalized = values.map(normalize_bidder_name).astype("string")
    if not aliases:
        return normalized

    normalized_aliases = {
        normalize_bidder_name(source): normalize_bidder_name(destination)
        for source, destination in aliases.items()
    }
    return normalized.replace(normalized_aliases)


def wide_bids_to_long(
    frame: pd.DataFrame,
    project_columns: Sequence[str],
    bidder_columns: Sequence[str],
    bid_amount_columns: Sequence[str],
    aliases: Mapping[str, str] | None = None,
) -> pd.DataFrame:
    """Reshape paired bidder and amount columns into one row per bid."""

    if len(bidder_columns) != len(bid_amount_columns):
        raise ValueError("bidder_columns and bid_amount_columns must have equal length")

    required = set(project_columns) | set(bidder_columns) | set(bid_amount_columns)
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"missing columns: {missing}")

    parts: list[pd.DataFrame] = []
    for position, (bidder_column, amount_column) in enumerate(
        zip(bidder_columns, bid_amount_columns, strict=True),
        start=1,
    ):
        part = frame.loc[:, [*project_columns, bidder_column, amount_column]].copy()
        part = part.rename(
            columns={bidder_column: "bidder", amount_column: "bid_amount"}
        )
        part["bid_position"] = position
        parts.append(part)

    long_frame = pd.concat(parts, ignore_index=True)
    long_frame = long_frame.loc[long_frame["bidder"].notna()].copy()
    long_frame["bidder"] = standardize_bidder_names(long_frame["bidder"], aliases)
    long_frame["bid_amount"] = pd.to_numeric(long_frame["bid_amount"], errors="coerce")
    return long_frame.reset_index(drop=True)
