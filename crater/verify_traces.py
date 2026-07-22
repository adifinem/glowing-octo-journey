"""Exact trace identities for the generic three-point fiber of the Alpoge map.

The trace of a fiber function is computed as the matrix trace of multiplication
in K[x]/(fiber cubic), where K = Q(A,B,C), after shape-position reconstruction.
"""
import sympy as sp

x, y, z, A, B, C = sp.symbols("x y z A B C")
F = [
    (1 + x*y)**3*z + y**2*(1 + x*y)*(4 + 3*x*y),
    y + 3*x*(1 + x*y)**2*z + 3*x*y**2*(4 + 3*x*y),
    2*x - 3*x**2*y - x**3*z,
]
L = 27*A**2*C**2 - 18*A*B*C + 16*A + B**3*C - B**2
S = 27*A*C**2 - 9*B*C + 8
K = sp.QQ.frac_field(A, B, C)

eqs = [sp.expand(f - t) for f, t in zip(F, (A, B, C))]
g1, g2, g3 = sp.groebner(eqs, y, z, x, order="lex", domain=K).exprs
p = sp.together(y - g1)
q = sp.together(z - g2)
fiber = sp.Poly(L*x**3 + (4 - 3*B*C)*x - 2*C, x, domain=K).monic()


def reduce_fiber(expr):
    """Return the degree-at-most-two representative in the generic fiber algebra."""
    return sp.rem(sp.Poly(sp.cancel(expr), x, domain=K), fiber).as_expr()


def fiber_trace(expr):
    """Trace of multiplication by expr on the generic rank-three fiber algebra."""
    h = reduce_fiber(expr)
    columns = []
    for basis_element in (1, x, x**2):
        product = sp.Poly(reduce_fiber(h*basis_element), x, domain=K)
        columns.append([product.nth(i) for i in range(3)])
    multiplication = sp.Matrix(3, 3, lambda i, j: columns[j][i])
    return sp.factor(sp.cancel(sp.trace(multiplication)))


traces = {
    "1": fiber_trace(1),
    "x": fiber_trace(x),
    "y": fiber_trace(p),
    "z": fiber_trace(q),
    "x^2": fiber_trace(x**2),
    "xy": fiber_trace(x*p),
    "xz": fiber_trace(x*q),
    "y^2": fiber_trace(p**2),
    "yz": fiber_trace(p*q),
    "z^2": fiber_trace(q**2),
}

assert traces["1"] == 3
assert traces["x"] == 0
assert sp.cancel(traces["y"] - 3*B/2) == 0
assert sp.cancel(traces["z"] + 3*(108*A**2*C**2 - 72*A*B*C + 136*A
                                  - 5*B**3*C + 2*B**2)/8) == 0
assert sp.cancel(traces["x^2"] - 2*(3*B*C - 4)/L) == 0
assert traces["xy"] == -3
assert sp.cancel(traces["xz"] + 3*B*(3*B*C + 2)/4) == 0
assert sp.cancel(traces["y^2"] + 9*(8*A - B**2)/4) == 0

# Every coordinate trace through degree two is polynomial except Tr(x^2).
polynomial_traces = ("1", "x", "y", "z", "xy", "xz", "y^2", "yz", "z^2")
for name in polynomial_traces:
    denominator = sp.Poly(sp.denom(traces[name]), A, B, C)
    assert denominator.total_degree() == 0
assert sp.factor(sp.denom(traces["x^2"])) == L

# The trace-pairing determinant in the x-power basis is the discriminant of the
# monic fiber cubic. Its S^2 zero records failure of x to separate the sheets
# on the S-wall; its L^-3 pole records the pair of sheets escaping at the rim.
power_basis = (1, x, x**2)
trace_form = sp.Matrix(3, 3, lambda i, j: fiber_trace(power_basis[i]*power_basis[j]))
assert sp.factor(sp.det(trace_form)) == -4*S**2/L**3

# Change the primitive element from x to y. The intrinsic square class remains
# -L, but the even projection divisor migrates from S^2 to A^2 and the x-lattice
# poles disappear. This machine-checks that only divisor parity is basis-free.
y_power_basis = (1, p, reduce_fiber(p**2))
y_change = sp.Matrix(
    3, 3,
    lambda i, j: sp.Poly(reduce_fiber(y_power_basis[j]), x, domain=K).nth(i),
)
y_trace_form = sp.Matrix(
    3, 3, lambda i, j: fiber_trace(y_power_basis[i]*y_power_basis[j])
)
assert sp.cancel(sp.det(y_change) - 27*A*L**2/(4*S)) == 0
assert sp.cancel(sp.det(y_trace_form) + 729*A**2*L/4) == 0
assert sp.cancel(sp.det(y_trace_form) - sp.det(trace_form)*sp.det(y_change)**2) == 0

print("Generic fiber traces through coordinate degree two:")
for name, value in traces.items():
    print(f"  Tr({name}) = {value}")
print("\nPolynomial through degree two except Tr(x^2):              OK")
print("Tr(x^2) = 2(3BC-4)/L exposes the escaping second moment: OK")
print("det trace form in x-basis = -4*S^2/L^3:                 OK")
print("det trace form in y-basis = -729*A^2*L/4:                OK")
print("DONE — fiber centroid, moments, and trace-form parity certified.")
