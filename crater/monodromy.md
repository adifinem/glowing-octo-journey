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

*Proof.* (1) the fiber cubic is **irreducible over ℂ(A,B,C)** (Lemma 1
below), so the monodromy is transitive; (2) the discriminant is
−4LS² = (2S)²·(−L), and **−L is not a square in ℂ(A,B,C)** (Lemma 2) — the
discriminant is a non-square, so the Galois group is not contained in A₃.
A transitive subgroup of S₃ not inside A₃ is S₃. ∎

## Exact irreducibility over ℂ(A,B,C) (certificate alignment, issue #11)

The original script checked factorization over ℚ; the two lemmas below
(proposed by GPT-Sol in issue #11, verified here) close the gap to the
complex function field. Their finite algebra is asserted in
`verify_monodromy.py` checks 6–7; the rational factorizations of checks 1–2
remain as sanity tests.

**Lemma 1 (the cubic has no root in ℂ(A,B,C)).** Work over K = ℂ(B,C) with
the valuation v at A = ∞ (v(A) = −1). The three terms of the cubic evaluated
at a putative root r ∈ K(A) with v(r) = −d have valuations
v(L·r³) = −2−3d (since deg_A L = 2 with unit leading coefficient 27C²,
check 6), v((4−3BC)·r) = −d, and v(2C) = 0. For the sum to vanish, the
minimum must be attained at least twice; running over d ∈ ℤ, the candidate
coincidences are d = −1 (valuations 1, 1, 0 — minimum 0 unique), d = 0
(valuations −2, 0, 0 — minimum −2 unique), and d = −2/3 ∉ ℤ; every other d
leaves a strict minimum. No root exists; a cubic without a root over a field
is irreducible. ∎

**Lemma 2 (−L is not a square in ℂ(A,B,C)).** As a quadratic in A, L has
discriminant **disc_A(L) = −4(3BC−4)³** (check 7 — note the tower: this is
built from the fiber cubic's own linear coefficient). The factor 3BC−4 is
linear in B, hence irreducible, and occurs to the odd power 3, so disc_A(L)
is a non-square in ℂ(B,C) and L is irreducible over ℂ(B,C)[A]. Since L is
primitive as a polynomial in A over ℂ[B,C] (content 1, check 7), Gauss's
lemma makes L irreducible in ℂ[A,B,C]; in particular L is squarefree, −L has
odd valuation along {L = 0}, and −L is not a square in ℂ(A,B,C). ∎

**The C = 0 stratum is internally covered** (check 8): substituting C = 0,
the fiber ideal over ℚ(A,B) has the shape-position basis
{y − p(x), z − q(x), x·((16A−B²)x² + 4)} with **constant** denominators —
no exceptional locus at all — so every target with C = 0 and L = 16A−B² ≠ 0
has exactly three preimages (x = 0 and the two roots of Lx² + 4), with the
explicit reconstruction y = B/4 − 3/(2x), z = (2−3xy)/x² on the x ≠ 0
branches (Sol's formulas, verified by reduction). The covering claim on
U = ℂ³ ∖ {L=0} is thus internal on every stratum.

**Corollary (the casserole).** π₁(ℂ³ ∖ {L = 0}) is **nonabelian**: the
monodromy representation of the Alpöge covering realizes an explicit
surjection onto S₃. Since complements of hypersurfaces in general position
have abelian fundamental groups (Zariski's program: nonabelian π₁ certifies
special/singular geometry), the rim hypersurface {L = 0} — an irreducible
quartic 3-fold — is Zariski-special, with the non-normal 3-cover as the
witness.

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
