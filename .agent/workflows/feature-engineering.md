# Agent Workflow: Feature Engineering

**Goal**: Transform validated raw URL strings into numerical feature matrices using static lexical parsing.

---

## Preconditions
1. Validated dataset exists at `data/processed/validated_dataset.csv`.
2. Static feature extractor module `src/features/extract_features.py` is operational.

---

## Execution Steps

1. **Initialize Extractor**:
   Instantiate `URLLexicalFeatureExtractor()` from `src/features/extract_features.py`.
2. **Feature Extraction Loop**:
   Iterate through URL strings and extract static feature dictionaries.
3. **Feature Schema Alignment**:
   Verify all extracted feature vectors conform to the schema defined in `docs/PROJECT_REFERENCE.md`.
4. **Data Splitting**:
   Execute stratified split (`train_test_split(..., stratify=y, test_size=0.20, random_state=42)`).
5. **Preprocessing & Scaling**:
   Fit `StandardScaler()` strictly on `X_train`. Transform `X_train`, `X_val`, and `X_test`.
6. **Persist Artifacts**:
   Save numpy/pandas feature matrices to `data/processed/features_v1.parquet`.

---

## Mandatory Constraints (Never Do)
- **NEVER** perform live network connections during extraction.
- **NEVER** fit scalers on test or combined data (prevent data leakage).
- **NEVER** introduce undocumented features without updating `docs/PROJECT_REFERENCE.md`.

---

## Output Artifacts
- `data/processed/features_train.parquet`
- `data/processed/features_test.parquet`
- `models/scaler_v1.joblib`
