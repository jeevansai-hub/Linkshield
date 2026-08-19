# Machine Learning Engineering Guide — LinkSentinel

> **Document Scope**: Feature extraction pipeline, baseline model selection, ensemble training, hyperparameter optimization, reproducibility, model persistence, and real-time inference latency constraints.

---

## 1. Machine Learning Philosophy

LinkSentinel adheres to the following core ML principles:

1. **Occam's Razor**: Start with simple, explainable linear models (Logistic Regression). Advance to non-linear tree ensembles (Random Forest, XGBoost, LightGBM) ONLY when empirical metrics show significant improvement.
2. **Reproducibility First**: Random seed `42` MUST be hardcoded across all ML pipelines.
3. **Inference Latency Constraint**: Real-time evaluation requires single-URL feature extraction + model prediction to complete in `<50ms`.
4. **Mandatory 5-Metric Logging**: Every experiment MUST report Accuracy, Precision, Recall, F1-Score, and ROC-AUC.

---

## 2. Feature Extraction Architecture

Static feature extraction is implemented in `src/features/extract_features.py`.

```python
class URLLexicalFeatureExtractor:
    """Extracts numerical feature vectors from static raw URL strings."""
    def extract(self, url: str) -> dict[str, float | int]:
        ...
```

Feature groups:
- **Lexical Metrics**: Length of URL, domain, path, query parameters.
- **Character Counts**: Dots, hyphens, underscores, slashes, digits, `@` symbols.
- **Structural Properties**: IP address host check, HTTPS scheme check, URL shortener detection.
- **Keyword Features**: Suspicious term matching (e.g. `login`, `bank`, `update`, `secure`).

---

## 3. Preprocessing & Leakage Prevention

To prevent data leakage:

```python
from sklearn.preprocessing import StandardScaler

# 1. Fit scaler ONLY on training data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# 2. Transform validation and test sets using fitted scaler
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)
```

Never call `fit` or `fit_transform` on combined datasets or test holdouts.

---

## 4. Model Training Progression

### Stage 1: Logistic Regression Baseline
- **Model**: `sklearn.linear_model.LogisticRegression(C=1.0, max_iter=1000, random_state=42)`
- **Purpose**: Fast baseline establishing lower-bound benchmark for all 5 metrics.

### Stage 2: Random Forest Classifier
- **Model**: `sklearn.ensemble.RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)`
- **Purpose**: Non-linear feature interaction capture without complex tuning.

### Stage 3: Gradient Boosted Trees (XGBoost / LightGBM)
- **Model**: `xgboost.XGBClassifier(n_estimators=200, learning_rate=0.05, max_depth=6, random_state=42)`
- **Purpose**: Maximum predictive performance, optimizing ROC-AUC and Recall.

---

## 5. Model Serialization & Artifact Storage

Trained pipeline artifacts are saved to `models/` using `joblib`:

```python
import joblib

artifact = {
    "model": trained_model,
    "scaler": fitted_scaler,
    "feature_names": feature_names,
    "version": "1.0.0",
    "metrics": evaluation_metrics_dict
}

joblib.dump(artifact, "models/linksentinel_xgboost_v1.0.0.joblib")
```

---

## 6. Real-Time Inference Benchmark Protocol

Inference speed is verified using benchmark scripts in `tests/`:

```python
import time

start_time = time.perf_counter()
features = extractor.extract(url)
X = scaler.transform([list(features.values())])
prob = model.predict_proba(X)[0][1]
elapsed_ms = (time.perf_counter() - start_time) * 1000.0

assert elapsed_ms < 50.0, f"Inference latency exceeded limit: {elapsed_ms:.2f} ms"
```
