"""Summary of bests/: exact value, contact counts, a convergence sign.

A strict local optimum of "minimise max/min distance" needs at least
3k-5 active pairs among its k rigidly held points (3k coordinates plus the
ratio, minus 6 rigid motions). Points touching fewer than 4 active pairs
can move a little without changing the ratio (like rattlers in a packing),
so they are stripped repeatedly first; what remains is the rigid core.
`core active >= 3k-5` is a necessary sign of convergence, not a proof.

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
        A = np.zeros((n, n), bool)
        A[np.triu_indices(n, 1)] = (s <= s.min() * (1 + TOL)) | (s >= s.max() * (1 - TOL))
        A |= A.T
        core = np.ones(n, bool)
        while True:
            weak = core & (A[:, core].sum(1) < 4)
            if not weak.any():
                break
            core &= ~weak
        k = int(core.sum())
        core_active = int(A[np.ix_(core, core)].sum() // 2)
        r = exact_ratio2(grid_points(X.tolist()))
        yield n, r, nmin, nmax, k, core_active


if __name__ == "__main__":
    loose = "--loose" in sys.argv
    for n, r, nmin, nmax, k, core_active in rows():
        need = 3 * k - 5
        ok = core_active >= need
        if loose:
            if not ok and n >= 31:
                print(n)
            continue
        print(f"n={n:2d}  r^2 <= {claim(r)}  min pairs={nmin:3d}  max pairs={nmax:2d}  "
              f"loose points={n - k}  core active={core_active:3d} / needed {need:3d}  "
              f"{'ok' if ok else 'LOOSE'}")
