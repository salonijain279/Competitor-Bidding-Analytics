import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bid_analytics.cleaning import (
    normalize_bidder_name,
    standardize_bidder_names,
    wide_bids_to_long,
)


class CleaningTests(unittest.TestCase):
    def test_normalize_and_reviewed_aliases(self):
        values = pd.Series(["  Alpha & Co., Inc. ", "ALPHA COMPANY", None])
        standardized = standardize_bidder_names(
            values,
            aliases={"ALPHA & CO INC": "ALPHA COMPANY"},
        )

        self.assertEqual(normalize_bidder_name(values.iloc[0]), "ALPHA CO INC")
        self.assertEqual(standardized.iloc[0], "ALPHA COMPANY")
        self.assertEqual(standardized.iloc[1], "ALPHA COMPANY")
        self.assertTrue(pd.isna(standardized.iloc[2]))

    def test_wide_bids_to_long(self):
        wide = pd.DataFrame(
            {
                "project_id": [101, 102],
                "region": ["North", "South"],
                "bidder_1": ["Focal Co.", "Focal Co."],
                "amount_1": [100.0, 205.0],
                "bidder_2": ["Beta LLC", None],
                "amount_2": [110.0, None],
            }
        )

        result = wide_bids_to_long(
            wide,
            project_columns=["project_id", "region"],
            bidder_columns=["bidder_1", "bidder_2"],
            bid_amount_columns=["amount_1", "amount_2"],
        )

        self.assertEqual(result.shape[0], 3)
        self.assertEqual(result["bidder"].tolist(), ["FOCAL CO", "FOCAL CO", "BETA LLC"])
        self.assertEqual(result["bid_position"].tolist(), [1, 1, 2])

    def test_wide_bids_requires_paired_columns(self):
        with self.assertRaisesRegex(ValueError, "equal length"):
            wide_bids_to_long(
                pd.DataFrame(),
                project_columns=[],
                bidder_columns=["bidder_1"],
                bid_amount_columns=[],
            )


if __name__ == "__main__":
    unittest.main()
