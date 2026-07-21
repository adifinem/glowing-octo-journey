# The anatomy of the crater: fiber geometry of the Alpöge–Fable map

*Notes to accompany `crater_map.py` / `crater_map.png`. Every displayed identity
and every stratum sample below is machine-verified in `../dixmier/verify_dixmier.py`
(checks 3 and 5).*

The map F(x, y, z) = (a, b, c) with

- a = (1+xy)³z + y²(1+xy)(4+3xy)
- b = y + 3x(1+xy)²z + 3xy²(4+3xy)
- c = 2x − 3x²y − x³z

has Jacobian determinant ≡ −2, so it is **étale**: a local isomorphism at every
point of ℂ³. Yet it is generically 3-to-1. Since étale maps cannot fold — a
merging pair of preimages would create a critical point — the only way a sheet
of the covering can disappear is by **escaping to infinity**. These notes make
that mechanism completely explicit.

## The fiber cubic

Eliminating z and then y from the fiber equations F = (A, B, C) shows that the
x-coordinate of every preimage of a target (A, B, C) with C ≠ 0 satisfies one
cubic:

```
L·x³ + (4 − 3BC)·x − 2C = 0,
L = 27A²C² − 18ABC + 16A + B³C − B²
```

(For C = 0 there is additionally the x = 0 preimage (0, B, A − 4B²).)

Three structural facts, all verified symbolically:

1. **Generic target (L ≠ 0):** three roots, three preimages — the 3-sheeted
   covering.
2. **The rim (L = 0, 4 − 3BC ≠ 0):** the cubic has *no x² term*, so when its
   leading coefficient vanishes the degree drops from 3 straight to 1 —
   **two sheets escape to infinity simultaneously**, as a pair. One preimage
   remains. Fiber cardinality never equals 2. Sample verified: the target
   (2/27, 1, 1) has exactly one preimage, (2, 5/6, −7/8).
3. **The crater floor (L = 0 and BC = 4/3):** both leading and linear
   coefficients vanish and the cubic degenerates to −2C ≠ 0 — no roots, no
   preimages. Solving the two conditions simultaneously, the omitted points
   form the rational curve

   ```
   (A, B, C) = (B²/12, B, 4/(3B)),   B ≠ 0.
   ```

   **F is not surjective**; its image omits this entire curve. This direction
   is fully rigorous: any preimage's x-coordinate must be a root of the fiber
   cubic (a resultant necessarily vanishes on common solutions), and on the
   floor curve the cubic is the nonzero constant −2C. Sample verified: the
   target (1/3, 2, 2/3) has empty fiber. In fact the image omits **exactly**
   this curve and nothing else — that stronger statement is proved by
   stratification in `fiber_structure.md` (surjectivity theorem).

In the slice C = 2/3 (see `crater_map.png`), the rim L = 0 is a cuspidal plane
curve and the omitted point sits **exactly at its cusp** — the crater floor is
the cusp locus of the crater rim.

## The real crater

The coefficients of F are integers, so F restricts to a polynomial map
ℝ³ → ℝ³ that is everywhere a local diffeomorphism, scaling volume by the
constant factor 2 (orientation-reversing). It is **not injective over ℝ
either**: the fiber cubic over the target (3/100, 1, 1) is

```
357x³ − 10000x + 20000 = 0
```

with positive discriminant (51,610,800,000,000), hence three distinct real
roots; complex conjugation permutes the three preimages while fixing each real
x-coordinate, so it fixes each preimage — all three are real. (Machine-checked
to 50 digits, together with exact resubstitution.)

Contrast: Pinchuk's 1994 counterexample to the strong real Jacobian conjecture
has a nonvanishing but *non-constant* Jacobian. Here the Jacobian is constant —
the real constant-Jacobian case falls with the same map as the complex one.

## Why the failure had to look like this

The Ax–Grothendieck theorem (an *injective* polynomial self-map of ℂⁿ is
bijective) survives the crater — it is a theorem. So any counterexample to the
Jacobian Conjecture was forced to be non-injective and many-to-one, with the
missing injectivity hidden at infinity rather than at any critical point. The
fiber cubic shows precisely how the map threads that needle: sheets leave only
in pairs, through the cusp at infinity, and the image omits exactly the curve
where there is no room left for even one sheet to stay.
