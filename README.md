# LinkSentinel (LinkShield)

> **Real-Time Malicious URL Detection Engine powered by Static Machine Learning Feature Extraction**

---

## 🛡️ Project Overview & Motivation

Phishing attacks, drive-by malware downloads, and malicious link distribution represent major cyber threat vectors. Traditional detection techniques relying on static blacklists (such as Google Safe Browsing or DNS blocklists) suffer from **zero-day vulnerability gaps**—they fail to detect newly registered or dynamically generated phishing URLs before the domain is reported and blacklisted.

**LinkSentinel** (hosted in repository workspace `LinkShield`) addresses this limitation by deploying an inline, lightweight Machine Learning classifier that evaluates raw URLs in **real-time (<50ms inference latency target)** using **static lexical, host, and structural feature analysis**.

---

## 🏗️ Architecture & Pipeline

LinkSentinel avoids live network requests (preventing drive-by execution and network overhead) by relying strictly on static parsing of URL structures.

```
                    ┌─────────────────────────┐
                    │    Input Raw URL        │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Static Feature Extractor│
                    │   (src/features/)       │
                    └────────────┬────────────┘
                                 │ Lexical, Host, Path, Query Features
                                 ▼
                    ┌─────────────────────────┐
                    │ Preprocessing Transformer│
                    │  (StandardScaler/Dict)  │
                    └────────────┬────────────┘
                                 │ Numeric Feature Vector
                                 ▼
                    ┌─────────────────────────┐
                    │ Trained ML Classifier   │
                    │ (Logistic / XGB / Light)│
                    └────────────┬────────────┘
                                 │ Risk Score (0.0 to 1.0)
                                 ▼
                    ┌─────────────────────────┐
                    │  Risk Classification    │
                    │  [Safe-Looking /        │
                    │   Suspicious]           │
                    └─────────────────────────┘
```

---

## 📊 The 5 Mandatory Evaluation Metrics

In threat classification, relying solely on **Accuracy** is dangerously misleading because malicious URLs often represent an imbalanced fraction of web traffic, and false negatives (missing a malicious URL) have catastrophic security consequences. LinkSentinel mandates reporting **all five evaluation metrics**:

1. **Accuracy**: Overall fraction of correct predictions across both safe and suspicious links.
2. **Precision**: $\frac{\text{TP}}{\text{TP} + \text{FP}}$ — Measures how many flagged links are genuinely suspicious (minimizes false alarms for legitimate users).
3. **Recall (Sensitivity)**: $\frac{\text{TP}}{\text{TP} + \text{FN}}$ — Measures the proportion of actual malicious URLs caught (minimizes security breaches).
4. **F1-Score**: Harmonic mean of Precision and Recall ($\frac{2 \cdot P \cdot R}{P + R}$), providing a single balanced operational score.
5. **ROC-AUC**: Area Under the Receiver Operating Characteristic Curve, measuring classifier discrimination capacity across all decision thresholds independently of class balance.

---

## 🚀 Quickstart & Usage

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/user/LinkShield.git
cd LinkShield

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Tests
```bash
pytest tests/
```

### 3. Static Feature Extraction Example
```python
from src.features.extract_features import URLLexicalFeatureExtractor

extractor = URLLexicalFeatureExtractor()
features = extractor.extract("http://login.paypal.account-update.com/verify?id=123")

print(features)
# Output: {'url_length': 52, 'num_dots': 3, 'has_ip': 0, 'num_hyphens': 1, 'is_https': 0, ...}
```

### 4. Baseline Training & Evaluation
```python
from src.models.train_evaluate import ModelPipeline

pipeline = ModelPipeline(model_type="logistic_regression")
metrics, model = pipeline.fit_and_evaluate(X_train, y_train, X_test, y_test)
print(metrics)
```

---

## 🔒 Safety & Zero-Trust Constraints

- **Static Analysis Only**: LinkSentinel never executes HTTP requests, DNS lookups, or page rendering during feature extraction. This guarantees that checking a malicious link does NOT trigger a drive-by download or alert an attacker.
- **Terminology Standard**: Predictions are categorized as **`Safe-Looking`** or **`Suspicious`**. LinkSentinel never guarantees absolute safety.

---

## 📂 Project Structure & Reference System

LinkSentinel includes a complete project reference system designed for human developers and AI coding agents:

- [`AGENTS.md`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/AGENTS.md) — 20 global developer/AI constraints.
- [`docs/PROJECT_REFERENCE.md`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/docs/PROJECT_REFERENCE.md) — Technical architecture & feature definitions.
- [`docs/DATA_GUIDE.md`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/docs/DATA_GUIDE.md) — Data engineering, storage, and validation standards.
- [`docs/ML_GUIDE.md`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/docs/ML_GUIDE.md) — Feature engineering, training, and model persistence.
- [`docs/EVALUATION_GUIDE.md`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/docs/EVALUATION_GUIDE.md) — Metric analysis, confusion matrices, and decision thresholds.
- [`docs/SAFETY.md`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/docs/SAFETY.md) — Security boundaries and zero-trust guidelines.
- [`.agent/workflows/`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/.agent/workflows/) — Executable agent task workflows.

---

## 🛣️ Future Scope

- ONNX Runtime export for browser extension integration (<10ms inference).
- Character-level CNN / Transformer static embeddings for obfuscated payload URLs.
- Automated quarterly model retraining on updated PhishTank datasets.
