#!/usr/bin/env python3
"""Exact adversarial benchmark for finite-to-one change of variables.

The Alpöge map has constant nonzero Jacobian determinant, but is globally
many-to-one. For a finite-to-one local diffeomorphism, the pushforward density
at a regular target is a SUM over all inverse branches:

    p_Y(y) = sum_{x in F^{-1}(y)} p_X(x) / |det J_F(x)|.

A solver that returns one valid inverse can therefore be locally correct while
globally wrong. This script uses an exact rational collision fiber to measure
the undercount.

Run:
    python3 local_to_global/flow_branch_benchmark.py

Dependency:
    sympy
"""

from __future__ import annotations

import sympy as sp

x, y, z = sp.symbols("x y z")
X = (x, y, z)

F = (
    (1 + x * y) ** 3 * z + y**2 * (1 + x * y) * (4 + 3 * x * y),
    y + 3 * x * (1 + x * y) ** 2 * z + 3 * x * y**2 * (4 + 3 * x * y),
    2 * x - 3 * x**2 * y - x**3 * z,
)

J = sp.Matrix(F).jacobian(X)
DET_J = sp.expand(J.det())
assert DET_J == -2

# Three distinct rational points with one common image.
PREIMAGES = (
    (sp.Rational(0), sp.Rational(0), sp.Rational(-1, 4)),
    (sp.Rational(1), sp.Rational(-3, 2), sp.Rational(13, 2)),
    (sp.Rational(-1), sp.Rational(3, 2), sp.Rational(13, 2)),
)
TARGET = (sp.Rational(-1, 4), sp.Rational(0), sp.Rational(0))


def image(point: tuple[sp.Expr, sp.Expr, sp.Expr]) -> tuple[sp.Expr, ...]:
    substitutions = dict(zip(X, point))
    return tuple(sp.simplify(component.subs(substitutions)) for component in F)


assert len(set(PREIMAGES)) == 3
assert all(image(point) == TARGET for point in PREIMAGES)

# An unnormalized positive source density with exact rational values at the
# witness points. Normalization is irrelevant because we compare two formulas
# at the same target.
def source_weight(point: tuple[sp.Expr, sp.Expr, sp.Expr]) -> sp.Expr:
    px, py, pz = point
    return sp.Rational(1, 1) / (1 + px**2 + py**2 + pz**2)


branch_terms = tuple(sp.simplify(source_weight(point) / abs(DET_J)) for point in PREIMAGES)
correct_pushforward = sp.simplify(sum(branch_terms))
one_branch_estimate = branch_terms[0]
undercount_factor = sp.simplify(correct_pushforward / one_branch_estimate)
missing_mass_fraction = sp.simplify(1 - one_branch_estimate / correct_pushforward)

print("Alpöge finite-to-one density benchmark")
print("=======================================")
print(f"det J_F: {DET_J}")
print(f"target:  {TARGET}")
print("\nExact inverse branches and contributions:")
for index, (point, term) in enumerate(zip(PREIMAGES, branch_terms), start=1):
    print(f"  branch {index}: x = {point}")
    print(f"            p_X(x)/|det J| = {term} ~= {sp.N(term, 12)}")

print("\nPushforward comparison:")
print(f"  correct branch sum: {correct_pushforward} ~= {sp.N(correct_pushforward, 12)}")
print(f"  one-root estimate:  {one_branch_estimate} ~= {sp.N(one_branch_estimate, 12)}")
print(f"  undercount factor:  {undercount_factor} ~= {sp.N(undercount_factor, 12)}")
print(f"  missing fraction:   {missing_mass_fraction} ~= {sp.N(missing_mass_fraction, 12)}")

assert correct_pushforward > one_branch_estimate
assert undercount_factor > 1
assert 0 < missing_mass_fraction < 1

print("\nPASS: constant local volume scaling did not imply a globally valid")
print("      one-branch change-of-variables formula.")
