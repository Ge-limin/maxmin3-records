"""Stage 2: basin hopping from the best known n-point configuration.

Each round starts SLSQP from one of:
  - the current best with a few points jiggled,
  - the best (n-1)-point set plus one new point,
  - the best (n+1)-point set minus one point.

    python improve.py N SECONDS SEED
"""
import sys
import time
import numpy as np
from common import Polisher, load_best, offer_best, ratio2

n, budget, seed = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
rng = np.random.default_rng(seed)
polish = Polisher(n)
best = load_best(n)
if best is None:
    sys.exit(f"n={n}: no starting configuration in bests/")
X, r = polish(best)  # first finish the local optimisation of the current best
best_r = ratio2(best)
if r < best_r:
    best, best_r = X, r
    offer_best(X, f"i{seed}")
t0 = time.time()
tries = wins = 0
while time.time() - t0 < budget:
    tries += 1
    cur = load_best(n)  # another worker may have improved it
    if ratio2(cur) < best_r:
        best, best_r = cur, ratio2(cur)
    below, above = load_best(n - 1), load_best(n + 1)
    u = rng.uniform()
    if u < 0.2 and below is not None:
        c = below.mean(0)
        d = rng.normal(size=3)
        d /= np.linalg.norm(d)
        rad = np.linalg.norm(below - c, axis=1).max()
        X = np.vstack([below, c + d * rad * rng.uniform(0.3, 1.0)])
    elif u < 0.3 and above is not None:
        X = np.delete(above, rng.integers(n + 1), axis=0)
    else:
        X = best.copy()
        k = rng.integers(1, max(2, n // 4))
        idx = rng.choice(n, k, replace=False)
        X[idx] += rng.normal(scale=rng.choice([0.05, 0.15, 0.4]), size=(k, 3))
    X = X + rng.normal(scale=1e-3, size=X.shape)
    X, r = polish(X)
    if r < best_r * (1 - 1e-10):
        wins += 1
        best, best_r = X, r
        offer_best(X, f"i{seed}")
        print(f"n={n} r^2 = {r:.10f} at try {tries} ({time.time() - t0:.0f}s)", flush=True)
print(f"n={n} seed={seed} improve best r^2 = {best_r:.10f} wins={wins} tries={tries}")
