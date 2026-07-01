# Benchmark results

Generated from the labeled corpus in this directory via
[`evaluate.py`](evaluate.py). The corpus design and methodology are documented in
[README.md](README.md); the numbers below are reproduced by running the real
scanner, not asserted by hand.

```bash
pip install -e .
python benchmark/evaluate.py
```

---

## Precision / recall / F1

For the set of expected `(file, family)` pairs `E` and the set the scanner
detects `D`:

- **Precision** = `|E ∩ D| / |D|` — of everything flagged, how much was correct.
- **Recall** = `|E ∩ D| / |E|` — of everything that should have been flagged, how
  much was caught.
- **F1** = harmonic mean of precision and recall (a single combined figure).

The corpus (**15 files, 9 languages, 26 labeled findings**) includes adversarial
**decoys**: crypto names inside comments, docstrings, log messages, and exception
strings, plus word-boundary traps (`md5sumLabel`, `rc4legacyName`, `dsaCount`).
`evaluate.py` runs the scanner **twice** — once as a naive line-level regex, once
with QuantumSafe's string/comment-aware pass — so the effect is measured, not
asserted:

| Configuration | TP | FP | FN | Precision | Recall | F1 |
|---|--:|--:|--:|--:|--:|--:|
| Naive line-regex baseline | 26 | 14 | 0 | 65.0% | 100% | 78.8% |
| **QuantumSafe (usage-aware)** | **26** | **0** | **0** | **100%** | **100%** | **100%** |

The usage-aware pass removes **14 false positives** — every one a keyword mention
inside a Python docstring, log string, or exception message — **without losing a
single true positive**, so recall stays 100%. The `positive/mixed.py` case is the
clearest: real `dsa.generate_private_key(...)` and `hashlib.sha1(...)` usage is
still caught, while the `RSA`/`MD5` that appear only in its docstring and a log
string are correctly ignored. Comment-only mentions and word-boundary traps are
handled by the comment filter and anchored patterns as before.

---

## Risk distribution (labeled findings)

Derived from `labels.json` (26 findings across the positive corpus).

### By crypto family

| Family | Findings | Severity |
|--------|---------:|----------|
| RSA    | 6 | HIGH |
| MD5    | 5 | HIGH |
| SHA-256| 3 | LOW |
| SHA-1  | 3 | HIGH |
| ECC    | 2 | HIGH |
| DSA    | 2 | HIGH |
| DH     | 1 | HIGH |
| 3DES   | 1 | MEDIUM |
| RC4    | 1 | MEDIUM |
| TLS old| 1 | MEDIUM |
| AES-128| 1 | LOW |

### By severity

| Severity | Findings | Share |
|----------|---------:|------:|
| HIGH     | 19 | 73% |
| MEDIUM   | 3  | 12% |
| LOW      | 4  | 15% |

(HIGH = `rsa, ecc, dsa, dh, md5, sha1`; MEDIUM = `tls_old, 3des, rc4`;
LOW = `sha256, aes128`.)

---

## Scan performance

The detection engine is pure-Python static analysis with no network calls per
file. Practical throughput is dominated by file I/O and regex matching; the engine
skips vendor directories and files over 2 MB (e.g. minified bundles) so scan time
scales roughly linearly with the number of in-scope source files. The
reproducible measurement (scan time vs. corpus size) is produced by the graph
script below rather than quoted as a fixed number, since it depends on the host.

---

## Reproducible charts

The script in [`graphs/generate_graphs.py`](graphs/generate_graphs.py) regenerates
three figures from live data (it runs the real scanner — it does not hardcode the
numbers above):

1. **Bar chart** — vulnerabilities by crypto family.
2. **Pie chart** — HIGH / MEDIUM / LOW distribution.
3. **Line chart** — scan time vs. number of files.

```bash
pip install matplotlib
python benchmark/graphs/generate_graphs.py     # writes PNGs into benchmark/graphs/
```

`matplotlib` is intentionally **not** part of the core or CI requirements — the
chart script is an optional, standalone tool, so the main project stays
dependency-light.

---

## Honest framing

This is a **regression benchmark**, not a large-scale field study. 100% on 26
findings across 15 files demonstrates the approach and guards against regressions;
it is **not** a claim of perfect accuracy on arbitrary code. The point of the
naive-vs-improved comparison is to quantify a specific, real improvement (string /
comment awareness) honestly — including that the naive approach's recall is already
100% here, so the win is precision, not coverage. See [README.md](README.md) and
[../TECHNICAL_OVERVIEW.md](../TECHNICAL_OVERVIEW.md) for the limitations.
