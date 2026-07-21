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

Zhao's Vanishing Conjecture (equivalent to JC) states: for **homogeneous**
P with Δᵐ(Pᵐ) = 0 for all m ≥ 1, one has Δᵐ(Pᵐ⁺¹) = 0 for m ≫ 0. Two facts
from van den Essen's survey ([arXiv:1006.5801](https://arxiv.org/abs/1006.5801),
p. 5–6) make an explicit counterexample a finite object:

- Δᵐ(Pᵐ) = 0 for all m  ⟺  **Hess P is nilpotent** (a finite symbolic check);
- Δᵐ(Pᵐ⁺¹) = 0 for m ≫ 0  ⟺  **z + ∇P is invertible**.

Our P above satisfies the second failure (z + ∇P non-invertible) but **not**
the first hypothesis: Hess P is *not* nilpotent (check 6 — equivalently JH is
not nilpotent, char poly ≠ λ³), and P is inhomogeneous. The missing step is
the classical **Bass–Connell–Wright cubic-homogeneous reduction**: push F
through it to a cubic homogeneous Keller counterexample x + H′ (JH′ nilpotent
by homogeneity) in some dimension N, then apply the same
½⟨x − iy, H′(x + iy)⟩ construction to get a **homogeneous quartic,
Hessian-nilpotent P′ in 2N variables** with z + ∇P′ non-invertible — an
explicit counterexample to the Vanishing Conjecture, with every certificate
finite: nilpotency of Hess P′, the lifted double points, and explicit nonzero
values of Δᵐ(P′ᵐ⁺¹).

The BCW step is explicit but bookkeeping-heavy (each high-degree monomial is
split by adjoining shear variables; all steps are compositions with elementary
automorphisms, so non-injectivity and the Keller property transport
automatically and can be re-asserted by machine at every stage). It is the
natural next artifact for this repository. From the quartic P′, explicit
counterexample data for the Gaussian-moments and Mathieu-style integral
formulations should follow along the routes described in the same survey.
