"""Run the labeled benchmark as part of the suite (guards detector accuracy)."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "benchmark"))

from evaluate import evaluate  # noqa: E402


def test_scanner_meets_accuracy_thresholds():
    r = evaluate()
    # Thresholds sit below the current 100% to leave honest headroom while still
    # catching real regressions.
    assert r["precision"] >= 0.9, f"precision dropped: FPs={r['fp']}"
    assert r["recall"] >= 0.9, f"recall dropped: FNs={r['fn']}"


def test_decoys_produce_no_false_positives():
    r = evaluate()
    assert all(not fp[0].startswith("negative/") for fp in r["fp"]), r["fp"]
