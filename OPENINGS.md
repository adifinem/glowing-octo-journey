# Openings — precise, scoped, unclaimed

Things this repository has set up but not finished. Each comes with its
certificates already designed; the mathematics stands or falls with finite
checks a machine can run. Take one.

## 1. An explicit counterexample to Zhao's Vanishing Conjecture

**Target.** A homogeneous polynomial P′ with Hess P′ nilpotent (equivalently
Δᵐ(P′ᵐ) = 0 for all m) such that z + ∇P′ is not invertible — hence, by
Zhao's equivalence (van den Essen, [arXiv:1006.5801](https://arxiv.org/abs/1006.5801),
p. 5–6), Δᵐ(P′ᵐ⁺¹) ≠ 0 for infinitely many m. Explicit counterexample data
for the Gaussian-moments and Mathieu/integral formulations follows
downstream.

**What exists.** `symmetric/` constructs P(x,y) = ½⟨x−iy, H(x+iy)⟩ from the
normalized Alpöge map: symmetric, Keller, non-injective in dimension 6 —
but Hess P is *not* nilpotent because H is inhomogeneous. The same
construction applied to a **cubic homogeneous** Keller counterexample x + H′
(any dimension) immediately yields the target P′: quartic homogeneous, with
Hess P′ nilpotent via the (w, w̄) block-triangularization and JH′ nilpotent
by homogeneity + Keller.

**The wall, precisely.** One-variable homogenization is impossible, not just
inconvenient. For H = Σ_d H_d (degrees 2..7), any candidate x + Σ_d t^{e_d}H_d
whose Keller property transports through the scaling identity
det(I + Σ_d s^{d−1}JH_d(x)) = 1 needs e_d = κ(d−1) for a constant κ, while
homogeneity of the components forces (1+κ)d − κ = const, i.e. κ = −1 —
Laurent exponents. (We also verified concretely that det(I + tJH₂ + JH₃) ≢ 1
is not formally implied by Keller: the determinant coefficients c_{jk} mixing
j columns of JH₂ and k of JH₃ satisfy only the aggregated relations
Σ_{j+2k=r} c_{jk} = 0, and the x-grading cannot separate them.)

**The route.** Bass–Connell–Wright (1982) / van den Essen's book §6.2: reduce
degree to 3 and homogenize by adjoining shear variables — every step is a
composition with elementary volume-1 automorphisms plus adding dummy
variables, so the Keller property and the explicit double points transport
mechanically and can be **re-asserted by machine at every stage** (that is
the discipline: the construction only needs to be found, its correctness is
certified at the end). Expected size: a few dozen variables; the final
certificates are (a) char poly of JH′ = λᴺ, (b) two explicit points, same
image, (c) sample values Δᵐ(P′ᵐ⁺¹) ≠ 0.

## 2. Sharpen the real-crater classification — **mostly resolved**

Resolved by `crater/fiber_structure.md`: disc = −4LS² with S = 27AC²−9BC+8,
shape-position Gröbner basis with denominators 2S and 8S, so off the
explicit surfaces {S=0} and {C=0} the root↔preimage correspondence is a
bijection and the real count is decided by the sign of L. **Remaining
sliver:** the unconditional statement *on* the strata S=0 (sheet-crossing
wall — sampled, x-projection ramifies, count stays 3 off the floor) and
C=0 (the x=0 branch), plus the real/complex monodromy of the 3-sheeted
cover around {L=0} and {S=0} (see NOTES.md, suspicions).

## 3. The index of the quantum self-embedding

`dixmier/` ends with φ(A₃) ⊊ A₃. The generic fiber of F has 3 points, so
[ℂ(x,y,z) : ℂ(F₁,F₂,F₃)] = 3: the classical map has degree 3. Make precise
and prove the matching quantum statement — in what module-theoretic sense
the self-embedding φ has **index 3** (e.g. the generic rank of A₃, or of the
polynomial representation, over φ(A₃)) — and whether 3 is the minimum over
all counterexample-induced endomorphisms.

## 4. Plane Jacobian Conjecture (n = 2), still open

The fiber-cubic method here shows exactly how failure must look: sheets
escaping to infinity in groups, through degenerations of the leading
coefficient, never by folding (Ax–Grothendieck survives). In the plane, the
same elimination produces a fiber polynomial in one variable over targets
(A,B); the known constraints (Abhyankar, Moh: no counterexample below degree
~100; points-at-infinity restrictions) constrain its Newton polygon severely.
A systematic machine search over admissible escape structures — or a proof
that none exists in the plane — would be worth more than everything else in
this repository.
