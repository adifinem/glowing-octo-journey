# glowing-octo-journey

**Machine-verified fallout from the July 2026 refutation of the Jacobian
Conjecture** — a napkin check anyone can run, the geometry of *how* the
counterexample works, and an explicit refutation of the Dixmier Conjecture
for the Weyl algebra A₃.

On July 19, 2026, Levent Alpöge announced an explicit polynomial map
F: ℂ³ → ℂ³ with constant Jacobian determinant −2 that is generically
three-to-one, refuting the 87-year-old Jacobian Conjecture for every
dimension n ≥ 3. Everything in this repository builds on that map, and
**every mathematical claim here is backed by an exact symbolic computation
that ends in an `assert`** — you don't have to trust anyone, including us.
Run the scripts.

## Contents

| Path | What it is |
|---|---|
| [`verify_alpoge_map.py`](verify_alpoge_map.py) | **The napkin check** (~1 min): Jacobian ≡ −2, plus one rational target with three exact preimages. This alone refutes the Jacobian Conjecture for n ≥ 3. |
| [`crater/fiber_geometry.md`](crater/fiber_geometry.md) | **The anatomy of the crater**: the fiber cubic `L·x³ + (4−3BC)·x − 2C = 0`, why sheets can only escape to infinity **in pairs** (no x² term), the fiber-count stratification 3 → 1 → 0, non-injectivity over ℝ with constant Jacobian, and the proof that F omits the entire rational curve **(B²/12, B, 4/(3B))** — the map is not even surjective. |
| [`crater/crater_map.py`](crater/crater_map.py), [`crater/crater_map.png`](crater/crater_map.png) | A picture of the crater: a slice of target space where the omitted point sits exactly at the **cusp** of the rim curve, and the two escaping sheets blowing up to infinity as a path crosses the rim. |
| [`dixmier/dixmier_note.md`](dixmier/dixmier_note.md) | **Draft note**: an explicit non-invertible endomorphism φ of the third Weyl algebra — x_i ↦ F_i, ∂_i ↦ Σ (J⁻¹)ₐᵢ ∂ₐ — refuting the **Dixmier Conjecture (1968)** for all n ≥ 3. The non-surjectivity proof is six lines: normal-order a putative preimage of x₁ and apply it to the constant 1; out falls a polynomial left inverse of F, contradicting the three-preimage point. Physically: the observable algebra of a quantum particle in 3-space admits a strict self-embedding preserving all canonical commutation relations. |
| [`dixmier/verify_dixmier.py`](dixmier/verify_dixmier.py) | **The load-bearing wall** (~3 min): five checks in exact arithmetic — constant Jacobian, complex non-injectivity, *real* non-injectivity, the Weyl-algebra commutation relations `[D_i,F_j]=δ_ij` and `[D_i,D_j]=0`, and the fiber-cubic identity with the omitted curve. |
| [`symmetric/symmetric_note.md`](symmetric/symmetric_note.md), [`symmetric/verify_symmetric.py`](symmetric/verify_symmetric.py) | **A symmetric (gradient) Keller counterexample in dimension 6**: the explicit degree-8 potential P(x,y) = ½⟨x−iy, H(x+iy)⟩ makes z + ∇P a non-injective Keller map with *symmetric* Jacobian — JC fails inside the symmetric class, concretely. The (w, w̄) block-triangularization that proves it is one similarity. Also scopes the next opening precisely: push F through the Bass–Connell–Wright cubic reduction and the same construction yields an explicit homogeneous **counterexample to Zhao's Vanishing Conjecture**. |

## Quick start

```sh
pip install sympy            # 1.12+
python3 verify_alpoge_map.py            # the napkin check
python3 dixmier/verify_dixmier.py       # the whole edifice
pip install numpy matplotlib && python3 crater/crater_map.py   # the picture
```

## Status and honesty

- The counterexample map is **Alpöge's** (announcement July 19, 2026; found in
  collaboration with Claude Fable, Anthropic; manuscript unrefereed at the time
  of writing). Nothing here depends on the unrefereed manuscript — only on the
  displayed map, whose relevant properties the scripts verify from scratch.
- The Dixmier refutation follows the classical DC ⇒ JC bridge (Dixmier 1968;
  van den Essen 2000; Tsuchimoto 2005; Belov-Kanel–Kontsevich 2007), made
  explicit and machine-checked here; full references in the note.
- Still open, untouched by the crater: the **plane Jacobian Conjecture
  (n = 2)**, Dixmier for **n = 1, 2**, and the **Kontsevich conjecture** on
  automorphism groups. The Ax–Grothendieck theorem survives — which is exactly
  why the counterexample had to hide its failure at infinity.

## Provenance

The analysis, constructions, drafts, figures, and verification scripts in this
repository were produced by **Claude (Fable 5, Anthropic)** in conversation
with **[@adifinem](https://github.com/adifinem)**, July 20–21, 2026. Repo
curated by adifinem; the mathematics stands or falls with the scripts, not
with either of us.

## License

MIT — see [LICENSE](LICENSE). Take it, rerun it, extend it. There are at least
two more explicit counterexamples waiting to be extracted from this map
(Gaussian moments; Mathieu's conjecture on compact-group integrals). Leave the
crater nicer than you found it. 🕳️
