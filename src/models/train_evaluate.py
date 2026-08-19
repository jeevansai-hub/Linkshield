"""Model Training and Pipeline Infrastructure for LinkSentinel.

Logistic Regression utilizes StandardScaler inside a Pipeline.
Random Forest operates directly on raw unscaled features.
Enforces seed 42 for 100% reproducibility.
"""

from typing import Tuple, Dict, Any, Optional
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from src.utils.metrics import calculate_metrics


class ModelPipeline:
    """Configurable model pipeline wrapper."""

    SUPPORTED_MODELS = ["logistic_regression", "random_forest"]

    def __init__(self, model_type: str = "logistic_regression", random_state: int = 42):
        if model_type not in self.SUPPORTED_MODELS:
            raise ValueError(f"Model type '{model_type}' not supported. Choose from {self.SUPPORTED_MODELS}")

        self.model_type = model_type
        self.random_state = random_state
        self.pipeline = self._initialize_pipeline()

    def _initialize_pipeline(self) -> Any:
        """Instantiates specified model with proper scaling pipeline."""
        if self.model_type == "logistic_regression":
            return Pipeline([
                ("scaler", StandardScaler()),
                ("classifier", LogisticRegression(C=1.0, max_iter=1000, random_state=self.random_state))
            ])
        elif self.model_type == "random_forest":
            return RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                random_state=self.random_state
            )

    def fit(self, X_train: np.ndarray, y_train: np.ndarray) -> "ModelPipeline":
        """Fits pipeline on training set."""
        self.pipeline.fit(X_train, y_train)
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predicts class probabilities."""
        if hasattr(self.pipeline, "predict_proba"):
            return self.pipeline.predict_proba(X)[:, 1]
        else:
            raise AttributeError("Pipeline does not support predict_proba.")

    def evaluate(self, X: np.ndarray, y: np.ndarray, threshold: float = 0.50) -> Dict[str, Any]:
        """Evaluates pipeline on specified dataset at given decision threshold.

        Args:
            X: Feature matrix.
            y: True binary labels.
            threshold: Decision threshold for class 1 (Suspicious).

        Returns:
            Dictionary containing the 5 mandatory evaluation metrics.
        """
        y_prob = self.predict_proba(X)
        y_pred = (y_prob >= threshold).astype(int)

        metrics = calculate_metrics(y, y_pred, y_prob)
        metrics["model_type"] = self.model_type
        metrics["decision_threshold"] = threshold

        return metrics
