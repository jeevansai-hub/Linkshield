# Evaluation Framework Guide — LinkSentinel

> **Document Scope**: Evaluation metrics, confusion matrix interpretation, threshold selection, and error analysis methodology for LinkSentinel (`LinkShield`).

---

## 1. The 5 Mandatory Evaluation Metrics

Every model evaluation in LinkSentinel MUST output and log the following five metrics:

```
┌────────────────────────────────────────────────────────┐
│               LinkSentinel 5-Metric Suite              │
├─────────────────┬──────────────────────────────────────┤
│ 1. Accuracy     │ (TP + TN) / (TP + TN + FP + FN)      │
│ 2. Precision    │ TP / (TP + FP)                       │
│ 3. Recall       │ TP / (TP + FN)                       │
│ 4. F1-Score     │ 2 * (Precision * Recall) / (P + R)   │
│ 5. ROC-AUC      │ Area under ROC Curve                 │
└─────────────────┴──────────────────────────────────────┘
```

---

## 2. Metric Justifications in Cyber Security Context

### Accuracy
- **Definition**: Proportion of all predictions that were correct.
- **Limitation**: In real-world web traffic where malicious URLs represent <5% of traffic, a naive model predicting all links as "safe" yields 95% accuracy while missing 100% of attacks. Therefore, Accuracy alone is INSUFFICIENT.

### Precision
- **Definition**: Proportion of predicted "Suspicious" links that were genuinely malicious.
- **Cybersecurity Role**: High precision minimizes false alarms (False Positives), preventing user fatigue and blocking legitimate user browsing.

### Recall (Sensitivity / Detection Rate)
- **Definition**: Proportion of actual malicious URLs successfully flagged.
- **Cybersecurity Role**: **CRITICAL METRIC**. High recall minimizes False Negatives (uncaught attacks). A false negative allows a phishing attack or malware infection to succeed.

### F1-Score
- **Definition**: Harmonic mean of Precision and Recall.
- **Cybersecurity Role**: Balances the operational tradeoff between flagging legitimate sites and catching malicious links.

### ROC-AUC
- **Definition**: Area under the Receiver Operating Characteristic curve (True Positive Rate vs False Positive Rate).
- **Cybersecurity Role**: Evaluates the model's intrinsic discrimination power across all possible decision thresholds, independent of class distribution.

---

## 3. Confusion Matrix Analysis

```text
                     Actual Safe (0)       Actual Suspicious (1)
Predicted Safe (0)   True Negative (TN)    False Negative (FN) <-- CRITICAL THREAT
Pred Suspicious (1)  False Positive (FP)   True Positive (TP)
```

- **False Negative (FN)**: User clicks malicious link classified as "Safe-Looking". High risk.
- **False Positive (FP)**: Legitimate URL classified as "Suspicious". Low risk (inconvenience).

---

## 4. Decision Threshold Tuning Strategy

Default classification threshold is $t = 0.50$. In high-security environments:
- Lowering threshold (e.g. $t = 0.35$) increases **Recall** (catches more threats) at the cost of slight precision reduction.
- LinkSentinel provides configurable threshold tuning via `src/models/train_evaluate.py`.
