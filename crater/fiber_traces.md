# The centroid is calm; the variance sees the crater

The three generic preimages of a target `(A,B,C)` have surprisingly regular
coordinate sums. Their second moments reveal exactly where that regularity
ends. Machine verification: [`verify_traces.py`](verify_traces.py).

Throughout, `Tr(h)` means the **unweighted algebraic trace**: sum the value of
a polynomial `h(x,y,z)` over all three points of a generic fiber, counting
multiplicity. This is a completeness diagnostic for an enumerated algebraic
fiber, not a posterior expectation with arbitrary branch weights.

## Exact first moments

The shape-position basis writes every generic preimage as

```text
(x, p(x), q(x)),    Lx^3 + (4-3BC)x - 2C = 0.
```

Taking the matrix trace of multiplication in the three-dimensional algebra
`Q(A,B,C)[x]/(fiber cubic)` gives

```text
Tr(1) = 3,
Tr(x) = 0,
Tr(y) = 3B/2,
Tr(z) = -3(108A^2C^2 - 72ABC + 136A - 5B^3C + 2B^2)/8.
```

Thus the unweighted centroid is polynomial in the target. In particular, the
two sheets escaping at the rim cancel in every coordinate sum.

## The second-moment surprise

Of the six quadratic coordinate monomials, five also have polynomial traces:

```text
Tr(xy)  = -3,
Tr(xz)  = -3B(3BC+2)/4,
Tr(y^2) = -9(8A-B^2)/4,
Tr(yz), Tr(z^2) are polynomial as well.
```

But the sixth is

```text
Tr(x^2) = 2(3BC-4)/L.
```

So polynomiality is not a general trace principle. The centroid is blind to
the paired escape because opposite leading terms cancel; the second `x`
moment sees it as a simple pole. Near a generic point of the rim `L=0`, this
is the exact algebraic version of `x_+,- ~ +/-sqrt((3BC-4)/L)`: their sum stays
zero while the sum of their squares diverges like `1/L`.

This gives a sharper conservation slogan:

> The fiber centroid stays calm while its variance blows up.

For inverse problems, the first-moment identities are cheap tests that a
reported *unweighted solution set* may be complete. The `x^2` identity is a
separate stress instrument: a method that regularizes away the remote pair
can look stable in its centroid while missing a quantitatively divergent
second moment.

## The trace form contains both walls

On the power basis `{1,x,x^2}`, the trace pairing

```text
T_ij = Tr(x^(i+j))
```

has exact determinant

```text
det(T) = -4 S^2 / L^3.
```

This is the discriminant of the monic fiber cubic. Its numerator and
denominator encode the two superficially similar but geometrically opposite
walls:

- `S^2 = 0`: the power basis degenerates because `x` ceases to separate two
  distinct preimages. The map itself remains etale; this is the phantom wall.
- `L^3 = 0`: the monic model and its trace form acquire poles because two
  sheets escape to infinity. This is the actual nonproperness rim.

The same factorization that controls monodromy therefore controls the
conditioning of fiber moments. The discriminant is not only where roots
merge in a chosen coordinate; as a rational trace form, it records both
**loss of separation** and **loss of finiteness** with opposite valuations.

## What is actually coordinate-free

The displayed matrix is tied to the `x`-power lattice. Under a generic change
of basis `M`, the trace form changes by congruence `T -> M^T T M`; therefore
its determinant is intrinsic only in `K*/(K*)^2`. Here

```text
-4S^2/L^3 = -L * (2S/L^2)^2,
```

so the basis-free determinant class is exactly `-L`. The odd rim valuation is
intrinsic; the even `S^2` shadow is not.

The `y`-power basis certifies the migration explicitly. Its change-of-basis
and trace determinants are

```text
det(M_y) = 27 A L^2/(4S),
det(T_y) = -729 A^2 L/4.
```

Thus the `S^2` zero and `L^-3` pole of the `x` lattice disappear and an `A^2`
shadow takes their place, while the square class remains `-L`. The quotient
construction in [`quotient_geometry.md`](quotient_geometry.md) realizes the
same pattern entirely in invariant coordinates:

```text
det(T_Q) = -4D^2/ell^3,       ell=LC^2.
```

Over a real target, the Sylvester-Hermite signature of the trace form equals
the number of distinct real fiber points. Its inertia stratification is
therefore the real-crater classification: signature `3` on the three-real-root
side and signature `1` on the one-real-root side.

## Verification

Run:

```sh
python3 crater/verify_traces.py
```

The script recomputes the shape-position basis, constructs multiplication
matrices in the generic fiber algebra, certifies all coordinate traces through
degree two, asserts `det(T_x) = -4*S^2/L^3`, and independently changes to the
`y`-power basis to assert `det(T_y) = -729*A^2*L/4`.

-- **GPT-Sol (GPT-5.6 Thinking, OpenAI)**, July 2026
