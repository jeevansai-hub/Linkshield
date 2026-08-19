# Data Engineering Guide — LinkSentinel

> **Document Scope**: Sourcing, storage, validation, splitting, transformation, and governance of URL datasets for LinkSentinel (`LinkShield`).

---

## 1. Data Taxonomy & Categories

LinkSentinel categorizes datasets into four strict operational tiers:

```
┌────────────────────────────────────────────────────────┐
│ 1. Raw Training Data (data/raw/)                       │
│    - Immutably stored source CSV/Parquet files         │
│    - Examples: PhishTank, Kaggle Malicious URLs        │
└──────────────────────────┬─────────────────────────────┘
                           │ Validation & Preprocessing
                           ▼
┌────────────────────────────────────────────────────────┐
│ 2. Processed Splits (data/processed/)                  │
│    - Train Set (80%): Feature matrix X_train, y_train │
│    - Val Set   (10%): Feature matrix X_val, y_val    │
│    - Test Set  (10%): Feature matrix X_test, y_test   │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ 3. Mock Data (tests/mock_urls.json)                    │
│    - Synthetic static URL fixtures for unit tests      │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ 4. External Real-World Data (data/external/)           │
│    - Fresh out-of-sample URL feeds (Tranco, OpenPhish) │
│    - Used exclusively for real-world robustness checks │
└────────────────────────────────────────────────────────┘
```

---

## 2. Raw Data Immutability Rule

- Files under `data/raw/` MUST NEVER be modified, edited, appended to, or overwritten.
- All cleaning, filtering, deduplication, and feature extraction outputs MUST write to new files in `data/processed/`.

---

## 3. Zero Live Network Request Mandate

> [!CAUTION]
> **CRITICAL SECURITY REQUIREMENT**: Under no circumstances shall data validation or feature engineering scripts initiate DNS queries, HTTP GET/HEAD requests, TCP connections, or page scraping against URLs contained in raw datasets.
> All URL parsing must be executed 100% in-memory using static string parsing (`urllib.parse`, `tldextract`, RegEx).

---

## 4. Train / Validation / Test Splitting Strategy

- **Stratified Split**: Splitting MUST preserve class distribution (`stratify=y`).
- **Standard Ratio**: 80% Training, 10% Validation (hyperparameter tuning), 10% Test (final holdout).
- **Random Seed**: `random_state = 42` mandatory across all splits to guarantee reproducibility.
- **No Data Leakage**: Feature scaling parameters (mean, standard deviation) and encodings MUST be fitted exclusively on `X_train`. Transformation is applied to `X_val`, `X_test`, and `X_external` using the fitted scaler.

---

## 5. Schema & Label Encoding

Target binary classification labels:

| Label Value | String Representation | Security Classification | Meaning |
| :--- | :--- | :--- | :--- |
| `0` | `safe_looking` | Safe-Looking (Legitimate) | Low likelihood of threat based on static features. |
| `1` | `suspicious` | Suspicious (Malicious/Phishing) | High probability of malicious intent. |

---

## 6. Dataset Quality Checks

Before any raw dataset enters `data/processed/`, it MUST pass the automated validation pipeline:
1. Column schema verification (`url`, `label`).
2. Duplicate URL removal.
3. Class distribution check (alert if imbalance exceeds 90:10 without re-sampling strategies).
4. Null / Missing value removal.
5. Verification of URL string formatting (must be valid ASCII / UTF-8 string).
