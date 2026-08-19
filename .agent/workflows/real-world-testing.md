# Agent Workflow: Real-World Testing

**Goal**: Execute out-of-sample real-world URL testing to verify classifier generalization and measure inference latency (<50ms limit).

---

## Preconditions
1. External test dataset exists in `data/external/real_world_urls.csv`.
2. Model artifact `models/linksentinel_model_latest.joblib` is loaded.

---

## Execution Steps

1. **Load External Dataset**:
   Load out-of-sample URL strings from `data/external/`.
2. **Execute Static Extraction**:
   Run static feature extraction on external URL strings.
3. **Inference Latency Benchmark**:
   Measure wall-clock latency per URL using `time.perf_counter()`.
   Verify average latency is `<50ms` (Target: `<10ms`).
4. **Compute 5-Metric Suite**:
   Calculate Accuracy, Precision, Recall, F1-Score, and ROC-AUC on external feed.
5. **Robustness Report**:
   Log performance comparison between holdout test set and real-world out-of-sample set in `reports/real_world_testing_report.md`.

---

## Mandatory Constraints (Never Do)
- **NEVER** issue live HTTP requests to real-world URLs during testing.
- **NEVER** overwrite model binary based on real-world testing without retraining workflow.

---

## Output Artifacts
- `reports/real_world_testing_report.md`
