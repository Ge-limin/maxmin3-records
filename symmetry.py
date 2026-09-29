"""Highest-order rotation axis of a configuration, for the page's symmetry note.

Any rotation symmetry axis passes through the centroid and is an axis of
the point set's own structure, so candidates are: inertia eigenvectors,
centroid -> each point, centroid -> midpoint of each min/max-distance pair,
and normals of triangles of min-distance pairs. A k-fold rotation about an
axis is a symmetry if it maps every point to within TOL of some point.
Free points (see report.py) can sit anywhere in their cage, so the note is
computed on the rigid core as well as the full set.

    python symmetry.py bests/n31.npy ...
"""
import sys
import numpy as np

TOL = 1e-4  # in units of the minimum distance


def rot(axis, ang):
    a = axis / np.linalg.norm(axis)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K


def candidate_axes(Y, s, iu):
    cands = list(np.linalg.eigh(Y.T @ Y)[1].T)
    cands += [p for p in Y if np.linalg.norm(p) > 1e-6]
    tight = [(i, j) for i, j, v in zip(*iu, s) if v <= s.min() * (1 + 1e-6) or v >= s.max() * (1 - 1e-6)]
    cands += [(Y[i] + Y[j]) / 2 for i, j in tight]
    near = {}
    for i, j in tight:
        near.setdefault(i, []).append(j)
    for i, js in near.items():
        for a in js:
            for b in js:
                if a < b:
                    cands.append(np.cross(Y[a] - Y[i], Y[b] - Y[i]))
    out = []
    for c in cands:
        nrm = np.linalg.norm(c)
        if nrm < 1e-9:
            continue
        c = c / nrm
        if not any(abs(abs(c @ o) - 1) < 1e-6 for o in out):
            out.append(c)
    return out


def is_symmetric(Y, R, tol):
    Z = Y @ R.T
    d = np.sqrt(((Z[:, None] - Y[None]) ** 2).sum(-1))
    return d.min(1).max() < tol


def max_fold(X):
    n = len(X)
    Y = X - X.mean(0)
    iu = np.triu_indices(n, 1)
    D = Y[:, None] - Y[None]
    s = (D * D).sum(-1)[iu]
    tol = TOL * np.sqrt(s.min())
    best = 1
    for ax in candidate_axes(Y, s, iu):
        for k in range(6, best, -1):
            if is_symmetric(Y, rot(ax, 2 * np.pi / k), tol):
                best = k
                break
    return best


def note(k):
    return "asymmetric" if k == 1 else f"{k}-fold rotational symmetry"


if __name__ == "__main__":
    for path in sys.argv[1:]:
        X = np.load(path)
        print(f"{path}: n={len(X)} {note(max_fold(X))}")
