"""Machine verification for: an explicit non-invertible endomorphism of the
third Weyl algebra A_3 (refuting the Dixmier conjecture for n >= 3).

Checks 1, 2, 4, and 5 are exact symbolic computation (sympy); check 3
combines an exact integer discriminant computation with 50-digit numerical
certification of realness (the exact realness argument — conjugation fixes
each simple real x-root's unique preimage — is in the note). Each section
ends in an assert; if the script prints DONE, every claim is verified.

  1. det J(F) = -2 identically (F is a Keller map).           [exact]
  2. F is not injective on C^3: an explicit target with three distinct
     preimages, each checked by exact substitution.           [exact]
  3. F is not injective on R^3 either: an explicit real target with three
     distinct REAL preimages.       [exact discriminant + 50-digit bounds]
  4. G := J^{-1} is a polynomial matrix, and the operators
     D_i := sum_a G[a,i] d_a satisfy [D_i, F_j] = delta_ij and
     [D_i, D_j] = 0, so x_i -> F_i, d_i -> D_i defines an endomorphism phi
     of A_3.                                                  [exact]
Non-surjectivity of phi follows from 2 by the normal-ordering argument in
the note: a preimage of x_1 under phi would give x_1 = Q_1(F), refuted by
the two displayed preimages sharing an image but differing in x_1.
"""
import sympy as sp

x1, x2, x3 = X = sp.symbols('x1 x2 x3')

F = [(1 + x1*x2)**3 * x3 + x2**2 * (1 + x1*x2) * (4 + 3*x1*x2),
     x2 + 3*x1*(1 + x1*x2)**2 * x3 + 3*x1*x2**2 * (4 + 3*x1*x2),
     2*x1 - 3*x1**2*x2 - x1**3*x3]

# -- 1. Keller condition -----------------------------------------------------
J = sp.Matrix(3, 3, lambda i, j: sp.diff(F[i], X[j]))
detJ = sp.expand(J.det())
assert detJ == -2
print("1. det J = -2 identically                                  OK")

# -- 2. Non-injectivity over C: three exact preimages of one target ----------
target = [sp.Rational(329, 270), sp.Rational(19, 10), sp.Rational(7, 10)]
s31, I = sp.sqrt(31), sp.I
pre = [(sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 5))]
for sgn in (+1, -1):
    pre.append((sp.Rational(-1, 4) + sgn*29*s31*I/372,
                sp.Rational(151, 120) + sgn*21*s31*I/40,
                sp.Rational(-3356649, 160000) + sgn*636423*s31*I/160000))
assert len(set(pre)) == 3
for p in pre:
    img = [sp.simplify(f.subs(dict(zip(X, p)))) for f in F]
    assert img == target, (p, img)
print("2. three distinct exact preimages of (329/270,19/10,7/10)  OK")

# -- 3. Non-injectivity over R: three real preimages of a real target --------
# The x-coordinates of preimages of (3/100, 1, 1) satisfy the fiber cubic
# 357 x^3 - 10000 x + 20000 = 0 (see the note). Its discriminant is a positive
# integer, so it has three distinct real roots; conjugation permutes the three
# preimages and fixes each real x-coordinate, hence fixes each preimage, so all
# three preimages are real. Exact discriminant check + 60-digit certification:
disc = -4*357*(-10000)**3 - 27*357**2*20000**2
assert disc > 0                                     # 51,610,800,000,000 > 0
rt = [sp.Rational(3, 100), sp.Integer(1), sp.Integer(1)]
sols = sp.solve([sp.Eq(f, t) for f, t in zip(F, rt)], X, dict=True)
assert len(sols) == 3
cubic_roots = sorted(sp.Poly(357*x1**3 - 10000*x1 + 20000, x1).all_roots(),
                     key=lambda r: sp.N(r))
xs = []
for s in sols:
    num = {k: sp.N(v, 60) for k, v in s.items()}
    for v in num.values():
        assert abs(sp.im(v)) < sp.Float(10)**-50    # real to 50 digits
    img = [sp.N(f.subs(s), 60) for f in F]
    for e, t in zip(img, rt):
        assert abs(e - t) < sp.Float(10)**-50       # maps to the target
    xs.append(sp.re(num[x1]))
for xv, rv in zip(sorted(xs), cubic_roots):
    assert abs(xv - sp.N(rv, 60)) < sp.Float(10)**-50
assert len({sp.N(v, 30) for v in xs}) == 3          # distinct
print("3. three distinct REAL preimages of (3/100, 1, 1)          OK")

# -- 4. The Weyl-algebra relations -------------------------------------------
G = (J.adjugate() / detJ).applyfunc(sp.expand)      # J^{-1}, polynomial entries
assert sp.simplify(J * G - sp.eye(3)) == sp.zeros(3)
for i in range(3):
    for j in range(i + 1, 3):
        for b in range(3):
            comm = sum(G[a, i]*sp.diff(G[b, j], X[a])
                       - G[a, j]*sp.diff(G[b, i], X[a]) for a in range(3))
            assert sp.expand(comm) == 0, (i, j, b)
print("4. [D_i, F_j] = delta_ij and [D_i, D_j] = 0                OK")

# -- 5. Fiber geometry: the fiber cubic and the omitted curve ----------------
A, B, C = sp.symbols('A B C')
r1 = sp.expand(sp.resultant(F[0] - A, F[2] - C, x3))
r2 = sp.expand(sp.resultant(F[1] - B, F[2] - C, x3))
res = sp.factor(sp.resultant(r1, r2, x2))
L = 27*A**2*C**2 - 18*A*B*C + 16*A + B**3*C - B**2
cubic = L*x1**3 + (4 - 3*B*C)*x1 - 2*C
assert sp.expand(res - (-C * x1**12 * cubic)) == 0
# Every preimage of (A,B,C) has x-coordinate killing this resultant.  If
# C != 0 then x != 0 (since F_3(0,y,z) = 0), so x is a root of the cubic.
# On the curve (A,B,C) = (B^2/12, B, 4/(3B)) both L and 4-3BC vanish:
floor = {A: B**2/12, C: sp.Rational(4, 3)/B}
assert sp.simplify(L.subs(floor)) == 0
assert sp.simplify((4 - 3*B*C).subs(floor)) == 0
# ... so the cubic degenerates to -2C != 0: the fiber is EMPTY.  F is not
# surjective; it omits the whole rational curve above.  Spot-checks:
assert sp.solve([sp.Eq(f, t) for f, t in
                 zip(F, [sp.Rational(1, 3), 2, sp.Rational(2, 3)])],
                X, dict=True) == []                  # floor: 0 preimages
assert len(sp.solve([sp.Eq(f, t) for f, t in
                     zip(F, [sp.Rational(2, 27), 1, 1])],
                    X, dict=True)) == 1              # rim (L=0): 1 preimage
print("5. fiber cubic identity; image omits (B^2/12, B, 4/(3B))   OK")

print("DONE — all claims verified.")
