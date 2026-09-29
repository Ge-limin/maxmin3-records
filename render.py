"""Draw a configuration in the style of Friedman's maxmin3 pictures.

White background, minimum-distance pairs as cyan rods, maximum-distance
pairs as red rods, points as small dark balls, painter's-order depth.
The view is the rotation (from a fixed random sample) that spreads the
projected points the most, so the picture is reproducible.

    python render.py bests/n31.npy out/mm31.gif
"""
import sys
import numpy as np
from PIL import Image, ImageDraw

SIZE = 250          # longest side; the reference pictures are 215-279 px
SS = 4              # supersampling factor
CYAN = np.array([0, 230, 230])
RED = np.array([235, 10, 0])
BALL = np.array([40, 60, 60])
TOL = 1e-6


def rotations(k, seed=0):
    rng = np.random.default_rng(seed)
    for _ in range(k):
        q = rng.normal(size=4)
        a, b, c, d = q / np.linalg.norm(q)
        yield np.array([
            [a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
            [2*(b*c+a*d), a*a-b*b+c*c-d*d, 2*(c*d-a*b)],
            [2*(b*d-a*c), 2*(c*d+a*b), a*a-b*b-c*c+d*d]])


def best_view(X):
    X = X - X.mean(0)

    def spread(R):
        P = (X @ R.T)[:, :2]
        D = P[:, None] - P[None]
        return (D * D).sum(-1)[np.triu_indices(len(X), 1)].min()
    return max(rotations(400), key=spread)


def shade(color, t):
    """t in [0,1]: 0 = far (darker), 1 = near."""
    return tuple(int(v) for v in color * (0.7 + 0.3 * t))


def render(X, path):
    n = len(X)
    Y = (X - X.mean(0)) @ best_view(X).T
    D = Y[:, None] - Y[None]
    s = (D * D).sum(-1)
    iu = np.triu_indices(n, 1)
    dmin, dmax = s[iu].min(), s[iu].max()
    edges = []
    for i, j in zip(*iu):
        if s[i, j] <= dmin * (1 + TOL):
            edges.append((i, j, CYAN))
        elif s[i, j] >= dmax * (1 - TOL):
            edges.append((i, j, RED))

    W = SIZE * SS
    xy = Y[:, :2]
    lo, hi = xy.min(0), xy.max(0)
    scale = (W * 0.9) / (hi - lo).max()
    P = (xy - (lo + hi) / 2) * scale * np.array([1, -1]) + W / 2
    z = Y[:, 2]
    zt = (z - z.min()) / (np.ptp(z) or 1)

    img = Image.new("RGB", (W, W), "white")
    g = ImageDraw.Draw(img)
    items = [((zt[i] + zt[j]) / 2, "e", (i, j, c)) for i, j, c in edges]
    items += [(zt[i] + 1e-3, "p", i) for i in range(n)]
    rod = 1.7 * SS
    for depth, kind, it in sorted(items, key=lambda t: t[0]):
        if kind == "e":
            i, j, c = it
            a, b = tuple(P[i]), tuple(P[j])
            g.line([a, b], fill=shade(c * 0.6, depth), width=int(rod * 1.6))
            g.line([a, b], fill=shade(c, depth), width=int(rod))
        else:
            x, y = P[it]
            r = 2.6 * SS
            g.ellipse([x - r, y - r, x + r, y + r], fill=shade(BALL, depth))
    # crop tight like the page's pictures (drawing touches all four edges)
    bbox = Image.eval(img.convert("L"), lambda v: 255 if v < 250 else 0).getbbox()
    img = img.crop(bbox)
    w, h = img.size
    f = SIZE / max(w, h)
    img = img.resize((max(1, round(w * f)), max(1, round(h * f))), Image.LANCZOS)
    img.convert("P", palette=Image.ADAPTIVE, colors=64).save(path)
    return sum(1 for e in edges if e[2] is CYAN), sum(1 for e in edges if e[2] is RED)


if __name__ == "__main__":
    X = np.load(sys.argv[1])
    nmin, nmax = render(X, sys.argv[2])
    print(f"{sys.argv[2]}: n={len(X)}, {nmin} min-distance rods, {nmax} max-distance rods")
