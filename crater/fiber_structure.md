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

## The surjectivity theorem: the image is exactly the complement of the floor

**Theorem.** F(ℂ³) = ℂ³ ∖ {(B²/12, B, 4/(3B)) : B ≠ 0}, exactly — and the
same over ℝ: F(ℝ³) = ℝ³ minus the real floor curve. Proof by complete
stratification, every stratum machine-certified (`verify_shape.py` checks
6–8):

1. **C = 0:** explicit preimage (0, B, A − 4B²) — exact, and real for real
   targets.
2. **C ≠ 0, S ≠ 0:** shape position in x. If L ≠ 0 there are three roots;
   if L = 0 the linear coefficient 4−3BC cannot also vanish (that would put
   the point on S = 0), so there is one root; all roots extend through
   p(x), q(x) since their denominators 2S, 8S are nonzero. Real targets:
   a cubic (or linear) equation with real coefficients has a real root, and
   p, q have real coefficients — a real preimage.
3. **C ≠ 0, S = 0, (3BC−4)(9BC−8) ≠ 0:** shape position *on the stratum*
   with y separating: the Gröbner basis over ℚ(B,C) of the fiber ideal
   restricted to {A = (9BC−8)/27C²} is {x − r(y), z − s(y), u(y)} with
   u(y) = (3BC + 6Cy − 8)·(9C²y² + (12C − 18BC²)y + 9B²C² − 3BC − 8),
   **leading coefficient 54C³ ≠ 0**, and denominators of r, s equal to
   (3BC−4)²(9BC−8) and 54C²(9BC−8). Roots exist and extend; odd degree
   gives a real root over ℝ.
4. **C ≠ 0, S = 0, BC = 4/3:** the floor — the fiber cubic degenerates to
   −2C ≠ 0; empty. (This is the only empty stratum.)
5. **C ≠ 0, S = 0, 9BC = 8** (equivalently A = 0, BC = 8/9): three explicit
   preimages, rational in C and verified by exact substitution as
   identities: (−9C/2, 8/(9C), 512/(729C²)), (9C/4, −4/(9C), 656/(729C²)),
   (9C/4, 8/(9C), −640/(729C²)) — real for real C. (Note two share
   x = 9C/4: the S-wall crossing, again.)

So the caveats are fully discharged: the complement of the image — over ℂ
and over ℝ — is precisely the floor curve, nothing more.

## How S was found

The six sampled targets suggested "3 real ⟺ L < 0". Testing whether that
could be a theorem meant asking whether W := 27LC² + (4−3BC)³ has constant
sign; expanding, the B³C³ terms cancel and W = (27AC² − 9BC + 8)² — a perfect
square. Everything above unwinds from that one cancellation.
