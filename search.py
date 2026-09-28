"""Stage 1: random multistart. Starts SLSQP from random points in a ball.

    python search.py N SECONDS SEED
"""
import sys
import time
import numpy as np
from common import Polisher, load_best, offer_best, ratio2

n, budget, seed = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
rng = np.random.default_rng(seed)
polish = Polisher(n)
cur = load_best(n)
best = ratio2(cur) if cur is not None else np.inf
hits = starts = 0
t0 = time.time()
while time.time() - t0 < budget:
    starts += 1
    X = rng.normal(size=(n, 3))
    X *= rng.uniform(size=(n, 1)) ** (1 / 3) / np.linalg.norm(X, axis=1, keepdims=True)
    X, r = polish(X)
    if abs(r - best) < 1e-8 * best:
        hits += 1
    elif r < best:
        best, hits = r, 1
        offer_best(X, f"s{seed}")
        print(f"n={n} r^2 = {r:.10f} at start {starts} ({time.time() - t0:.0f}s)", flush=True)
print(f"n={n} seed={seed} search best r^2 = {best:.10f} hits={hits} starts={starts}")
