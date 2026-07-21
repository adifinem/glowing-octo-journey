# The real crater: F over ℝ³, classified

*Companion to `fiber_geometry.md`; samples machine-verified in
`verify_real_crater.py`, figure in `real_crater_map.png`.*

The map F has integer coefficients and Jacobian ≡ −2, so F: ℝ³ → ℝ³ is an
everywhere-local diffeomorphism scaling volume by 2. We showed in
`fiber_geometry.md` that it is not injective over ℝ. Here is the full real
picture.

## Classification

For a real target (A, B, C) with C ≠ 0 and a full 3-point complex fiber, the
number of **real** preimages is governed by the discriminant of the fiber
cubic L·x³ + (4 − 3BC)·x − 2C:

```
disc = −4L(4−3BC)³ − 108 L²C²
```

- **disc > 0:** all three preimages are real — F is honestly 3-to-1 over ℝ.
- **disc < 0:** exactly one real preimage (the other two form a conjugate
  pair).

Two small arguments carry this. First, a real x-root gives a real preimage:
the fiber is reduced (F is étale), conjugation permutes it fixing x, so the
unique preimage over a real x is fixed, hence real. Second — the **parity
argument** — conjugation acting on a fiber of odd cardinality must fix at
least one point, so *every* real target with a nonempty odd fiber has a real
preimage.

## Consequences

1. **Real surjectivity up to the floor.** Fibers have cardinality 3, 1
   (rim), or 0 (floor) — never 2 — so every real target off the floor curve
   has a real preimage: **F(ℝ³) misses exactly the real floor curve
   (B²/12, B, 4/(3B)), B ∈ ℝ\{0}**, the same curve as over ℂ. A polynomial
   local diffeomorphism of ℝ³ with constant volume distortion whose image is
   the complement of one smooth curve.
2. **The geometry of the 3-to-1 region.** disc factors through L
   (disc = −4L[(4−3BC)³ + 27LC²]), so the boundary of the 3-to-1 region has
   two walls: the **rim** L = 0 (two sheets leave to infinity) and the
   **fold-free wall** (4−3BC)³ + 27LC² = 0, where two real preimages become
   complex *without ever colliding* (étale maps cannot fold — the pair goes
   complex, not degenerate). In the slice C = 1 the 3-to-1 region is a wedge
   pinching shut precisely at the omitted point (4/27, 4/3) — see the figure.
3. Contrast with the classical picture: Pinchuk's 1994 map has non-constant
   Jacobian; here the volume distortion is constant and the failure of
   injectivity over ℝ is total on an open region, yet invisible to any local
   test.

Status of rigor: the classification is proved conditional on the fiber being
a full 3-point fiber (true off a proper algebraic subset; the parity and
conjugation arguments are unconditional given that count, and the count and
realness are verified exactly at samples in all region types — six targets
with varied signs of L, B, C in `verify_real_crater.py`).
