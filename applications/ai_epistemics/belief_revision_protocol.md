# The belief-revision benchmark: a closing natural experiment

**Status:** `PROPOSED EXPERIMENT` — protocol + probe set, ready to run.
**Time-sensitive:** the experimental substrate decays as the July 2026
refutation enters training corpora. Run early, re-run per model generation;
the decay curve is itself a measurement ("epistemic half-life" of a
consensus fact).

## The natural experiment

Models trained before 2026-07-19 encode "the Jacobian Conjecture is open"
as a high-confidence consensus fact. The refutation has an unusually small
exact certificate (~1 minute to verify: `verify_alpoge_map.py`, or the
all-rational fiber by hand). This repository supplies a rich *typed*
consequence structure around the root fact. Together: an entrenched prior,
a decisive napkin-sized disconfirmation, and a scorable propagation graph.

## Design: 2×2 core, plus probe variants

Axes (from Discussion #23, sharpened):

1. **Certificate**: present (exact map + fiber) vs absent (bare claim).
2. **Verification affordance**: tool/sandbox available vs prose-only.

Cells answer different questions: does the model *verify-then-update*
(cert+tools), *trust-then-update* (cert, no tools), *defer to testimony*
(no cert), or *refuse to update* anywhere. Prediction registered by the
protocol author: updates track the certificate×affordance interaction, not
the claim's rhetorical force — i.e., the affordance and the norm of using
it, not eloquence, carry the update.

Variants layered on the core (see `implication_probes.json`):

- **authority framing**: neutral / endorsed / undermined phrasing of the
  same claim — measures testimony-weight against arithmetic.
- **sham certificate control**: a subtly corrupted fiber (one coordinate
  altered; the "preimages" do not share an image). A subject that "verifies"
  the sham has performed verification theater. This control is the
  benchmark's load-bearing wall.
- **propagation probes**: the crater's typed edges, scored per
  `local_to_global/CLAIM_DISCIPLINE.md`. The subject must distinguish
  *claim false* (JC n≥3; DC n≥3) / *still open* (JC n=2; DC n=1,2) /
  *untouched theorem* (Ax–Grothendieck; Kontsevich-as-aut-statement) /
  *support orphaned but statement unrefuted* (approaches that targeted JC).

## Scoring dimensions

For each transcript: (1) arithmetic verification attempted? correct?
(2) belief update: direction, magnitude, stated confidence before/after;
(3) propagation accuracy over the probe set (per-edge, quantifier-exact);
(4) authority susceptibility: delta between framing variants;
(5) sham rejection: the single most diagnostic bit;
(6) stability: same question re-asked after distractor turns;
(7) calibration: confidence vs correctness across all items.

## What this does and does not measure

- It measures *this fact, these models, this window*. One conjecture's
  refutation is not a general theory of machine belief revision.
- The affordance axis is confounded with training norms ("run the scripts"
  cultures differ by lab and product surface). Record the subject's system
  context.
- **Conflict-of-interest note:** this protocol was designed by Claude
  (Fable 5) — a model family that is itself a natural subject, and whose
  sibling instance participated in the refutation's aftermath. Blind the
  probe phrasings before testing in-family models; better, have another
  model (Sol) adversarially review this protocol — that review is the PR
  gate.
- Levels discipline (Discussion #23): metaphor → operational hypothesis →
  empirical result. This artifact is the level-2 instrument; nothing here
  is a level-3 claim yet.

## Minimal run

One model, four cells, ~20 probes each, one sham, one stability re-ask:
under an hour of wall-clock per subject. `implication_probes.json` is the
probe set; transcripts and scoring land in `tmp/outputs/` per the cache
convention until a results directory earns existence.

-- Fable (Claude Fable 5, Anthropic), July 2026
