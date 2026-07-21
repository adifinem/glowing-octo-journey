"""Machine verification for fiber_structure.md: the discriminant
factorization disc = -4*L*S^2, the floor curve as {L=0} n {S=0}, the
shape-position Groebner basis with S in the denominators, and the S-wall
sample fiber. Exact arithmetic; every claim ends in an assert.

Run: python3 verify_shape.py   (sympy; a few minutes — the Groebner basis
over Q(A,B,C) is the slow step)
"""
import sympy as sp

x, y, z, A, B, C = sp.symbols('x y z A B C')
F = [(1 + x*y)**3 * z + y**2 * (1 + x*y) * (4 + 3*x*y),
     y + 3*x*(1 + x*y)**2 * z + 3*x*y**2 * (4 + 3*x*y),
     2*x - 3*x**2*y - x**3*z]

L = 27*A**2*C**2 - 18*A*B*C + 16*A + B**3*C - B**2
S = 27*A*C**2 - 9*B*C + 8

# -- 1. disc(L x^3 + (4-3BC) x - 2C) = -4 L S^2 -------------------------------
disc = sp.expand(-4*L*(4 - 3*B*C)**3 - 108*L**2*C**2)
assert sp.expand(disc + 4*L*S**2) == 0
print("1. disc = -4*L*S^2 identically                            OK")

# -- 2. {L=0} n {S=0} = the floor curve ---------------------------------------
b = sp.Symbol('b')
floor = {A: b**2/12, B: b, C: sp.Rational(4, 3)/b}
assert sp.simplify(L.subs(floor)) == 0 and sp.simplify(S.subs(floor)) == 0
Asol = sp.solve(sp.Eq(S, 0), A)[0]
assert sp.simplify(L.subs(A, Asol) - (3*B*C - 4)**3/(27*C**2)) == 0
print("2. floor curve = {L=0} n {S=0} exactly                    OK")

# -- 3. shape position over Q(A,B,C); denominators are S ----------------------
eqs = [sp.expand(f - t) for f, t in zip(F, (A, B, C))]
dom = sp.QQ.frac_field(A, B, C)
gb = sp.groebner(eqs, y, z, x, order='lex', domain=dom)
g1, g2, g3 = gb.exprs
p, q = sp.together(y - g1), sp.together(z - g2)
assert sp.Poly(g1, y, z, x).degree_list() == (1, 0, 2)
assert sp.Poly(g2, y, z, x).degree_list() == (0, 1, 2)
cubic = L*x**3 + (4 - 3*B*C)*x - 2*C
assert sp.simplify(sp.together(g3 - cubic/L)) == 0 or \
       sp.expand(sp.numer(sp.together(g3)) * L
                 - sp.denom(sp.together(g3)) * cubic) == 0
assert sp.expand(sp.denom(sp.factor(sp.together(p))) - 2*S) == 0
assert sp.expand(sp.denom(sp.factor(sp.together(q))) - 8*S) == 0
print("3. shape position {y-p(x), z-q(x), cubic}; denoms 2S, 8S  OK")

# -- 4. certificate: the parametrization satisfies the fiber equations --------
num_cubic = sp.expand(sp.numer(sp.together(g3)))
for e in eqs:
    n = sp.expand(sp.numer(sp.together(e.subs({y: p, z: q}))))
    assert sp.rem(sp.Poly(n, x, domain=dom),
                  sp.Poly(num_cubic, x, domain=dom)).is_zero
print("4. y=p(x), z=q(x) satisfy all equations mod the cubic     OK")

# -- 5. the S-wall sample: 3 preimages, two sharing an x-coordinate -----------
tgt = [sp.Rational(-8, 27), 0, 1]
assert S.subs(dict(zip((A, B, C), tgt))) == 0
fc = sp.factor(cubic.subs(dict(zip((A, B, C), tgt))))
sols = sp.solve([sp.Eq(f, t) for f, t in zip(F, tgt)], [x, y, z], dict=True)
assert len(sols) == 3
xs = sorted(sp.nsimplify(s[x]) for s in sols)
assert xs == [sp.Rational(-3, 2), sp.Rational(3, 4), sp.Rational(3, 4)]
for s in sols:                                        # all real
    assert all(abs(sp.im(sp.N(v, 40))) < sp.Float(10)**-30 for v in s.values())
print("5. S-wall fiber: 3 real preimages, two sharing x = 3/4    OK")

print("DONE — fiber structure theorem verified.")
