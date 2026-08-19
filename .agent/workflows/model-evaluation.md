# Agent Workflow: Model Evaluation

**Goal**: Execute comprehensive model evaluation, decision threshold analysis, and error audit on holdout test datasets.

---

## Preconditions
1. Serialized model artifact exists in `models/`.
2. Processed test set (`X_test`, `y_test`) exists in `data/processed/`.

---

## Execution Steps

1. **Load Artifact**:
   Load trained model and scaler from `models/`.
2. **Predict Probabilities**:
   Generate raw prediction probabilities $P(\text{Suspicious} \mid X)$ on `X_test`.
3. **Calculate 5-Metric Suite**:
   Invoke `calculate_metrics(y_true, y_pred, y_prob)` from `src/utils/metrics.py`.
4. **Decision Threshold Sweep**:
   Evaluate Precision and Recall across threshold values $t \in [0.10, 0.90]$ with step $0.05$. Select optimal operational threshold prioritizing Recall while controlling FP.
5. **Confusion Matrix Generation**:
   Generate confusion matrix array (TP, FP, TN, FN).
6. **Error Analysis**:
   Extract False Positives (legitimate links marked suspicious) and False Negatives (malicious links missed). Categorize root causes.
7. **Write Report**:
   Render complete markdown evaluation report to `reports/model_evaluation_report.md`.

---

## Mandatory Constraints (Never Do)
- **NEVER** evaluate using Accuracy alone.
- **NEVER** modify predictions or fabricate metric values.
- **NEVER** label predictions as "100% Safe".

---

## Output Artifacts
- `reports/model_evaluation_report.md`
- `reports/confusion_matrix.png`
- `reports/roc_curve.png`
