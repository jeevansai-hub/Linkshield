"""Unit tests for mandatory 5-metric evaluation utility."""

import unittest
import numpy as np
from src.utils.metrics import calculate_metrics


class TestMetrics(unittest.TestCase):

    def test_metrics_calculation_includes_all_five_metrics(self):
        y_true = np.array([0, 0, 1, 1, 0, 1, 0, 1])
        y_pred = np.array([0, 0, 1, 0, 0, 1, 1, 1])
        y_prob = np.array([0.1, 0.2, 0.8, 0.4, 0.3, 0.9, 0.6, 0.85])

        metrics = calculate_metrics(y_true, y_pred, y_prob)

        self.assertIn("accuracy", metrics)
        self.assertIn("precision", metrics)
        self.assertIn("recall", metrics)
        self.assertIn("f1_score", metrics)
        self.assertIn("roc_auc", metrics)

        self.assertTrue(0.0 <= metrics["accuracy"] <= 1.0)
        self.assertTrue(0.0 <= metrics["precision"] <= 1.0)
        self.assertTrue(0.0 <= metrics["recall"] <= 1.0)
        self.assertTrue(0.0 <= metrics["f1_score"] <= 1.0)
        self.assertTrue(0.0 <= metrics["roc_auc"] <= 1.0)

        self.assertIn("confusion_matrix", metrics)
        cm = metrics["confusion_matrix"]
        self.assertEqual(cm["true_positives"], 3)
        self.assertEqual(cm["false_negatives"], 1)


if __name__ == "__main__":
    unittest.main()

