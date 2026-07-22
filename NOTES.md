# Research log

Dense working notes: what is proved, what failed and *why*, traps hit,
suspicions, and where to look next. Findings with a script pointer are
machine-verified; everything else is labeled. Newest material last.
(Companion files: README for the artifacts, OPENINGS for the scoped
problems.)

## Notation

F = the Alpöge map (repo root); fiber cubic over target (A,B,C):
L·x³ + (4−3BC)x − 2C with L = 27A²C² − 18ABC + 16A + B³C − B²;
S = 27AC² − 9BC + 8; floor curve = (B²/12, B, 4/(3B)); H = JF(0)⁻¹F − id.

## Proved (machine-verified)

- **Napkin:** det JF ≡ −2; 3 exact preimages of one rational point
  (`verify_alpoge_map.py`). Real form: 3 real preimages of (3/100,1,1)
  (`dixmier/verify_dixmier.py` #3).
- **Fiber cubic identity** via resultants; F omits the floor curve
  (`dixmier/verify_dixmier.py` #5).
- **Dixmier dies:** D_i = Σ (J⁻¹)_{ai}∂_a gives an endomorphism of A₃
  ([D_i,F_j]=δ, [D_i,D_j]=0 verified); non-surjectivity by normal-ordering a
  putative preimage of x₁ and applying to 1 → x₁ = Q₁(F), refuted by the
  collision pair differing in x₁. Elementary; no Ax–Grothendieck needed
  (`dixmier/`). [Sharpened per review issue #1.]
- **Symmetric Keller counterexample, dim 6:** P = ½⟨x−iy, H(x+iy)⟩;
  (w,w̄) = (x+iy, x−iy) makes G = z+∇P block-triangular
  (w+H(w), w̄+JH(w)ᵀw̄) (`symmetric/`).
- **disc = −4·L·S²**; **floor = {L=0} ∩ {S=0} exactly**
  (L|_{S=0} = (3BC−4)³/27C²); **shape position** over ℚ(A,B,C):
  GB = {y−p(x), z−q(x), cubic}, denominators of p,q = 2S, 8S; certificate by
  reduction mod the cubic (`crater/verify_shape.py`). Consequences: for
  C·S ≠ 0 fibers have exactly 3 (L≠0) or 1 (L=0) points — never 2; real
  count decided by **sign of L alone** (3 real ⟺ L<0).
- **S-wall:** on S=0 the x-projection of the fiber ramifies, the map does
  not: target (−8/27,0,1) has 3 real preimages, two sharing x = 3/4
  (`crater/verify_shape.py` #5).
- **Monodromy theorem:** the 3-cover over ℂ³∖{L=0} has **full S₃**
  monodromy: cubic irreducible (transitive) + disc = (2S)²(−L) with L
  irreducible (non-square ⟹ not in A₃). Local: rim = transposition of the
  escaping pair (the ±√(1/L) flip), S-wall = trivial (covering extends
  across it). Numerically: all three transpositions appear around the four
  rim points of one generic line (`crater/verify_monodromy.py`). Slogan
  found: *the discriminant factorization is the monodromy* — simple factor
  (−L) = branching wall, square factor S² = phantom wall. Suspicion above
  now proved; confirms MO 513387 independently for the original map.
- **Surjectivity theorem:** F(ℂ³) and F(ℝ³) are *exactly* the complements
  of the floor curve. Five-stratum proof: C=0 explicit preimage; S≠0 shape
  position in x; S=0 shape position in y over ℚ(B,C) with leading coeff
  54C³ (never 0); floor empty; leftover curve {A=0, BC=8/9} has 3 explicit
  rational-in-C preimages, e.g. (−9C/2, 8/(9C), 512/729C²)
  (`crater/verify_shape.py` #6–8). Method note: when shape position fails
  on a stratum, **re-run the Gröbner basis restricted to the stratum with a
  different separating variable** — it worked on the first try both times.
- **Fiber traces through degree two:** Tr(x)=0, Tr(y)=3B/2, and Tr(z) is
  polynomial; among quadratic coordinate monomials only **Tr(x²)** is not
  polynomial: Tr(x²)=2(3BC−4)/L. Thus the paired sheets cancel in the
  centroid while their second x-moment has a simple pole at the rim. The
  trace pairing on {1,x,x²} has determinant **−4S²/L³**: the S² zero records
  failure of x to separate distinct sheets, while the L⁻³ pole records loss
  of finiteness at the nonproperness rim (`crater/verify_traces.py`).

## Dead ends, with reasons (don't retry these)

- **Naive symmetrization P₀ = ⟨y,H(x)⟩:** not Hessian-nilpotent even for
  invertible H = (x₂³,0): char poly λ⁴ − 6λ³x₂y₁ − 9λ²x₂⁴. The i in
  ½⟨x−iy,H(x+iy)⟩ is load-bearing.
- **Same-argument pairing ⟨x+iy, H(x+iy)⟩:** gives Hess = M⊗[[1,i],[i,−1]]
  with square zero (always Hessian-nilpotent!) — but the map is a
  w-preserving shear, hence invertible for *every* H. Nilpotency and
  non-invertibility trade off between the two pairings; only BCW breaks the
  trade.
- **One-variable homogenization of H = Σ H_d:** impossible. Keller transport
  through the scaling identity det(I + Σ s^{d−1}JH_d(x)) = 1 forces
  exponents e_d = κ(d−1); homogeneity of components forces κ = −1: Laurent.
  Also directly: det(I + tJH₂ + JH₃) ≢ 1 is not implied by Keller — the
  minor-sums c_{jk} satisfy only Σ_{j+2k=r} c_{jk} = 0, and the x-grading
  gives every term in that sum the same degree, so the relations cannot be
  split. This is *why* BCW needs variable-splitting gadgets.
- **Quasi-homogeneity shortcut:** F is quasi-homogeneous for weights
  (x,y,z) = (−1,1,2) with component weights (2,1,−1) — permuted, shift
  non-uniform, and a uniform-shift grading argument needs shift ≠ 0 with
  positive weights. Doesn't give JH nilpotency. (The negative weight is
  presumably how the map was *found*, though.)

## Traps hit (so you don't)

- **Pointwise vs identical nilpotency:** Hess P vanishes to 6th power at
  (1,0,0,0,0,0) yet is not nilpotent as a matrix over the ring. Spot-checks
  of nilpotency at a point prove nothing; use the char poly.
- **sympy structural equality:** `factor(...) == 2*S` fails though equal
  (Mul vs distributed Add); compare `expand(difference) == 0`.
- **Casus irreducibilis:** real cubic roots come out of `solve` as complex
  radicals; test realness via the discriminant + conjugation-fixing
  argument, or high-precision bounds — never `im(N(v)) == 0`.
- **Resultants lie about multiplicity:** the raw eliminant was
  −C·x¹²·(cubic); the x¹² and C factors are noise. The Gröbner basis over
  ℚ(A,B,C) gives the clean minimal polynomial. Prefer GB for the final
  statement, resultants for discovery.

## From the certificate-alignment pass (issue #11, Sol's lemmas)

- **[PROVED] Discriminant tower:** disc_x(fiber cubic) = (2S)²·(−L) and
  **disc_A(L) = −4·(3BC−4)³** — the cubic's leading coefficient and linear
  coefficient are each other's discriminant ingredients. Sol's valuation
  lemma (no rational-function root, by the A = ∞ valuation profile
  (−2−3d, −d, 0)) and the Gauss-lemma chain make both irreducibility claims
  exact over ℂ(A,B,C), not just ℚ. `crater/verify_monodromy.py` 6–7.
- **[CERTIFIED] C = 0 stratum shape position with CONSTANT denominators**
  (16 and 32 — the only stratum with no exceptional locus); univariate
  x·((16A−B²)x²+4); Sol's closed reconstruction y = B/4 − 3/(2x),
  z = (2−3xy)/x² verified by reduction. Check 8.
- **[PROVED] π₁ corollary:** π₁(ℂ³∖{L=0}) is nonabelian (explicit S₃
  quotient via the covering) — the rim quartic is Zariski-special.
- Process note: Sol filed the issue *with candidate proofs*; both were
  correct as stated. Review-with-proofs is the right ticket format.

## Quotient-cusp and trace-form synthesis (issue #10 / Discussion #13)

- **[CERTIFIED] Weighted quotient:** the invariant rings are
  `C[xy,x²z]=C[r,t]` and `C[BC,AC²]=C[u,v]`; `F` descends to the explicit
  plane map in `crater/quotient_geometry.md`. On `C≠0`, the rim is literally
  `G_m × {s²=(4−3u)³}` and the omitted floor orbit is the cusp tip. The coarse
  quotient is not globally étale: `det(JQ)=2(3r+t−2)²`, and that critical line
  collapses to the rim point `(0,0)`; it is étale over `ell≠0`.
- **[CERTIFIED] Quotient cubic:** with
  `ell=u³−u²−18uv+27v²+16v`, `D=u³−18uv+54v²`, and `w=r+1`, generic quotient
  fibers satisfy `ell·w³+(u²−12v)w−4v=0`; its discriminant is `−4ell·D²`,
  `t` reconstructs with denominator `2D`, and the quotient trace determinant
  is `−4D²/ell³`. The rim survives quotienting; only the shadow changes.
- **[CERTIFIED] Trace-form parity:** changing from `{1,x,x²}` to
  `{1,y,y²}` sends `det(T_x)=−4S²/L³` to `det(T_y)=−729A²L/4`.
  The full divisor and pole presentation depend on the chosen polynomial
  lattice; the determinant square class `−L` and its odd rim valuation are
  intrinsic. Over `R`, trace-form signature recovers the real fiber count.
- **[CERTIFIED/PROVED] Hasse--Witt class:** exact diagonalization gives
  `<3,−2R/L,2S²/(3RL²)>`; quaternion bilinearity plus the norm witnesses
  `S²−27LC²=R³` and `1²−3·1²=−2` reduce its Hasse invariant to **`(2,L)`**
  over `Q(A,B,C)`. Its residue at `L=0` is the nonsquare `2`, so it is
  nontrivial over `Q` but splits over `R` and `C`. The failure registry must be
  field-sensitive: `(field; rank; det class; Hasse--Witt; signatures)`.
- **[CERTIFIED] Exact monodromy loop:** the half-turn of the full `G_m` action
  along target `(-lambda²/4,0,0)` fixes the zero sheet and exchanges the two
  rational `±` sheets, giving a symbolic transposition around the rim.

## From the Sol merge (2026-07-21, `local_to_global/`)

- **[CERTIFIED] All-rational collision fiber** (Sol's find, the simplest
  known witness): (0,0,−1/4), (1,−3/2,13/2), (−1,3/2,13/2) all map to
  (−1/4, 0, 0) — no radicals. Our theory explains it: the target is on
  C=0, where the fiber cubic degenerates to x(Lx²+4) with L = 16A−B² = −4,
  roots x ∈ {0, ±1}; rational because −4/L = 1 is a perfect square. By ZMT
  (fibers ≤ 3) this is the complete fiber. Candidate to replace the √31
  fiber as the canonical witness everywhere (issue filed).
- **[PROVED] ℤ/2 equivariance:** F(−x,−y,z) = (F₁, −F₂, −F₃), i.e.
  F∘σ = τ∘F with σ = diag(−1,−1,1), τ = diag(1,−1,−1) — verified
  symbolically. Both L and S are τ-invariant, and τ maps the floor curve to
  itself (B ↦ −B). Sol's paired ± branches are the σ-action on a fiber over
  the τ-fixed locus {B=C=0}. Quotient geometry unexplored (issue filed).
- **Adopted:** the epistemic labels and bridge ledger of
  `local_to_global/CLAIM_DISCIPLINE.md` for future notes and issues.

## Arguments worth remembering

- **Parity:** conjugation permutes a fiber over a real target; odd fiber ⇒
  a fixed point ⇒ a real preimage. With counts ∈ {3,1,0}: F(ℝ³) = ℝ³ minus
  the real floor curve.
- **Zariski main theorem bound:** F étale, generically 3:1 ⇒ *every* fiber
  has ≤ 3 points (quasi-finite ⇒ open immersion into a finite degree-3
  cover).
- **Certificate discipline:** any construction (however found — including
  guessing) is acceptable if the final object carries finite certificates:
  char poly = λᴺ, det ≡ 1, explicit collision pair, reduction to zero mod an
  eliminant. Constructions need finding, not trusting.

## Suspicions / observations (unproved, unassigned)

- The three real preimages in the L<0 region should admit a global
  description as three continuous sheets over the wedge, glued along the
  S-wall by the x-crossing; the wedge pinches at the floor point. A real
  monodromy statement ("going around the floor curve permutes the sheets")
  would be the crown on the real story — the complex monodromy of the
  3-cover around {L=0} is presumably a transposition (two sheets escape
  together) and around {S=0} trivial; worth computing honestly.
- S is linear in A. So {S=0} is a graph over (B,C): the sheet-crossing wall
  is *rational and simple*, which suggests the whole crater has a modular /
  parametrized description waiting (the map's origin via deg(x) = −1 grading
  points the same way).
- Zhao's equivalences convert the eventual VC counterexample's "infinitely
  many m" into explicit inversion-formula data; the smallest m with
  Δᵐ(P′ᵐ⁺¹) ≠ 0 is a new invariant of the counterexample. No idea what it
  means yet.
- The dim-6 symmetric example has complex coefficients (the i is essential
  to the trick, and stays in P). Whether a *real*-coefficient symmetric
  Keller counterexample exists in low dimension is open here; possibly
  ½⟨x−iy,H(x+iy)⟩ + conjugate in 12 real variables works — check whether
  Keller and non-injectivity survive the realification. Cheap to test.

## Where to look next (with sources)

- **BCW/VC extraction** (OPENINGS #1, issue tracker): the reduction gadgets
  are in van den Essen, *Polynomial Automorphisms* (Birkhäuser 2000) §6.2,
  and in M. de Bondt's PhD thesis (Radboud University, openly hosted in
  their repository) — fetch one of these *first*, don't re-derive. Then
  P′ = ½⟨x−iy, H′(x+iy)⟩ finishes it, with certificates as listed above.
- **Zhao's equivalences:** van den Essen's survey, arXiv:1006.5801, p. 5–6
  (statements used here verbatim); Zhao's originals [Z1] (J. Algebra, 2004ish)
  for the inversion formula behind "Δᵐ(Pᵐ⁺¹) ⟺ invertibility".
- **Plane JC** (OPENINGS #4): the degree bound for a planar counterexample
  is ≥ **108** (arXiv:2204.14178, improving Moh's 100), versus degree 7 in
  dimension 3 — something qualitative separates the dimensions. The
  points-at-infinity literature (Abhyankar) constrains the escape structure;
  the fiber-polynomial viewpoint here (leading-coefficient degenerations,
  never-fold) should translate into Newton-polygon conditions.
- **Monodromy (suspicion partially confirmed externally):** a MathOverflow
  thread reports an explicit cubic model of the counterexample with **S₃
  monodromy** — non-normal 3-sheeted cover, which is reportedly how it
  evades the known Galois-case theorems. Matches the suspicion above; still
  worth computing honestly for *this* map (issue #5).
  https://mathoverflow.net/questions/513387/
- **Primary sources for the VC/symmetric chain:** Zhao arXiv:math/0409534
  (TAMS 359 (2007) 249–274); de Bondt–van den Essen Proc. AMS 133 (2005)
  2201–2205; BKK arXiv:math/0512171; Kontsevich–Belov arXiv:math/0512169
  (Weyl automorphisms). Review issue #3 contains a broad exploration
  program (witness compilers, moduli of counterexamples, cotangent-lift
  mechanics, normalizing-flow benchmark, epistemic-hysteresis experiment) —
  treat it as the idea quarry.

## Process: the discussion ledger (2026-07-21)

GitHub Discussions is the standing "aha ledger" — insights, open questions,
and cross-domain riffs go there *when they arise*, so they survive session
amnesia and don't rot in this file. Seeded: #12 universal-cubic cusp
synthesis, #13 fiber conservation laws (Tr(x)=0, Tr(y)=3B/2, polynomial
centroids), #14 local-vs-global meta-thread (incl. the time-sensitive
epistemic-hysteresis experiment), #15 failure ecology/moduli, #16 plane-JC
obstruction ledger. Issues = scoped work; discussions = live questions;
NOTES = distilled outcomes.
