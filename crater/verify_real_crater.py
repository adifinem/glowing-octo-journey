"""Machine verification for the real-crater classification (real_crater.md).

For a real target (A,B,C) with C != 0, the x-coordinates of preimages solve
L x^3 + (4-3BC) x - 2C = 0. Real x-roots correspond to real preimages (a
simple fiber point fixed by complex conjugation is real), so with a full
3-point fiber the number of REAL preimages is governed by the cubic's
discriminant

    disc = -4 L (4-3BC)^3 - 108 L^2 C^2 :   3 real if disc > 0,
                                            1 real if disc < 0.

This script asserts that classification at sample targets in both regions,
with varied signs of L, B, C — each fiber computed exactly from the original
map, realness certified to 30 digits.

Run: python3 verify_real_crater.py   (sympy; a few minutes)
"""
import sympy as sp

x, y, z, A, B, C = sp.symbols('x y z A B C')
F = [(1 + x*y)**3 * z + y**2 * (1 + x*y) * (4 + 3*x*y),
     y + 3*x*(1 + x*y)**2 * z + 3*x*y**2 * (4 + 3*x*y),
     2*x - 3*x**2*y - x**3*z]

L = 27*A**2*C**2 - 18*A*B*C + 16*A + B**3*C - B**2
disc = sp.expand(-4*L*(4 - 3*B*C)**3 - 108*L**2*C**2)

targets = [(sp.Rational(3, 100), 1, 1),
           (sp.Rational(1, 3), 2, sp.Rational(7, 10)),
           (sp.Rational(-1, 2), 1, 1),
           (2, 1, 1),
           (sp.Rational(1, 10), sp.Rational(1, 2), -1),
           (-1, -1, sp.Rational(1, 2))]

for pt in targets:
    dv = disc.subs(dict(zip((A, B, C), pt)))
    assert dv != 0
    sols = sp.solve([sp.Eq(f, t) for f, t in zip(F, pt)], [x, y, z], dict=True)
    assert len(sols) == 3                      # full fiber
    nreal = sum(1 for s in sols
                if all(abs(sp.im(sp.N(v, 40))) < sp.Float(10)**-30
                       for v in s.values()))
    expected = 3 if dv > 0 else 1
    assert nreal == expected, (pt, dv, nreal)
    print(f"target {tuple(map(str, pt))}: sign(disc)={'+' if dv > 0 else '-'}"
          f" -> {nreal} real preimage(s)   OK")

print("DONE — real-crater classification verified at all samples.")
