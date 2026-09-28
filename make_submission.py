"""Build the submission package for n=31..50 in out/.

For every n: out/mmN.gif (Friedman-style picture) and out/coords_nN.txt
(the exact grid coordinates the claimed value was computed from), plus
out/email.md with the value table filled in. The email still needs the
submitter's full name; nothing is sent from here.

    python make_submission.py
"""
import os
import numpy as np
from common import load_best
from render import render
from verify import SCALE, claim, exact_ratio2, grid_points

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
lines = []
for n in range(31, 51):
    X = load_best(n)
    if X is None:
        print(f"n={n}: missing")
        continue
    P = grid_points(X.tolist())
    r = exact_ratio2(P)
    with open(os.path.join(OUT, f"coords_n{n}.txt"), "w") as f:
        f.write(f"# n={n}, 3D, r^2 = max/min squared distance = {r.numerator}/{r.denominator}\n")
        f.write(f"# coordinates are integers / {SCALE}\n")
        for p in P:
            f.write(" ".join(f"{c / SCALE:.12f}" for c in p) + "\n")
    Xg = np.array(P, dtype=float) / SCALE
    nmin, nmax = render(Xg, os.path.join(OUT, f"mm{n}.gif"))
    lines.append(f"{n}. r^2 = {claim(r)}")
    print(f"n={n}: r^2 <= {claim(r)}  ({nmin} min pairs, {nmax} max pairs)")

draft = open(os.path.join(os.path.dirname(OUT), "email_template.md")).read()
with open(os.path.join(OUT, "email.md"), "w") as f:
    f.write(draft.replace("{{TABLE}}", "\n".join(lines)))
print(f"wrote {len(lines)} entries to {OUT}")
