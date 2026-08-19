# AGENTS.md — Global AI Agent & Developer Rules

> **Project Identity**: `LinkShield` (ML-driven Real-Time Malicious URL Detection Engine)  
> **Repository Directory**: `LinkShield`  
> **Status**: Core Technical Specification & Single Source of Truth

---

## 1. Executive Directive

This file defines the mandatory coding, machine learning, data engineering, evaluation, and security principles for any human developer or AI coding agent working on **LinkShield**.

Before performing any code modification, feature addition, dataset cleaning, model training, or evaluation, **agents MUST read and comply with these rules**.

---

## 2. The 20 Global Agent Rules

1. **Understand before modifying**: Read existing code, docstrings, tests, and documentation before making changes.
2. **Never invent data, metrics, or experimental results**: All numbers, latency metrics, and performance tables must come from empirical execution logs.
3. **Never train on test data**: Maintain strict train/validation/test segregation at all times.
4. **Never leak test information into preprocessing**: Preprocessing transformations (scalers, encoders, imputers) MUST be fit ONLY on training data.
5. **Never claim "safe"**: Output classifications MUST use probabilistic terms like `"safe-looking"` (low risk) or `"suspicious"` (high risk). Never claim a URL is guaranteed safe.
6. **Never open suspicious URLs during dataset processing**: Feature extraction MUST be 100% static parsing. Never issue HTTP GET/HEAD requests, follow redirects, or download content from untrusted domains.
7. **Keep raw data immutable**: Raw datasets (`data/raw/`) are read-only artifacts and must never be mutated or overwritten in-place.
8. **Make experiments reproducible**: Fix random seeds (`random_state=42`) across NumPy, scikit-learn, PyTorch/XGBoost/LightGBM, and data splits.
9. **Prefer simple, explainable models first**: Start with Logistic Regression as a baseline. Advance to Random Forest, XGBoost, or LightGBM only when empirical gains are justified.
10. **Every ML change must have evaluation evidence**: No pull request or model update will be merged without generating all five mandatory evaluation metrics.
11. **Every important feature must have a documented definition**: Any feature added to `src/features/extract_features.py` must be explicitly defined in `docs/PROJECT_REFERENCE.md`.
12. **Never silently change the target-label meaning**: Label conventions are strictly: `0` = Safe-Looking (Legitimate), `1` = Suspicious (Malicious/Phishing).
13. **Never hard-code dataset-specific assumptions without documentation**: Avoid hardcoded column indexes, dataset paths, or magic numbers without clear constants or config definitions.
14. **Keep notebooks for experimentation and `src/` for reusable logic**: Prototypes live in `notebooks/`. Production logic MUST be refactored into modular `src/` packages.
15. **Test feature extraction independently from model training**: Unit tests MUST verify feature extraction functions on static sample URLs isolated from model objects.
16. **Do not optimize for Accuracy alone**: False negatives (classifying a malicious URL as safe) carry extreme real-world risk. Recall and ROC-AUC are critical metrics.
17. **Report all five required evaluation metrics**: Every evaluation report MUST include **Accuracy, Precision, Recall, F1-Score, and ROC-AUC**.
18. **Never fabricate benchmark results**: Real-time inference latency (e.g., `<50ms`) is a measurable target to be verified with benchmark scripts, not a hardcoded claim.
19. **Keep security and privacy boundaries explicit**: Input URLs may contain sensitive query tokens, authentication parameters, or PII. Log redactors must strip credentials.
20. **Prefer small, verifiable changes over large rewrites**: Implement incremental, fully tested modular additions with clear commit descriptions.

---

## 3. Architecture & Directory Boundaries

```text
LinkShield/
├── README.md               # Human-facing project entry point
├── AGENTS.md               # Global AI/developer rules (THIS FILE)
├── requirements.txt        # Python dependency manifest
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI automation
├── docs/
│   ├── PROJECT_REFERENCE.md# Complete technical architecture & data flow
│   ├── DATA_GUIDE.md       # Data sourcing, cleaning, splitting & schemas
│   ├── ML_GUIDE.md         # Pipeline, feature engineering & model persistence
│   ├── EVALUATION_GUIDE.md # 5-metric evaluation, threshold tuning & error analysis
│   └── SAFETY.md           # Zero-trust safety, static parsing & threat boundaries
├── .agent/
│   └── workflows/          # Step-by-step executable workflows for agents
│       ├── data-validation.md
│       ├── feature-engineering.md
│       ├── model-training.md
│       ├── model-evaluation.md
│       ├── real-world-testing.md
│       └── release-check.md
├── src/                    # Production Python code
│   ├── __init__.py
│   ├── features/           # Static URL feature extractors
│   │   ├── __init__.py
│   │   └── extract_features.py
│   ├── models/             # Model training & inference logic
│   │   ├── __init__.py
│   │   └── train_evaluate.py
│   └── utils/              # 5-metric calculation & report utilities
│       ├── __init__.py
│       └── metrics.py
├── tests/                  # Automated unit and integration tests
│   ├── test_features.py
│   └── test_metrics.py
├── data/                   # Immutable raw & processed datasets
│   ├── raw/
│   ├── processed/
│   └── external/
├── models/                 # Saved model binaries (.pkl / .joblib)
├── notebooks/              # Jupyter notebooks for EDA and experiment logs
└── reports/                # Generated evaluation markdown and charts
```

---

## 4. Coding & Quality Standards

- **Python Version**: 3.10+
- **Code Style**: PEP 8 compliant, checked with `flake8`.
- **Type Annotations**: All public functions in `src/` must have type hints.
- **Docstrings**: Google-style docstrings for all modules, classes, and functions.
- **Error Handling**: Use explicit, specific exceptions (`ValueError`, `KeyError`, `URLError`). Never use bare `except:`.
- **Testing**: `pytest` / `unittest` must pass 100% cleanly before any code is marked done.

---

## 5. Definition of Done (DoD)

A task or feature for LinkShield is complete ONLY when:
1. All relevant rules in `AGENTS.md` are respected.
2. Code passes `unittest` unit tests cleanly.
3. Code complies with `flake8` lint checks.
4. All 5 metrics (Accuracy, Precision, Recall, F1-Score, ROC-AUC) are documented if ML components are modified.
5. `docs/PROJECT_REFERENCE.md` or related docs are updated if signatures or features change.
