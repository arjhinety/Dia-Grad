"""Measurements for the tranche-1 feasibility gate (prereg/PREREGISTRATION.md section 7a).

- retrieval_error: cross-lingual retrieval error (xsim-style) on aligned pairs;
- probe_scores: linear probe, balanced accuracy, 5-fold cross-validation, out-of-fold per-sentence
  correctness kept for the bootstrap;
- gap_ci: two-sided 95% bootstrap interval of (drafter probe - z_m probe), resampling sentences;
- label_po_opo / label_ay_inversion: automatic labels (the ay detector is provisional and must be
  checked against 200 hand-labelled sentences before use).
"""
from __future__ import annotations

import re

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def retrieval_error(a: np.ndarray, b: np.ndarray) -> float:
    """Share of rows i in `a` whose nearest row in `b` (cosine) is not row i. a, b: [N, D], aligned."""
    a = a / np.linalg.norm(a, axis=1, keepdims=True)
    b = b / np.linalg.norm(b, axis=1, keepdims=True)
    nearest = (a @ b.T).argmax(axis=1)
    return float((nearest != np.arange(len(a))).mean())


def _balanced_accuracy(y: np.ndarray, correct: np.ndarray) -> float:
    return float(np.mean([correct[y == c].mean() for c in np.unique(y)]))


def probe_scores(x: np.ndarray, y: np.ndarray, seed: int = 0, folds: int = 5) -> tuple[float, np.ndarray]:
    """Balanced accuracy of a linear probe and the per-sentence out-of-fold correctness vector."""
    correct = np.zeros(len(y), dtype=bool)
    for tr, te in StratifiedKFold(folds, shuffle=True, random_state=seed).split(x, y):
        clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
        clf.fit(x[tr], y[tr])
        correct[te] = clf.predict(x[te]) == y[te]
    return _balanced_accuracy(y, correct), correct


def gap_ci(y: np.ndarray, correct_a: np.ndarray, correct_b: np.ndarray,
           resamples: int = 10_000, seed: int = 0) -> tuple[float, float, float]:
    """Point estimate and two-sided 95% bootstrap interval (2.5th, 97.5th percentile) of
    balanced_accuracy(a) - balanced_accuracy(b), resampling sentences (same draw for a and b)."""
    rng = np.random.default_rng(seed)
    n = len(y)
    diffs = np.empty(resamples)
    for i in range(resamples):
        idx = rng.integers(0, n, n)
        yi = y[idx]
        if len(np.unique(yi)) < 2:
            diffs[i] = np.nan
            continue
        diffs[i] = _balanced_accuracy(yi, correct_a[idx]) - _balanced_accuracy(yi, correct_b[idx])
    point = _balanced_accuracy(y, correct_a) - _balanced_accuracy(y, correct_b)
    lo, hi = np.nanpercentile(diffs, [2.5, 97.5])
    return point, float(lo), float(hi)


_WORD = re.compile(r"[\wÀ-ÿñÑ'-]+", re.UNICODE)


def label_po_opo(sentence: str) -> int:
    """1 if the sentence contains the politeness marker `po` or `opo` as a separate word."""
    return int(any(w in ("po", "opo") for w in (t.lower() for t in _WORD.findall(sentence))))


def label_ay_inversion(sentence: str) -> int:
    """PROVISIONAL rule: 1 if the word `ay` occurs after at least one word (the inverted
    'topic ay predicate' order, e.g. "Ang bata ay kumain"). Sentence-initial `Ay` (an interjection)
    does not count. Known gap [inference]: `ay` inside quoted or code-switched text also counts.
    Must be checked against 200 hand-labelled sentences (prereg 7a) before the gate uses it."""
    words = [t.lower() for t in _WORD.findall(sentence)]
    return int(any(w == "ay" for w in words[1:]))
