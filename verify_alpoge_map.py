"""The napkin check: verify Alpoge's counterexample to the Jacobian Conjecture.

Two facts, exact arithmetic, ~1 minute:
  1. The map F below has Jacobian determinant identically -2.
  2. F is not injective: one rational target, three exact preimages,
     each confirmed by substitution.
A polynomial self-map of C^3 with constant nonzero Jacobian that is not
injective refutes the Jacobian Conjecture for n = 3, hence (padding with
identity coordinates) for every n >= 3.

Map announced by L. Alpoge, 2026-07-19, credited to work with Claude Fable.
Run: python3 verify_alpoge_map.py   (needs sympy)
"""
import sympy as sp

x, y, z = sp.symbols('x y z')

F = [(1 + x*y)**3 * z + y**2 * (1 + x*y) * (4 + 3*x*y),
     y + 3*x*(1 + x*y)**2 * z + 3*x*y**2 * (4 + 3*x*y),
     2*x - 3*x**2*y - x**3*z]

# 1. Constant Jacobian
det = sp.Matrix([F]).jacobian([x, y, z]).det()
assert sp.expand(det) == -2
print("Jacobian determinant == -2 identically:      OK")

# 2. Three exact preimages of (329/270, 19/10, 7/10)
target = [sp.Rational(329, 270), sp.Rational(19, 10), sp.Rational(7, 10)]
s31, I = sp.sqrt(31), sp.I
preimages = [(sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 5))]
for sgn in (+1, -1):
    preimages.append((sp.Rational(-1, 4) + sgn*29*s31*I/372,
                      sp.Rational(151, 120) + sgn*21*s31*I/40,
                      sp.Rational(-3356649, 160000) + sgn*636423*s31*I/160000))
assert len(set(preimages)) == 3
for p in preimages:
    image = [sp.simplify(f.subs(dict(zip((x, y, z), p)))) for f in F]
    assert image == target, (p, image)
print("3 distinct exact preimages of one point:     OK")

print("\nThe Jacobian Conjecture is false for all n >= 3.")
