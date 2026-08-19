# Agent Workflow: Data Validation

**Goal**: Validate a raw URL dataset before it enters the ML feature engineering pipeline.

---

## Preconditions
1. Raw dataset exists in `data/raw/<dataset_name>.csv` or `data/raw/<dataset_name>.parquet`.
2. Environment has `pandas` and `tldextract` installed.

---

## Execution Steps

1. **Schema Check**:
   Verify required columns exist (`url`, `label`).
2. **Encoding Verification**:
   Ensure `label` is binary (`0` = Safe-Looking, `1` = Suspicious).
3. **Duplicate Audit**:
   Identify and log exact duplicate URL strings. Remove duplicates while logging count.
4. **Missing Value Audit**:
   Check for null, empty, or non-string URL entries. Drop corrupt rows.
5. **Class Imbalance Check**:
   Calculate class distribution ratio. Log warning if ratio exceeds 90:10.
6. **Malformed URL Filter**:
   Verify URL strings start with valid protocols or standard domain patterns.
7. **Generate Report**:
   Write summary statistics to `reports/data_validation_report.md`.

---

## Mandatory Constraints (Never Do)
- **NEVER** modify raw data in `data/raw/`.
- **NEVER** open URLs, issue HTTP requests, or perform DNS lookups.
- **NEVER** silently discard suspicious records without logging.

---

## Output Artifacts
- `data/processed/validated_dataset.csv`
- `reports/data_validation_report.md`
