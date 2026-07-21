"""Machine verification: an explicit SYMMETRIC (gradient) Keller counterexample
to the Jacobian Conjecture in dimension 6.

Construction: normalize the Alpoge map to Ft = A^{-1} F (A = JF(0)), write
H = Ft - id, and set

    P(x, y) = (1/2) < x - iy, H(x + iy) >      (degree 8, in C^6)

Then G = z + grad P is a Keller map (det(I + Hess P) = 1) whose Hessian is
symmetric by construction, and G is NOT injective. Proof mechanism: in the
coordinates w = x + iy, wbar = x - iy the map G becomes block-triangular,

    G ~ ( w + H(w),  wbar + JH(w)^T wbar ),

so its Jacobian is similar to [[I+JH, 0], [*, I+JH^T]]: the Keller property
follows from det(I + JH) = 1, and double points of Ft lift to double points
of G along wbar = 0.

Checks (exact symbolic computation, each ends in an assert):
  1. H has order >= 2 (so G = z + grad P has identity linear part).
  2. det(I3 + JH) = 1 identically.
  3. The block identity above, as polynomial identities in C[x, y].
     (With 2 and triangularity this gives det(I6 + Hess P) = 1 identically.)
  4. Hess P is symmetric; det(I6 + Hess P) = 1 at random rational points.
  5. Two distinct explicit points of C^6 with the same image under G.
  6. Hess P is NOT nilpotent (char poly of JH is not lam^3): this P is a
     symmetric counterexample but not a Hessian-nilpotent one; producing a
     homogeneous Hessian-nilpotent example (a counterexample to Zhao's
     Vanishing Conjecture) additionally requires the Bass-Connell-Wright
     cubic-homogeneous reduction. See symmetric_note.md.

Run: python3 verify_symmetric.py   (sympy; a few minutes)
"""
import sympy as sp
import random

x1, x2, x3, y1, y2, y3 = V = sp.symbols('x1 x2 x3 y1 y2 y3')
X, Y = [x1, x2, x3], [y1, y2, y3]
I = sp.I

Fmap = [(1 + x1*x2)**3 * x3 + x2**2 * (1 + x1*x2) * (4 + 3*x1*x2),
        x2 + 3*x1*(1 + x1*x2)**2 * x3 + 3*x1*x2**2 * (4 + 3*x1*x2),
        2*x1 - 3*x1**2*x2 - x1**3*x3]

# -- 1. normalize ------------------------------------------------------------
JF = sp.Matrix(3, 3, lambda i, j: sp.diff(Fmap[i], X[j]))
A = JF.subs({v: 0 for v in X})
Ft = list(A.inv() * sp.Matrix(Fmap))
H = [sp.expand(Ft[k] - X[k]) for k in range(3)]
for h in H:
    assert h.subs({v: 0 for v in X}) == 0
assert sp.Matrix(3, 3, lambda i, j: sp.diff(H[i], X[j])).subs(
    {v: 0 for v in X}) == sp.zeros(3)
print("1. H = A^{-1}F - id has order >= 2                       OK")

# -- 2. Keller in dimension 3 ------------------------------------------------
JH = sp.Matrix(3, 3, lambda i, j: sp.diff(H[i], X[j]))
assert sp.expand((sp.eye(3) + JH).det()) == 1
print("2. det(I3 + JH) = 1 identically                          OK")

# -- 3. the potential and the block identity ---------------------------------
w    = [X[k] + I*Y[k] for k in range(3)]
wbar = [X[k] - I*Y[k] for k in range(3)]
Hw = [sp.expand(H[k].subs(dict(zip(X, w)), simultaneous=True)) for k in range(3)]
P = sp.expand(sp.Rational(1, 2) * sum(wbar[k]*Hw[k] for k in range(3)))
assert sp.total_degree(P) == 8
grad = [sp.expand(sp.diff(P, v)) for v in V]
G = [V[k] + grad[k] for k in range(6)]

JHw = sp.Matrix(3, 3, lambda i, j: sp.expand(
    sp.diff(H[i], X[j]).subs(dict(zip(X, w)), simultaneous=True)))
for k in range(3):
    assert sp.expand(G[k] + I*G[3+k] - (w[k] + Hw[k])) == 0
    assert sp.expand(G[k] - I*G[3+k]
                     - (wbar[k] + sum(JHw[j, k]*wbar[j] for j in range(3)))) == 0
print("3. block identity G ~ (w+H(w), wbar+JH(w)^T wbar)        OK")

# -- 4. symmetry and Keller spot checks in dimension 6 ------------------------
Hess = sp.Matrix(6, 6, lambda i, j: sp.diff(P, V[i], V[j]))
assert Hess == Hess.T
random.seed(7)
for _ in range(3):
    pt = {v: sp.Rational(random.randint(-9, 9), random.randint(1, 9)) for v in V}
    assert (sp.eye(6) + Hess.subs(pt)).det() == 1
print("4. Hess P symmetric; det(I+Hess)=1 at 3 random points    OK")

# -- 5. non-injectivity -------------------------------------------------------
s31 = sp.sqrt(31)
p = [sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 5)]
q = [sp.Rational(-1, 4) + 29*s31*I/372,
     sp.Rational(151, 120) + 21*s31*I/40,
     sp.Rational(-3356649, 160000) + 636423*s31*I/160000]

def embed(pt):          # w = pt, wbar = 0  =>  x = pt/2, y = -i pt/2
    return {**{X[k]: pt[k]/2 for k in range(3)},
            **{Y[k]: -I*pt[k]/2 for k in range(3)}}

z1, z2 = embed(p), embed(q)
assert all(sp.expand(g.subs(z1) - g.subs(z2)) == 0 for g in G)
assert any(sp.expand(z1[v] - z2[v]) != 0 for v in V)
print("5. two distinct points, same image under z + grad P      OK")

# -- 6. not Hessian-nilpotent (the remaining opening) --------------------------
lam = sp.Symbol('lam')
cp = sp.expand(JH.charpoly(lam).as_expr())
assert cp != lam**3
assert (JH.subs({x1: 1, x2: 1, x3: 1})**2).trace() != 0
print("6. Hess P not nilpotent (VC needs cubic step first)      OK")

print("DONE — all claims verified.")
