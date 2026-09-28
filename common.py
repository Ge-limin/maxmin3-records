"""Shared pieces: the objective, the local optimiser and the bests/ store.

Problem: n points in R^3 minimising (max distance / min distance)^2.
Formulation for the local optimiser: variables x (n*3) and t;
minimise t subject to 1 <= |xi - xj|^2 <= t. SLSQP with exact Jacobian.
"""
import os
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
BESTS = os.path.join(HERE, "bests")


def ratio2(X):
    D = X[:, None, :] - X[None, :, :]
    s = (D * D).sum(-1)[np.triu_indices(len(X), 1)]
    return s.max() / s.min()


class Polisher:
    def __init__(self, n):
        self.n = n
        self.I, self.J = np.triu_indices(n, 1)
        self.m = len(self.I)
        self.grad = np.eye(1, 3 * n + 1, 3 * n)[0]

    def _d2(self, z):
        X = z[:-1].reshape(self.n, 3)
        D = X[self.I] - X[self.J]
        return (D * D).sum(1), D

    def _cons(self, z):
        s, _ = self._d2(z)
        return np.concatenate([s - 1.0, z[-1] - s])

    def _jac(self, z):
        n, m, I, J = self.n, self.m, self.I, self.J
        _, D = self._d2(z)
        Jm = np.zeros((2 * m, 3 * n + 1))
        rows = np.arange(m)
        for k in range(3):
            Jm[rows, 3 * I + k] = 2 * D[:, k]
            Jm[rows, 3 * J + k] = -2 * D[:, k]
        Jm[m:, :-1] = -Jm[:m, :-1]
        Jm[m:, -1] = 1.0
        return Jm

    def __call__(self, X, maxiter=3000):
        D = X[:, None] - X[None]
        s = (D * D).sum(-1)[np.triu_indices(self.n, 1)]
        X = X / np.sqrt(s.min())
        z0 = np.concatenate([X.ravel(), [s.max() / s.min()]])
        res = minimize(lambda z: z[-1], z0, jac=lambda z: self.grad,
                       constraints=[{"type": "ineq", "fun": self._cons, "jac": self._jac}],
                       method="SLSQP", options={"maxiter": maxiter, "ftol": 1e-15})
        X = res.x[:-1].reshape(self.n, 3)
        return X, ratio2(X)


def load_best(n):
    path = os.path.join(BESTS, f"n{n}.npy")
    return np.load(path) if os.path.exists(path) else None


def offer_best(X, tag):
    """Replace bests/n{n}.npy only if X is strictly better. Safe across workers."""
    n = len(X)
    tmp = os.path.join(BESTS, f".n{n}_{tag}_{os.getpid()}.npy")
    np.save(tmp, X)
    cur = load_best(n)
    if cur is None or ratio2(X) < ratio2(cur) * (1 - 1e-12):
        os.replace(tmp, os.path.join(BESTS, f"n{n}.npy"))
        return True
    os.remove(tmp)
    return False
