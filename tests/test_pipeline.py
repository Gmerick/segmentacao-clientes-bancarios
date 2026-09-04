import unittest

import pandas as pd

from src.config import N_CUSTOMERS, N_MONTHS, SELECTED_K
from src.features import build_customer_features
from src.generate_data import generate_customers, generate_monthly_activity
from src.segmentation import build_segment_profiles, segment_customers


class CustomerSegmentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.customers = generate_customers(n_customers=600)
        cls.activity = generate_monthly_activity(cls.customers, months=N_MONTHS)
        cls.features = build_customer_features(cls.customers, cls.activity)
        cls.scored, cls.evaluation, cls.metrics = segment_customers(cls.features, save_model=False)
        cls.profiles = build_segment_profiles(cls.scored)

    def test_full_generator_size(self):
        sample = generate_customers(n_customers=N_CUSTOMERS)
        self.assertEqual(len(sample), N_CUSTOMERS)
        self.assertTrue(sample["customer_id"].is_unique)

    def test_monthly_activity_integrity(self):
        self.assertEqual(len(self.activity), 600 * N_MONTHS)
        self.assertTrue((self.activity["total_inflow"] >= 0).all())

    def test_one_feature_row_per_customer(self):
        self.assertEqual(len(self.features), 600)
        self.assertTrue(self.features["customer_id"].is_unique)

    def test_five_business_segments(self):
        self.assertEqual(self.scored["segment"].nunique(), SELECTED_K)
        self.assertEqual(len(self.profiles), SELECTED_K)

    def test_model_selection_range(self):
        self.assertEqual(self.evaluation["k"].tolist(), list(range(2, 9)))
        self.assertEqual(int(self.evaluation["selected"].sum()), 1)

    def test_output_has_no_missing_segments(self):
        self.assertFalse(self.scored["segment"].isna().any())
        self.assertTrue(pd.api.types.is_numeric_dtype(self.scored["product_count"]))


if __name__ == "__main__":
    unittest.main()

