import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bid_analytics.metrics import (
    add_target_margins,
    build_competitor_scorecard,
    summarize_segments,
)


class MetricsTests(unittest.TestCase):
    def setUp(self):
        self.bids = pd.DataFrame(
            [
                {"project_id": 1, "bidder": "Focal Co", "bid_amount": 100, "won": True, "region": "North"},
                {"project_id": 1, "bidder": "Alpha", "bid_amount": 108, "won": False, "region": "North"},
                {"project_id": 1, "bidder": "Beta", "bid_amount": 112, "won": False, "region": "North"},
                {"project_id": 2, "bidder": "Focal Co", "bid_amount": 220, "won": False, "region": "North"},
                {"project_id": 2, "bidder": "Alpha", "bid_amount": 200, "won": True, "region": "North"},
                {"project_id": 3, "bidder": "Focal Co", "bid_amount": 150, "won": False, "region": "South"},
                {"project_id": 3, "bidder": "Beta", "bid_amount": 140, "won": True, "region": "South"},
            ]
        )

    def test_competitor_scorecard(self):
        scorecard = build_competitor_scorecard(self.bids, "Focal Co")
        alpha = scorecard.set_index("bidder").loc["ALPHA"]
        beta = scorecard.set_index("bidder").loc["BETA"]

        self.assertEqual(alpha["co_bid_projects"], 2)
        self.assertEqual(alpha["competitor_wins"], 1)
        self.assertAlmostEqual(alpha["overlap"], 2 / 3)
        self.assertAlmostEqual(alpha["win_pressure_index"], 1 / 2)
        self.assertAlmostEqual(alpha["impact_score"], 1 / 3)
        self.assertAlmostEqual(beta["impact_score"], 1 / 3)
        self.assertEqual(alpha["threat_rank"], 1)

    def test_target_margins_and_segment_summary(self):
        margins = add_target_margins(
            self.bids,
            "Focal Co",
            segment_columns=["region"],
        )
        by_project = margins.set_index("project_id")

        self.assertAlmostEqual(by_project.loc[1, "relative_margin"], 0.08)
        self.assertAlmostEqual(by_project.loc[2, "relative_margin"], 0.10)
        self.assertAlmostEqual(by_project.loc[3, "relative_margin"], 10 / 140)

        summary = summarize_segments(margins, ["region"]).set_index("region")
        self.assertEqual(summary.loc["North", "projects"], 2)
        self.assertAlmostEqual(summary.loc["North", "win_rate"], 0.5)
        self.assertAlmostEqual(summary.loc["South", "win_rate"], 0.0)

    def test_target_must_exist(self):
        with self.assertRaisesRegex(ValueError, "does not appear"):
            build_competitor_scorecard(self.bids, "Missing Co")


if __name__ == "__main__":
    unittest.main()
