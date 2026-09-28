"""Exact check of configurations, independent of the search code.

Coordinates are rounded to integers on a 1e-12 grid, so every squared
distance is an exact integer and r^2 = max/min is an exact fraction.
The value we claim is that fraction rounded UP at the 5th decimal, and the
coordinates we publish are exactly these grid points.

    python verify.py bests/n31.npy [bests/n32.npy ...]
"""
import sys
from decimal import Decimal, ROUND_CEILING
from fractions import Fraction
from itertools import combinations

SCALE = 10 ** 12


def grid_points(points):
    P = [tuple(int(round(float(c) * SCALE)) for c in p) for p in points]
    assert len(set(P)) == len(P), "duplicate points"
    return P


def exact_ratio2(P):
    d = [sum((a - b) ** 2 for a, b in zip(p, q)) for p, q in combinations(P, 2)]
    return Fraction(max(d), min(d))


def claim(r):
    return (Decimal(r.numerator) / Decimal(r.denominator)).quantize(
        Decimal("0.00001"), rounding=ROUND_CEILING)


if __name__ == "__main__":
    import numpy as np
    for path in sys.argv[1:]:
        X = np.load(path)
        assert X.ndim == 2 and X.shape[1] == 3
        r = exact_ratio2(grid_points(X.tolist()))
        print(f"{path}: n={len(X)} exact r^2 = {float(r):.12f}  claim r^2 <= {claim(r)}")
