# The fiber structure theorem: S, the shape position, and the sign of L

*The definitive statement of the crater's geometry, superseding the
conditional parts of `real_crater.md`. Machine verification:
`verify_shape.py`.*

Let L = 27A²C² − 18ABC + 16A + B³C − B² (the fiber cubic's leading
coefficient) and

**S = 27AC² − 9BC + 8.**

## Three identities (all machine-verified)

1. **The discriminant factors:** disc(L·x³ + (4−3BC)x − 2C) = **−4·L·S²**.
2. **The floor is an intersection:** L restricted to {S = 0} equals
   (3BC−4)³/(27C²), so **{L=0} ∩ {S=0} is exactly the omitted floor curve**
   (B²/12, B, 4/(3B)).
3. **Shape position:** over the function field ℚ(A,B,C), the reduced lex
   Gröbner basis of the fiber ideal is

   **{ y − p(x), z − q(x), L·x³ + (4−3BC)x − 2C }**

   with p, q ∈ ℚ(A,B,C)[x] of degree ≤ 2 whose coefficient denominators are
   **2S and 8S** — the same S. (Certificate: substituting y = p(x),
   z = q(x) into the three original fiber equations and reducing modulo the
   cubic gives zero.)

## The theorem

For any target (A, B, C) ∈ ℂ³ with **C ≠ 0 and S ≠ 0**, the fiber of F is
exactly {(x, p(x), q(x)) : x a root of the fiber cubic} — one preimage per
distinct root, unconditionally. Hence:

| stratum | # preimages |
|---|---|
| L ≠ 0 | **3**, all distinct (disc = −4LS² ≠ 0) |
| L = 0 | **1** (the linear coefficient 4−3BC cannot also vanish: that would force S = 0) |
| — | never 2, never more than 3 |

And over ℝ (real targets, C ≠ 0, S ≠ 0): since disc = −4LS² has the sign of
−L, the count of **real** preimages is decided by L alone:

- **L < 0 ⟹ 3 real preimages. L > 0 ⟹ 1 real. L = 0 ⟹ 1 real.**

The genericity caveats of `real_crater.md` are hereby discharged: the
exceptional set is the explicit surface {S = 0} together with the plane
{C = 0}, not an abstract "proper subvariety".

## What happens on S = 0: the sheet-crossing wall

S = 0 is *not* a wall of the fiber count — it is the locus where the
**x-projection of the fiber ramifies while the map stays étale**. Verified
sample: the target (−8/27, 0, 1) has S = 0, L = −64/27, fiber cubic
32x³ − 54x + 27 = (4x−3)²(2x+3), and **three** real preimages —
(−3/2, 4/3, 104/27) and the pair (3/4, −2/3 ± 2√3/3, 104/27 ∓ 8√3/3)
**sharing the x-coordinate 3/4**. Two sheets cross in the x-coordinate
without meeting in space. This is also exactly why y cannot be a polynomial
in x there — i.e., why S must appear in the shape-position denominators. The
consistency is total.

## How S was found

The six sampled targets suggested "3 real ⟺ L < 0". Testing whether that
could be a theorem meant asking whether W := 27LC² + (4−3BC)³ has constant
sign; expanding, the B³C³ terms cancel and W = (27AC² − 9BC + 8)² — a perfect
square. Everything above unwinds from that one cancellation.
