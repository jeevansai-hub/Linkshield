# Agent Workflow: Model Training

**Goal**: Train baseline and ensemble machine learning models on extracted URL feature matrices.

---

## Preconditions
1. Processed feature matrices (`X_train`, `y_train`, `X_test`, `y_test`) exist in `data/processed/`.
2. Random seed is set to `42`.

---

## Execution Steps

1. **Stage 1 — Baseline Model**:
   Train `LogisticRegression(C=1.0, max_iter=1000, random_state=42)`. Log metrics.
2. **Stage 2 — Ensemble Models**:
   Train `RandomForestClassifier(n_estimators=100, random_state=42)` and `XGBClassifier(random_state=42)`.
3. **Hyperparameter Tuning**:
   Tune depth and learning rates using `X_val` validation set.
4. **Evaluate Metrics**:
   Compute all 5 required metrics (Accuracy, Precision, Recall, F1-Score, ROC-AUC) using `src/utils/metrics.py`.
5. **Serialize Artifact**:
   Save trained model and feature list to `models/linksentinel_model_latest.joblib`.

---

## Mandatory Constraints (Never Do)
- **NEVER** train on test holdout data.
- **NEVER** omit any of the 5 mandatory evaluation metrics.
- **NEVER** invent or fabricate performance numbers in training logs.

---

## Output Artifacts
- `models/linksentinel_model_v1.joblib`
- `reports/training_summary.md`
