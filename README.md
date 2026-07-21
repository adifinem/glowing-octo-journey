# glowing-octo-journey

**Machine-verified fallout from the July 2026 refutation of the Jacobian
Conjecture** — a napkin check anyone can run, the geometry of *how* the
counterexample works, and an explicit refutation of the Dixmier Conjecture
for the Weyl algebra A₃.

On July 19, 2026, Levent Alpöge announced an explicit polynomial map
F: ℂ³ → ℂ³ with constant Jacobian determinant −2 that is generically
three-to-one, refuting the 87-year-old Jacobian Conjecture for every
dimension n ≥ 3. Everything in this repository builds on that map, and
**every load-bearing claim is backed by an exact symbolic computation that
ends in an `assert`** — the geometric narrative is interpretation layered on
those certificates, and each note says which is which. You don't have to
trust anyone, including us. Run the scripts.

## Contents

| Path | What it is |
|---|---|
| [`verify_alpoge_map.py`](verify_alpoge_map.py) | **The napkin check** (~1 min): Jacobian ≡ −2, plus one rational target with three exact preimages. This alone refutes the Jacobian Conjecture for n ≥ 3. |
| [`crater/fiber_geometry.md`](crater/fiber_geometry.md) | **The anatomy of the crater**: the fiber cubic `L·x³ + (4−3BC)·x − 2C = 0`, why sheets can only escape to infinity **in pairs** (no x² term), the fiber-count stratification 3 → 1 → 0, non-injectivity over ℝ with constant Jacobian, and the proof that F omits the entire rational curve **(B²/12, B, 4/(3B))** — the map is not even surjective. |
| [`crater/crater_map.py`](crater/crater_map.py), [`crater/crater_map.png`](crater/crater_map.png) | A picture of the crater: a slice of target space where the omitted point sits exactly at the **cusp** of the rim curve, and the two escaping sheets blowing up to infinity as a path crosses the rim. |
| [`crater/real_crater.md`](crater/real_crater.md), [`crater/verify_real_crater.py`](crater/verify_real_crater.py), [`crater/real_crater_map.png`](crater/real_crater_map.png) | **The real crater, classified**: over ℝ³ the map is 3-to-1 where disc = −4L(4−3BC)³ − 108L²C² > 0 and 1-to-1 where disc < 0; odd fibers force a real preimage (parity!), so **F(ℝ³) misses exactly the real floor curve**. The 3-to-1 wedge pinches shut at the omitted point. |
| [`crater/fiber_structure.md`](crater/fiber_structure.md), [`crater/verify_shape.py`](crater/verify_shape.py) | **The fiber structure + surjectivity theorem**: disc = **−4·L·S²** with S = 27AC²−9BC+8; the floor curve is exactly {L=0}∩{S=0}; shape-position Gröbner bases (in x off {S=0}, in y on it) make preimages ↔ roots explicit on every stratum. Fibers have 3, 1, or 0 points — never 2 — the **real count is decided by the sign of L alone**, and **F(ℂ³) and F(ℝ³) are exactly the complements of the floor curve**. Eight machine checks. |
| [`crater/monodromy.md`](crater/monodromy.md), [`crater/verify_monodromy.py`](crater/verify_monodromy.py) | **Full S₃ monodromy**: the 3-sheeted covering over ℂ³∖{L=0} has monodromy group S₃ (irreducible cubic + non-square discriminant (2S)²·(−L)); the rim carries a transposition of the escaping pair, the S-wall carries nothing, and rim loops on one generic line generate the whole group. **The discriminant factorization *is* the monodromy.** Non-normal — the three sheets are globally inequivalent. |
| [`NOTES.md`](NOTES.md) | **The research log**: proved facts with pointers, dead ends with reasons, traps, suspicions, and sourced leads. Read this before working on an opening. |
| [`dixmier/dixmier_note.md`](dixmier/dixmier_note.md) | **Draft note**: an explicit non-invertible endomorphism φ of the third Weyl algebra — x_i ↦ F_i, ∂_i ↦ Σ (J⁻¹)ₐᵢ ∂ₐ — refuting the **Dixmier Conjecture (1968)** for all n ≥ 3. The non-surjectivity proof is six lines: normal-order a putative preimage of x₁ and apply it to the constant 1; out falls x₁ as a polynomial in F₁, F₂, F₃ — impossible, because the displayed collision has two preimages with different x₁. Physically: the observable algebra of a quantum particle in 3-space admits a strict self-embedding preserving all canonical commutation relations. |
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
- The Dixmier refutation does not merely cite the classical DC/JC
  relationship (Dixmier 1968; van den Essen 2000; Tsuchimoto 2005;
  Belov-Kanel–Kontsevich 2007): the Jacobian-to-Weyl construction is applied
  explicitly to this map, its commutation relations are machine-checked, and
  the resulting endomorphism is shown directly to be non-surjective. Full
  references in the note.
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

## Openings

Precisely-scoped unfinished business — an explicit Vanishing-Conjecture
counterexample (the BCW wall is analyzed, the certificates are designed),
the unconditional real classification, the index of the quantum
self-embedding, and the plane case — lives in [OPENINGS.md](OPENINGS.md).

## License

MIT — see [LICENSE](LICENSE). Take it, rerun it, extend it. There are at least
two more explicit counterexamples waiting to be extracted from this map
(Gaussian moments; Mathieu's conjecture on compact-group integrals). Leave the
crater nicer than you found it. 🕳️
