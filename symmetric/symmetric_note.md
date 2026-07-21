# An explicit symmetric Keller counterexample in dimension 6

*Notes to accompany `verify_symmetric.py`, which machine-checks every claim
marked (check n). Sequel to `../dixmier/dixmier_note.md`.*

## Statement

There is an explicit polynomial **P of degree 8 in six variables** (complex
coefficients) such that

- **G = z + ∇P** has Jacobian matrix I + Hess P with **determinant ≡ 1**
  (a Keller map) — and Hess P is **symmetric** by construction, so G is a
  *gradient* (symmetric) Keller map;
- **G is not injective**: two explicit points of ℂ⁶ have the same image
  (check 5).

So the Jacobian Conjecture fails **already within the symmetric class**, in
dimension 6, with an explicit potential function. The de Bondt–van den Essen
reduction says failure of JC must show up among symmetric maps *in some
dimension*; this pins it to a concrete P.

## Construction

Let F be the Alpöge counterexample (see the repo root), A = JF(0), and
normalize: F̃ = A⁻¹F, H = F̃ − id (order ≥ 2, check 1; det(I + JH) = 1,
check 2). In ℂ⁶ = ℂ³ₓ × ℂ³ᵧ define

**P(x, y) = ½ ⟨x − iy, H(x + iy)⟩.**

## Why it works: one similarity

In the coordinates w = x + iy, w̄ = x − iy, the map G = z + ∇P becomes
(check 3, a polynomial identity):

**G ~ ( w + H(w),  w̄ + JH(w)ᵀ w̄ ).**

Its Jacobian is therefore similar to the block-triangular matrix
[[I + JH(w), 0], [∗, I + JH(w)ᵀ]], and everything falls out:

- **Keller:** det(I + Hess P) = det(I + JH)·det(I + JHᵀ) = 1 identically
  (checks 2 & 3; spot-checked numerically in check 4).
- **Non-injective:** the first block is the original map. If F̃(p) = F̃(q)
  with p ≠ q, then the points (x, y) = (p/2, −ip/2) and (q/2, −iq/2) — i.e.
  w = p resp. q on the slice w̄ = 0 — have the same G-image (check 5).
- **Symmetric:** Hess P is a Hessian; nothing to prove.

A remark worth recording: the *naive* symmetrization P₀ = ⟨y, H(x)⟩ fails —
even for an invertible Keller map H = (x₂³, 0), Hess P₀ is not nilpotent
(char poly λ⁴ − 6λ³x₂y₁ − 9λ²x₂⁴, verified). The i in ½⟨x − iy, H(x + iy)⟩
is what makes the (w, w̄) triangularization possible; it is the whole trick.

## The remaining opening: Zhao's Vanishing Conjecture, explicitly

*(This section describes a **proposed next artifact**; the dimension-6
symmetric counterexample above is the completed result of this note.)*

Zhao's Vanishing Conjecture states: for **homogeneous** P with Δᵐ(Pᵐ) = 0
for all m ≥ 1, one has Δᵐ(Pᵐ⁺¹) = 0 for m ≫ 0. Within Zhao's
homogeneous/Hessian-nilpotent framework [Z07] (see also the survey [vdE10],
p. 5–6, whose formulations we use):

- for homogeneous P, Δᵐ(Pᵐ) = 0 for all m  ⟺  **Hess P is nilpotent**
  (a finite symbolic check) [Z07];
- for such P, Δᵐ(Pᵐ⁺¹) = 0 for m ≫ 0  ⟺  **the associated gradient map is
  invertible** [Z07].

(Sign convention: much of the literature writes the gradient map as
z − ∇P; this note uses z + ∇P throughout. The two are exchanged by
P ↦ −P, which affects neither nilpotency nor invertibility.)

Our P above exhibits the second failure (z + ∇P non-invertible) but **not**
the first hypothesis: Hess P is *not* nilpotent (check 6 — equivalently JH
is not nilpotent, char poly ≠ λ³), and P is inhomogeneous. The missing step
is the classical **Bass–Connell–Wright cubic-homogeneous reduction** [BCW82]:
push F through it to a cubic homogeneous Keller counterexample x + H′ (JH′
nilpotent by homogeneity) in some dimension N, then apply the same
½⟨x − iy, H′(x + iy)⟩ construction — the reduction to the symmetric/gradient
case being due to de Bondt–van den Essen [BE05] — to get a **homogeneous
quartic, Hessian-nilpotent P′ in 2N variables** with z + ∇P′ non-invertible.

The finite certificate for the resulting Vanishing Conjecture counterexample
is: **Hessian nilpotency of P′** (char poly = λ^{2N}) **plus an explicit
collision certifying non-invertibility of z + ∇P′**; the equivalence [Z07]
then yields failure of eventual vanishing, i.e. Δᵐ(P′ᵐ⁺¹) ≠ 0 for
infinitely many m. Individually computed nonzero values of Δᵐ(P′ᵐ⁺¹) are
illustrations, not the proof — a finite list of failures cannot by itself
refute *eventual* vanishing.

On the BCW step: the classical reduction is constructive in principle and
preserves the invertibility question under stabilization and polynomial
coordinate changes, but this repository has **not yet** produced the actual
reduction sequence, added variables, or transported double points. An
explicit implementation should record each stable-equivalence transformation
so that the Keller property, non-injectivity, and the lifted collision can
be re-checked by machine at every stage. That is the natural next artifact
(see OPENINGS.md and issue #4). From the quartic P′, explicit counterexample
data for the Gaussian-moments and Mathieu-style integral formulations should
follow along the routes described in [vdE10].

## References

- [BCW82] H. Bass, E. Connell, D. Wright, *The Jacobian conjecture:
  reduction of degree and formal expansion of the inverse*, Bull. Amer.
  Math. Soc. 7 (1982), 287–330.
- [BE05] M. de Bondt, A. van den Essen, *A reduction of the Jacobian
  conjecture to the symmetric case*, Proc. Amer. Math. Soc. 133 (2005),
  2201–2205.
- [vdE10] A. van den Essen, *The amazing image conjecture*,
  [arXiv:1006.5801](https://arxiv.org/abs/1006.5801) (2010).
- [Z07] W. Zhao, *Hessian nilpotent polynomials and the Jacobian
  conjecture*, Trans. Amer. Math. Soc. 359 (2007), 249–274.
  [arXiv:math/0409534](https://arxiv.org/abs/math/0409534).
