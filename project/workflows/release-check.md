# Agent Workflow: Pre-Flight Release Check

**Goal**: Validate repository readiness before merging a feature branch or tagging a release version.

---

## Execution Checklist

1. **Unit Test Verification**:
   Execute `pytest tests/` and verify 100% test pass rate.
2. **Linting & Code Style**:
   Execute `flake8 src/ tests/` and verify zero style or syntax warnings.
3. **Documentation Sync**:
   Verify any new URL features added to `src/features/extract_features.py` are documented in `docs/PROJECT_REFERENCE.md`.
4. **Safety Verification**:
   Confirm zero live network queries are present in extraction logic.
5. **Metric Verification**:
   Verify all ML model checkpoints include evaluation logs for all 5 required metrics.
6. **Git Status Check**:
   Ensure no temporary files or raw data mutations exist in workspace.

---

## Output Artifacts
- `reports/release_check_passed.log`
