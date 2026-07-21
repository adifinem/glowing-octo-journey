# The monodromy of the crater: full S₃

*Machine verification: `verify_monodromy.py`. Closes the monodromy half of
issue #5; the stratum half is `fiber_structure.md`.*

## Setup

By the fiber structure theorem, over **U = ℂ³ ∖ {L = 0}** the map F has
constant fiber cardinality 3 and is étale, so it restricts to an unramified
**3-sheeted covering** F⁻¹(U) → U (sheets can only disappear at the rim, so
no escape happens over U and the local homeomorphism with constant finite
fibers is a genuine covering map). Its monodromy is a representation
π₁(U) → S₃, and its image equals the Galois group of the fiber cubic
L·x³ + (4−3BC)x − 2C over ℂ(A,B,C).

## Theorem

**The monodromy group is the full symmetric group S₃.** The covering is
connected and non-normal: the three sheets are globally inequivalent.

*Proof.* Two machine checks: (1) the fiber cubic is **irreducible** over the
function field (`verify_monodromy.py` check 1), so the monodromy is
transitive; (2) the discriminant is −4LS² = (2S)²·(−L), and L is an
**irreducible** polynomial (check 2), hence squarefree, so −L has odd
valuation along {L = 0} and cannot be a square in ℂ(A,B,C) — the
discriminant is a non-square, so the Galois group is not contained in A₃.
A transitive subgroup of S₃ not inside A₃ is S₃. ∎

## Local monodromy

- **Around the rim {L = 0}: a transposition.** Near L = 0 the two escaping
  roots behave like ±√(−(4−3BC)/L)·(1 + o(1)); winding L once around 0
  flips the square root, exchanging exactly the two escaping sheets while
  the surviving sheet returns to itself. Numeric witness (check 3): loops
  around both rim points on the line B = C = 1 return the permutation
  (0 1), identity on the third sheet.
- **Around the S-wall {S = 0}: trivial.** The covering extends across
  S = 0 — the three preimages remain distinct there (only their
  x-coordinates cross; see `fiber_structure.md`), so a small loop around
  the wall does nothing. Numeric witness (check 4): identity permutation.
- **Global generation** (check 5): on a generic complex line, the four rim
  points yield the transpositions (0 2), (1 2), (0 1), (0 2) at a common
  basepoint — generating a subgroup of order 6, the whole of S₃, matching
  the algebraic proof.

## Remarks

1. Non-normality is structural, not incidental: a *normal* (Galois)
  3-sheeted cover would have cyclic A₃ monodromy, forcing the discriminant
  −4LS² to be a square — i.e. −L a square — which the irreducibility of L
  forbids. Relatedly, a MathOverflow discussion (question 513387) reports S₃
  monodromy for a cubic model of the counterexample and connects
  non-normality to how the construction evades the known Galois-case
  theorems; the computation here confirms the S₃ statement independently
  for the original map.
2. The two local behaviors are exactly the two factors of the
  discriminant: the simple zero (−L) is the branching wall with
  transposition monodromy; the double zero (S²) is a phantom wall — root
  collision in one coordinate's shadow, no monodromy. **The discriminant
  factorization is the monodromy, read off algebraically.**
