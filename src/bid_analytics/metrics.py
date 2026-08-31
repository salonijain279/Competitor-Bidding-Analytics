"""Interpretable competitor, margin, and segment metrics."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd

from .cleaning import normalize_bidder_name

REQUIRED_BID_COLUMNS = {"project_id", "bidder", "bid_amount", "won"}


def _validated_bid_table(frame: pd.DataFrame) -> pd.DataFrame:
    missing = sorted(REQUIRED_BID_COLUMNS.difference(frame.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    result = frame.copy()
    result["bidder"] = result["bidder"].map(normalize_bidder_name).astype("string")
    result["bid_amount"] = pd.to_numeric(result["bid_amount"], errors="coerce")

    won_map = {
        True: True,
        False: False,
        1: True,
        0: False,
        "1": True,
        "0": False,
        "TRUE": True,
        "FALSE": False,
        "YES": True,
        "NO": False,
        "Y": True,
        "N": False,
    }
    result["won"] = result["won"].map(
        lambda value: won_map.get(value, won_map.get(str(value).upper(), np.nan))
    )

    if result["project_id"].isna().any() or result["bidder"].isna().any():
        raise ValueError("project_id and bidder cannot contain missing values")
    if result["bid_amount"].isna().any() or (result["bid_amount"] <= 0).any():
        raise ValueError("bid_amount must contain positive numeric values")
    if result["won"].isna().any():
        raise ValueError("won must contain boolean-like values")
    if result.duplicated(["project_id", "bidder"]).any():
        raise ValueError("each bidder must appear at most once per project")

    result["won"] = result["won"].astype(bool)
    return result


def build_competitor_scorecard(
    frame: pd.DataFrame,
    target_bidder: str,
) -> pd.DataFrame:
    """Calculate overlap, win pressure, impact score, and threat rank."""

    bids = _validated_bid_table(frame)
    target = normalize_bidder_name(target_bidder)
    target_projects = bids.loc[bids["bidder"].eq(target), "project_id"].unique()
    if len(target_projects) == 0:
        raise ValueError("target_bidder does not appear in the bid table")

    shared = bids.loc[
        bids["project_id"].isin(target_projects) & bids["bidder"].ne(target)
    ].copy()
    if shared.empty:
        return pd.DataFrame(
            columns=[
                "bidder",
                "co_bid_projects",
                "competitor_wins",
                "overlap",
                "win_pressure_index",
                "impact_score",
                "threat_rank",
            ]
        )

    scorecard = (
        shared.groupby("bidder", as_index=False)
        .agg(
            co_bid_projects=("project_id", "nunique"),
            competitor_wins=("won", "sum"),
        )
        .sort_values("bidder")
    )
    scorecard["overlap"] = scorecard["co_bid_projects"] / len(target_projects)
    scorecard["win_pressure_index"] = (
        scorecard["competitor_wins"] / scorecard["co_bid_projects"]
    )
    scorecard["impact_score"] = (
        scorecard["overlap"] * scorecard["win_pressure_index"]
    )
    scorecard["threat_rank"] = (
        scorecard["impact_score"].rank(method="min", ascending=False).astype(int)
    )
    return scorecard.sort_values(
        ["threat_rank", "co_bid_projects", "bidder"],
        ascending=[True, False, True],
        ignore_index=True,
    )


def add_target_margins(
    frame: pd.DataFrame,
    target_bidder: str,
    segment_columns: Sequence[str] = (),
) -> pd.DataFrame:
    """Create one focal-company margin record per participated project."""

    bids = _validated_bid_table(frame)
    missing_segments = sorted(set(segment_columns).difference(bids.columns))
    if missing_segments:
        raise ValueError(f"missing segment columns: {missing_segments}")

    target = normalize_bidder_name(target_bidder)
    target_projects = bids.loc[bids["bidder"].eq(target), "project_id"].unique()
    records: list[dict[str, object]] = []

    for project_id in target_projects:
        project = bids.loc[bids["project_id"].eq(project_id)].copy()
        target_row = project.loc[project["bidder"].eq(target)].iloc[0]
        sorted_amounts = project["bid_amount"].sort_values(ignore_index=True)
        winning_rows = project.loc[project["won"]]
        winning_bid = (
            float(winning_rows["bid_amount"].min())
            if not winning_rows.empty
            else float(sorted_amounts.iloc[0])
        )
        second_lowest_bid = (
            float(sorted_amounts.iloc[1]) if len(sorted_amounts) > 1 else np.nan
        )
        target_bid = float(target_row["bid_amount"])
        target_won = bool(target_row["won"])

        if target_won and not np.isnan(second_lowest_bid):
            margin_type = "win"
            relative_margin = (second_lowest_bid - target_bid) / target_bid
        elif not target_won:
            margin_type = "loss"
            relative_margin = (target_bid - winning_bid) / winning_bid
        else:
            margin_type = "unavailable"
            relative_margin = np.nan

        record: dict[str, object] = {
            "project_id": project_id,
            "target_bid": target_bid,
            "winning_bid": winning_bid,
            "second_lowest_bid": second_lowest_bid,
            "won": target_won,
            "margin_type": margin_type,
            "relative_margin": relative_margin,
        }
        for column in segment_columns:
            record[column] = target_row[column]
        records.append(record)

    return pd.DataFrame.from_records(records)


def summarize_segments(
    project_metrics: pd.DataFrame,
    dimensions: Sequence[str],
) -> pd.DataFrame:
    """Summarize project participation, wins, win rate, and median margin."""

    required = {"project_id", "won", "relative_margin", *dimensions}
    missing = sorted(required.difference(project_metrics.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    if not dimensions:
        raise ValueError("at least one segment dimension is required")

    summary = (
        project_metrics.groupby(list(dimensions), dropna=False, as_index=False)
        .agg(
            projects=("project_id", "nunique"),
            wins=("won", "sum"),
            win_rate=("won", "mean"),
            median_relative_margin=("relative_margin", "median"),
        )
        .sort_values(["projects", *dimensions], ascending=[False, *([True] * len(dimensions))])
        .reset_index(drop=True)
    )
    return summary
