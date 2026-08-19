"""Mandatory 5-Metric Evaluation Engine for LinkSentinel.

Calculates Accuracy, Precision, Recall, F1-Score, and ROC-AUC.
"""

from typing import Dict, Any, Optional
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)


def calculate_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: Optional[np.ndarray] = None
) -> Dict[str, Any]:
    """Computes the five mandatory LinkSentinel evaluation metrics.

    Args:
        y_true: Ground truth binary labels (0 = Safe-Looking, 1 = Suspicious).
        y_pred: Predicted binary labels.
        y_prob: Optional raw prediction probabilities for class 1 (Suspicious).

    Returns:
        Dictionary containing all 5 evaluation metrics, confusion matrix, and sample counts.
    """
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    roc_auc: Optional[float] = None
    if y_prob is not None:
        try:
            roc_auc = float(roc_auc_score(y_true, y_prob))
        except ValueError:
            roc_auc = 0.5  # Fallback for single-class arrays in synthetic tests

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

    metrics: Dict[str, Any] = {
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
        "roc_auc": round(float(roc_auc), 4) if roc_auc is not None else None,
        "confusion_matrix": {
            "true_negatives": int(tn),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_positives": int(tp)
        },
        "total_samples": len(y_true)
    }

    return metrics
