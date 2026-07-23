#!/usr/local/stuff/jspace/.venv/bin/python
"""Narrow MCP exact-arithmetic affordance for the JC belief-revision pilot."""

from __future__ import annotations

import re
from typing import Any

import sympy as sp
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("exact-polynomial-map")
_NAME = re.compile(r"[A-Za-z]+")
_EXPR = re.compile(r"[0-9A-Za-z+*/().^\- ]+")
_RATIONAL = re.compile(r"[+\-]?[0-9]+(?:/[0-9]+)?")


def _parse_expr(text: str, symbols: dict[str, sp.Symbol]) -> sp.Expr:
    if not _EXPR.fullmatch(text):
        raise ValueError("expression contains a forbidden character")
    names = set(_NAME.findall(text))
    if not names <= set(symbols):
        raise ValueError(f"unknown names: {sorted(names - set(symbols))}")
    return sp.sympify(text.replace("^", "**"), locals=symbols)


def _parse_rational(text: str) -> sp.Rational:
    if not _RATIONAL.fullmatch(text.strip()):
        raise ValueError(f"not an exact rational: {text!r}")
    return sp.Rational(text)


def polynomial_map_report_impl(
    variables: list[str], expressions: list[str], points: list[list[str]]
) -> dict[str, Any]:
    """Compute the exact Jacobian determinant and exact images of supplied points."""
    if not variables or len(expressions) != len(variables):
        raise ValueError("need n variables and n coordinate expressions")
    if len(set(variables)) != len(variables) or any(not v.isalpha() for v in variables):
        raise ValueError("variables must be distinct alphabetic names")
    syms_tuple = sp.symbols(" ".join(variables), seq=True)
    symbols = dict(zip(variables, syms_tuple, strict=True))
    exprs = [_parse_expr(text, symbols) for text in expressions]
    jacobian = sp.Matrix(exprs).jacobian(syms_tuple)
    det = sp.factor(jacobian.det())

    images: list[list[str]] = []
    for point in points:
        if len(point) != len(variables):
            raise ValueError("every point must have n coordinates")
        values = [_parse_rational(value) for value in point]
        sub = dict(zip(syms_tuple, values, strict=True))
        images.append([str(sp.factor(expr.subs(sub))) for expr in exprs])

    return {
        "jacobian_determinant": str(det),
        "point_images": images,
        "all_images_equal": bool(images and all(image == images[0] for image in images[1:])),
        "points_pairwise_distinct": len({tuple(point) for point in points}) == len(points),
    }


@mcp.tool()
def polynomial_map_report(
    variables: list[str], expressions: list[str], points: list[list[str]]
) -> dict[str, Any]:
    """Return an exact symbolic Jacobian determinant and exact images of rational points.

    Inputs are variable names, one polynomial coordinate expression per variable, and
    rational points encoded as strings such as "-1/4". No floating-point arithmetic,
    files, network, repository data, or external retrieval are used.
    """
    return polynomial_map_report_impl(variables, expressions, points)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Exact polynomial-map MCP server")
    parser.add_argument("--transport", choices=("stdio", "streamable-http"), default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    mcp.settings.host = args.host
    mcp.settings.port = args.port
    mcp.run(transport=args.transport)
