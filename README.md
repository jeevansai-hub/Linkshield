# LinkSentinel (LinkShield)

> **Real-Time Malicious URL Detection Engine powered by Static Machine Learning Feature Extraction**

---

## 🛡️ Project Overview & Motivation

Phishing attacks, drive-by malware downloads, and malicious link distribution represent major cyber threat vectors. Traditional detection techniques relying on static blacklists (such as Google Safe Browsing or DNS blocklists) suffer from **zero-day vulnerability gaps**—they fail to detect newly registered or dynamically generated phishing URLs before the domain is reported and blacklisted.

**LinkSentinel** (hosted in repository workspace `LinkShield`) addresses this limitation by deploying an inline, lightweight Machine Learning classifier that evaluates raw URLs in **real-time (<50ms inference latency target)** using **static lexical, host, and structural feature analysis**.

---

## 🏗️ Architecture & Pipeline

LinkSentinel avoids live network requests (preventing drive-by execution and network overhead) by relying strictly on static parsing of URL structures.

```text
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
                    │ Preprocessing Pipeline  │
                    │  (StandardScaler/Dict)  │
                    └────────────┬────────────┘
                                 │ Numeric Feature Vector
                                 ▼
                    ┌─────────────────────────┐
                    │ Trained ML Classifier   │
                    │ (Logistic / Random For) │
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

## 🚀 Quickstart & Execution Guide (After Cloning)

Follow these step-by-step instructions to run the entire project on your local machine:

### Step 1: Clone Repository & Open Folder
```bash
git clone https://github.com/jeevansai-hub/Linkshield.git
cd Linkshield
```

### Step 2: Set Up Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
venv\Scripts\activate
# On Linux / macOS:
source venv/bin/activate

# Upgrade pip & install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Run Automated Unit Tests
```bash
python -m unittest discover -s tests -p "test_*.py"
```
**Expected Output**:
```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.019s

OK
```

### Step 4: Launch Real-Time Streamlit Web Application
```bash
python -m streamlit run app.py
```
- Automatically opens at `http://localhost:8501`.
- Enter any URL (e.g. `http://login.paypal.account-verify.com/update?id=123`) and click **RUN STATIC RISK ANALYSIS**.
- View the classification badge (`SAFE-LOOKING` / `SUSPICIOUS`), probability %, processing latency (<10ms), and feature breakdown.

### Step 5: Run Instant Prediction via Python CLI
```bash
python -c "import joblib, pandas as pd; from src.features.extract_features import URLLexicalFeatureExtractor; ext = URLLexicalFeatureExtractor(); models = joblib.load('models/linksentinel_models.joblib'); res = models['engine_rf'].predict_proba(pd.DataFrame([ext.extract('http://login.paypal.account-verify.com/update?id=123')])[models['feature_names']])[0]; print('Probability Suspicious:', round(float(res)*100, 2), '%'); print('Label:', 'SUSPICIOUS' if res >= 0.30 else 'SAFE-LOOKING')"
```

---

## 📂 Project Structure & Reference System

LinkSentinel includes a complete project reference system designed for human developers and AI coding agents:

- [`docs/MASTER_PROJECT_DOCUMENTATION.md`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/docs/MASTER_PROJECT_DOCUMENTATION.md) — **Exhaustive Master Technical Documentation**.
- [`AGENTS.md`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/AGENTS.md) — 20 global developer/AI constraints.

- [`docs/PROJECT_REFERENCE.md`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/docs/PROJECT_REFERENCE.md) — Technical architecture & feature definitions.
- [`docs/DATA_GUIDE.md`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/docs/DATA_GUIDE.md) — Data engineering, storage, and validation standards.
- [`docs/ML_GUIDE.md`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/docs/ML_GUIDE.md) — Feature engineering, training, and model persistence.
- [`docs/EVALUATION_GUIDE.md`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/docs/EVALUATION_GUIDE.md) — Metric analysis, confusion matrices, and decision thresholds.
- [`docs/SAFETY.md`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/docs/SAFETY.md) — Security boundaries and zero-trust guidelines.
- [`project/workflows/`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/project/workflows/) — Executable agent task workflows.

- [`reports/activity4_final_report.md`](file:///c:/Users/jeeva/OneDrive/jeevan_workspace/ml%20projects/LinkShield/reports/activity4_final_report.md) — Complete 17-section Activity 4 submission report.

---

## 🔒 Safety & Zero-Trust Constraints

- **Static Analysis Only**: LinkSentinel never executes HTTP requests, DNS lookups, or page rendering during feature extraction. This guarantees that checking a malicious link does NOT trigger a drive-by download or alert an attacker.
- **Terminology Standard**: Predictions are categorized as **`Safe-Looking`** or **`Suspicious`**. LinkSentinel never guarantees absolute safety.
