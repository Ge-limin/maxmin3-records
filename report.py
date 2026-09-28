"""Summary of bests/: exact value, contact counts, a convergence sign.

A strict local optimum of "minimise max/min distance" needs at least
3n-5 active pairs (3n coordinates plus the ratio, minus 6 rigid motions),
so `active >= 3n-5` is a necessary sign of convergence, not a proof.

    python report.py          # table
    python report.py --loose  # just the n that fail the sign (for pipeline.sh)
"""
import glob
import os
import re
import sys
import numpy as np
from common import BESTS
from verify import claim, exact_ratio2, grid_points

TOL = 1e-6


def rows():
    paths = glob.glob(os.path.join(BESTS, "n*.npy"))
    for path in sorted(paths, key=lambda p: int(re.findall(r"n(\d+)\.npy", p)[0])):
        X = np.load(path)
        n = len(X)
        D = X[:, None] - X[None]
        s = (D * D).sum(-1)[np.triu_indices(n, 1)]
        nmin = int((s <= s.min() * (1 + TOL)).sum())
        nmax = int((s >= s.max() * (1 - TOL)).sum())
        r = exact_ratio2(grid_points(X.tolist()))
        yield n, r, nmin, nmax, 3 * n - 5


if __name__ == "__main__":
    loose = "--loose" in sys.argv
    for n, r, nmin, nmax, need in rows():
        ok = nmin + nmax >= need
        if loose:
            if not ok and n >= 31:
                print(n)
            continue
        print(f"n={n:2d}  r^2 <= {claim(r)}  min pairs={nmin:3d}  max pairs={nmax:2d}  "
              f"active={nmin + nmax:3d} / needed {need:3d}  {'ok' if ok else 'LOOSE'}")
