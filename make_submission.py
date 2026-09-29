"""Build the submission package for n=31..50 in out/.

For every n: out/mmN.gif (picture in the page's style) and out/coords_nN.txt
(the exact grid coordinates the value was computed from), plus out/email.md
with the value table, symmetry notes and free points filled in. The email
still needs the submitter's full name; nothing is sent from here.

    python make_submission.py
"""
import os
import numpy as np
from common import load_best
from render import render
from symmetry import max_fold, note
from verify import claim, exact_ratio2, grid_points

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
TOL = 1e-6


def free_points(X):
    """Points in no min- or max-distance pair: they can move without changing r."""
    n = len(X)
    D = X[:, None] - X[None]
    s = (D * D).sum(-1)
    iu = np.triu_indices(n, 1)
    tight = (s <= s[iu].min() * (1 + TOL)) | (s >= s[iu].max() * (1 - TOL))
    np.fill_diagonal(tight, False)
    return [i + 1 for i in range(n) if not tight[i].any()]


os.makedirs(OUT, exist_ok=True)
lines, free = [], []
for n in range(31, 51):
    X = load_best(n)
    if X is None:
        print(f"n={n}: missing")
        continue
    P = grid_points(X.tolist())
    r = exact_ratio2(P)
    with open(os.path.join(OUT, f"coords_n{n}.txt"), "w") as f:
        f.write(f"# n={n} points in 3D; r^2 = (max squared distance)/(min squared distance) "
                f"= {r.numerator}/{r.denominator} exactly\n")
        f.write("# x y z per line, each an exact decimal with 12 digits after the point\n")
        for p in P:
            f.write(" ".join(f"{c / 10**12:.12f}" for c in p) + "\n")
    Xg = np.array(P, dtype=float) / 10**12
    nmin, nmax = render(Xg, os.path.join(OUT, f"mm{n}.gif"))
    sym = note(max_fold(Xg))
    fp = free_points(Xg)
    if fp:
        free.append(f"n={n} (point {', '.join(map(str, fp))} in coords_n{n}.txt)")
    lines.append(f"{n}. r^2 = {claim(r)} ({sym})")
    print(f"n={n}: r^2 = {claim(r)}  {sym}  free={fp}  ({nmin} min pairs, {nmax} max pairs)")

free_text = ("In " + "; ".join(free) + ", one point touches neither a shortest nor a longest "
             "pair, so it can move slightly without changing r and appears in the picture as a "
             "dot with no rods.") if free else ""
draft = open(os.path.join(HERE, "email_template.md")).read()
with open(os.path.join(OUT, "email.md"), "w") as f:
    f.write(draft.replace("{{TABLE}}", "\n".join(lines)).replace("{{FREE}}", free_text))
print(f"wrote {len(lines)} entries to {OUT}")
