"""Exact certificates for the C*-quotient and universal-cubic geometry.

Checks equivariance, invariant quotient formulas, the rim cusp, exact orbit
monodromy loop, the universal depressed cubic, and the descended quotient
fiber/trace form. All arithmetic is symbolic over Q.
"""
import sympy as sp

x, y, z, A, B, C, lam = sp.symbols("x y z A B C lam", nonzero=True)
r, t, u, v, w = sp.symbols("r t u v w")

F = [
    (1 + x*y)**3*z + y**2*(1 + x*y)*(4 + 3*x*y),
    y + 3*x*(1 + x*y)**2*z + 3*x*y**2*(4 + 3*x*y),
    2*x - 3*x**2*y - x**3*z,
]
L = 27*A**2*C**2 - 18*A*B*C + 16*A + B**3*C - B**2
S = 27*A*C**2 - 9*B*C + 8

# Source invariants r=xy, t=x^2z; target invariants u=BC, v=AC^2.
Qu = -(3*r + t - 2)*(9*r**3 + 3*r**2*t + 12*r**2 + 6*r*t + r + 3*t)
Qv = ((r + 1)*(3*r + t - 2)**2
      *(3*r**3 + r**2*t + 4*r**2 + 2*r*t + t))
ell = u**3 - u**2 - 18*u*v + 27*v**2 + 16*v
s = 27*v - 9*u + 8
D = u**3 - 18*u*v + 54*v**2

# 1. Full weighted equivariance.
source_action = {x: x/lam, y: lam*y, z: lam**2*z}
weights = (lam**2, lam, 1/lam)
for component, weight in zip(F, weights):
    assert sp.factor(component.subs(source_action) - weight*component) == 0
print("1. C* equivariance with weights (-1,1,2) -> (2,1,-1)   OK")

# 2. The map descends to the stated polynomial quotient Q(r,t)=(u,v).
source_invariants = {r: x*y, t: x**2*z}
assert sp.expand(F[1]*F[2] - Qu.subs(source_invariants)) == 0
assert sp.expand(F[0]*F[2]**2 - Qv.subs(source_invariants)) == 0
print("2. quotient formulas Q(r,t)=(BC, AC^2) verified exactly       OK")

# 3. The rim and S-wall descend, and the rim is a cusp.
target_chart = {A: v/C**2, B: u/C}
assert sp.cancel((L*C**2).subs(target_chart) - ell) == 0
assert sp.cancel(S.subs(target_chart) - s) == 0
assert sp.expand(s**2 - (4 - 3*u)**3 - 27*ell) == 0
print("3. s^2=(4-3u)^3+27ell; quotient rim is cuspidal             OK")

# 4. The omitted floor orbit maps to the cusp tip.
floor_uv = {u: sp.Rational(4, 3), v: sp.Rational(4, 27)}
assert ell.subs(floor_uv) == 0 and s.subs(floor_uv) == 0
print("4. omitted floor orbit maps to (u,v,s)=(4/3,4/27,0)          OK")

# 5. Exact symbolic transposition loop from the rational fiber.
p0 = (0, 0, -sp.Rational(1, 4))
pplus = (1, -sp.Rational(3, 2), sp.Rational(13, 2))
pminus = (-1, sp.Rational(3, 2), sp.Rational(13, 2))
target0 = (-sp.Rational(1, 4), 0, 0)
for point in (p0, pplus, pminus):
    image = tuple(sp.expand(f.subs(dict(zip((x, y, z), point)))) for f in F)
    assert image == target0
action_at_minus_one = lambda point: (-point[0], -point[1], point[2])
assert action_at_minus_one(p0) == p0
assert action_at_minus_one(pplus) == pminus
assert action_at_minus_one(pminus) == pplus
assert sp.expand(L.subs({A: lam**2*A, B: lam*B, C: C/lam}) - lam**2*L) == 0
print("5. exact C* orbit loop swaps the rational +/- sheets          OK")

# 6. Original fiber is the universal depressed cubic after monic scaling.
P = (4 - 3*B*C)*L
Q = -2*C*L**2
assert sp.expand(4*P**3 + 27*Q**2 - 4*L**3*S**2) == 0
print("6. universal cubic identity 4P^3+27Q^2=4L^3S^2             OK")

# 7. Quotient fibers have their own depressed cubic in w=r+1.
K = sp.QQ.frac_field(u, v)
gb = sp.groebner([sp.expand(Qu-u), sp.expand(Qv-v)], t, r,
                 order="lex", domain=K)
g1, g2 = gb.exprs
quotient_fiber = ell*w**3 + (u**2 - 12*v)*w - 4*v
assert sp.cancel(g2 - quotient_fiber.subs(w, r+1)/ell) == 0
assert sp.expand(D**2 - (u**2 - 12*v)**3 - 108*ell*v**2) == 0
quotient_disc = sp.factor(sp.discriminant(quotient_fiber, w))
assert sp.expand(quotient_disc + 4*ell*D**2) == 0
print("7. quotient fiber: ell*w^3+(u^2-12v)w-4v; disc=-4ell D^2 OK")

# The lexicographic basis also reconstructs t rationally away from D=0.
t_reconstruction = sp.factor(sp.cancel(t - g1))
assert not t_reconstruction.has(t)
assert sp.expand(sp.denom(t_reconstruction) - 2*D) == 0

# 8. Trace determinant in the quotient power basis {1,r,r^2}.
quotient_monic = sp.Poly(g2, r, domain=K).monic()

def reduce_quotient(expr):
    return sp.rem(sp.Poly(sp.cancel(expr), r, domain=K), quotient_monic).as_expr()

def quotient_trace(expr):
    h = reduce_quotient(expr)
    columns = []
    for basis_element in (1, r, r**2):
        product = sp.Poly(reduce_quotient(h*basis_element), r, domain=K)
        columns.append([product.nth(i) for i in range(3)])
    matrix = sp.Matrix(3, 3, lambda i, j: columns[j][i])
    return sp.factor(sp.trace(matrix))

trace_form = sp.Matrix(3, 3,
                       lambda i, j: quotient_trace(r**(i+j)))
trace_det = sp.factor(sp.cancel(trace_form.det()))
assert trace_det == -4*D**2/ell**3
assert sp.cancel(trace_det - sp.discriminant(quotient_monic.as_expr(), r)) == 0
print("8. quotient trace determinant = -4D^2/ell^3                     OK")
print("DONE — quotient cusp, cubic, monodromy, and trace form certified.")
