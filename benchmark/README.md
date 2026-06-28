# Scanner evaluation benchmark

A labeled benchmark that measures how well the QuantumSafe scanner actually works
— so "it detects vulnerable crypto" is a *measured* claim, not an assertion.

## Run it

```bash
pip install -e .
python benchmark/evaluate.py
```

## Method

- **Ground truth** (`labels.json`) is defined at **(file, detection-family)**
  granularity by hand.
- `benchmark/positive/` contains known-vulnerable code; `benchmark/negative/`
  contains safe code and **decoys** designed to trip a naive matcher:
  crypto names that appear only in **comments**, and **word-boundary traps**
  (`md5sumLabel`, `rc4legacyName`, `dsaCount`) that must *not* match.
- `evaluate.py` runs the real scanner, compares detected vs. expected pairs, and
  reports precision / recall / F1 **plus the exact false positives and false
  negatives**, so the numbers are auditable.

## Results (current)

| Metric | Value |
|--------|-------|
| Files | 12 (9 positive, 3 negative/decoy) across 9 languages |
| Labeled findings | 24 |
| True positives | 24 |
| False positives | 0 |
| False negatives | 0 |
| **Precision** | **100%** |
| **Recall** | **100%** |

The comment decoys produce zero false positives because the regex engine skips
comment-only lines; the word-boundary traps are excluded by anchored patterns.

## Honest limitations (what this benchmark does *not* prove)

This is a focused regression benchmark, not a large-scale field study. Real-world
caveats, stated plainly:

- **Small scale:** 12 files / 24 findings. It guards against regressions and
  demonstrates the approach; it is not a claim of 100% accuracy on arbitrary code.
- **Inline comments & string literals:** the scanner skips *comment-only* lines,
  but a crypto name in a *trailing* comment (`x = 1  # drop RSA`) or inside a
  string can still be a false positive. Block comments are only partially handled.
- **Regex outside Python:** only Python gets AST precision; other languages are
  regex-based, so unusual crypto wrappers can be missed (false negatives).

These are the genuine edges of a static pattern-based approach — see
`TECHNICAL_OVERVIEW.md` for how AST/Tree-sitter parsing would address them.
