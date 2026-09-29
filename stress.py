"""Stress test: try to beat each best(n) from its neighbours, re-optimised.

For each n: delete every point of best(n+1) in turn and re-polish, and add
a point to best(n-1) from many directions and re-polish. If anything beats
best(n), the result was not good enough; the better one is kept.

    python stress.py N [INSERTIONS]
"""
import sys
import numpy as np
from common import Polisher, load_best, offer_best, ratio2

n = int(sys.argv[1])
insertions = int(sys.argv[2]) if len(sys.argv) > 2 else 60
rng = np.random.default_rng(n)
polish = Polisher(n)
ours = ratio2(load_best(n))
found = []
above, below = load_best(n + 1), load_best(n - 1)
if above is not None:
    for i in range(n + 1):
        found.append(("delete", polish(np.delete(above, i, 0) + rng.normal(scale=1e-3, size=(n, 3)))))
if below is not None:
    c = below.mean(0)
    rad = np.linalg.norm(below - c, axis=1).max()
    for _ in range(insertions):
        d = rng.normal(size=3)
        d /= np.linalg.norm(d)
        X = np.vstack([below, c + d * rad * rng.uniform(0.2, 1.0)])
        found.append(("insert", polish(X + rng.normal(scale=1e-3, size=X.shape))))
best_kind, (X, r) = min(found, key=lambda t: t[1][1])
beat = r < ours * (1 - 1e-9)
if beat:
    offer_best(X, "stress")
print(f"n={n} ours {ours:.10f}  best of {len(found)} neighbour tries {r:.10f} ({best_kind})  "
      f"{'BEATEN -> replaced' if beat else 'held'}")
