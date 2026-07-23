#!/usr/bin/env python3
"""Fail-closed exact validator for the frozen cert_B sham."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
STIMULI = ROOT / 'stimuli.json'


def _fraction(value: str) -> sp.Rational:
    f = Fraction(str(value))
    return sp.Rational(f.numerator, f.denominator)


def validate() -> dict:
    stimuli = json.loads(STIMULI.read_text())
    genuine = stimuli['certificates']['cert_A']
    sham = stimuli['certificates']['cert_B']
    x, y, z = sp.symbols('x y z')
    variables = (x, y, z)
    expressions = tuple(sp.sympify(e) for e in sham['map'])
    points = [tuple(_fraction(v) for v in p) for p in sham['points']]
    claimed = tuple(_fraction(v) for v in sham['claimed_common_image'])

    determinant = sp.factor(sp.Matrix(expressions).jacobian(variables).det())
    images = [
        tuple(sp.factor(e.subs(dict(zip(variables, p)))) for e in expressions)
        for p in points
    ]

    # Independent structural witness: cert_B is L(a,b,c+1/4)+q, where the
    # triangular map (x,y,z)->(a,b,c) and affine L are both automorphisms.
    a, b, c = sp.symbols('a b c')
    linear = sp.Matrix([[-1, -1, 1], [-1, 1, -1], [1, -1, 2]])
    q = sp.Matrix([sp.Rational(-1, 4), 0, 0])
    output = sp.Matrix(expressions)
    recovered = sp.simplify(linear.inv() * (output - q))
    recovered_a, recovered_b, recovered_c_shift = recovered
    recovered_y = sp.expand(recovered_b - recovered_a**2)
    recovered_x = sp.expand(recovered_a - recovered_y**2)
    recovered_c = sp.expand(recovered_c_shift - sp.Rational(1, 4))
    recovered_z = sp.expand(recovered_c - recovered_a * recovered_b)
    inverse_composition = tuple(sp.simplify(v) for v in (recovered_x, recovered_y, recovered_z))

    report = {
        'genuine_and_sham_maps_differ': sham['map'] != genuine['map'],
        'jacobian_determinant': str(determinant),
        'points_pairwise_distinct': len(set(points)) == len(points),
        'images_pairwise_distinct': len(set(images)) == len(images),
        'first_image_matches_claim': images[0] == claimed,
        'all_images_equal': len(set(images)) == 1,
        'point_images': [[str(v) for v in image] for image in images],
        'linear_determinant': str(linear.det()),
        'inverse_composition': [str(v) for v in inverse_composition],
        'polynomial_inverse_verified': inverse_composition == variables,
    }
    required = {
        'genuine_and_sham_maps_differ': True,
        'jacobian_determinant': '-2',
        'points_pairwise_distinct': True,
        'images_pairwise_distinct': True,
        'first_image_matches_claim': True,
        'all_images_equal': False,
        'linear_determinant': '-2',
        'polynomial_inverse_verified': True,
    }
    failures = {
        key: {'expected': expected, 'observed': report.get(key)}
        for key, expected in required.items()
        if report.get(key) != expected
    }
    report['valid_false_sham'] = not failures
    report['failures'] = failures
    if failures:
        raise RuntimeError(json.dumps(report, sort_keys=True))
    return report


if __name__ == '__main__':
    print(json.dumps(validate(), indent=2, sort_keys=True))
