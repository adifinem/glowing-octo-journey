# Claim discipline for cross-domain exploration

This repository is exploratory, but exploration becomes much more useful when every statement carries its epistemic type.

Use the labels below in notes, issues, experiments, and code comments.

## Labels

### `PROVED`

A mathematical statement established by a complete argument or a trusted theorem whose hypotheses have been checked.

Include:

- the exact statement;
- the hypotheses;
- the proof or primary reference;
- any machine artifact that checks the finite algebra.

### `CERTIFIED`

A finite computational claim checked by a replayable script or formal proof.

A certificate proves exactly what its assertions encode. It does not automatically prove the surrounding prose, the faithfulness of a formalization, novelty, or attribution.

### `DERIVED`

A consequence of proved or certified premises through a stated argument.

List every non-machine step. A derivation is only as strong as its weakest bridge.

### `EMPIRICAL`

A numerical or experimental observation with a specified domain, sample, tolerance, and method.

Do not upgrade a large search to a universal claim. Record the searched family as part of the result.

### `CONJECTURE`

A mathematically precise proposition believed to be true but not established.

It should be falsifiable and should name what would count as a witness or proof.

### `HYPOTHESIS`

A proposed mechanism intended to organize experiments. It may be less formal than a conjecture but must still expose possible failure tests.

### `ANALOGY`

A structural resemblance across domains. An analogy may generate experiments, but it transmits no theorem by itself.

Example:

> J-space collisions may be an interpretability analogue of noninjective fibers.

This becomes a hypothesis only after defining a readout map, an equivalence tolerance, and a behavioral distinction.

### `METAPHOR`

Explanatory language with no inferential force.

“Sheets escaping through infinity” is geometrically grounded in this project. “Ideas escaping through latent infinity” is a metaphor until given operational meaning.

### `OPEN QUESTION`

A clearly scoped unknown, preferably with known bounds, obstructions, or proposed certificates.

### `KNOWN FALSE`

A tempting statement contradicted by a theorem, certificate, counterexample, or failed derivation. Keep these visible when they are likely to be rediscovered.

## Bridge ledger

Every cross-domain bridge should answer six questions.

1. **Objects:** What are the objects on each side?
2. **Map:** What construction or correspondence relates them?
3. **Preserved structure:** What is actually preserved?
4. **Lost structure:** What is discarded, weakened, or only local?
5. **Failure test:** What observation would break the proposed bridge?
6. **Status:** Is this proved, certified, empirical, hypothetical, or analogical?

## Example: J-space bridge

- **Objects:** transformer residual states and J-space readouts.
- **Map:** the J-lens projection or causal sensitivity map.
- **Preserved structure:** selected future-token-relevant directions.
- **Lost structure:** concepts outside the lens vocabulary, nonlinear context, and possibly branch-selecting latent variables.
- **Failure test:** find two states with matched J-space readout but reliably divergent downstream behavior.
- **Status:** `HYPOTHESIS`, motivated by an `ANALOGY` to noninjective local-to-global maps.

## Example: normalizing-flow bridge

- **Objects:** source samples and transformed samples under the Alpöge map.
- **Map:** the exact polynomial map `F`.
- **Preserved structure:** local nonsingularity and constant volume scaling.
- **Lost structure:** global injectivity and surjectivity.
- **Failure test:** use a one-branch change-of-variables formula at a target with three preimages.
- **Status:** `CERTIFIED`; see `flow_branch_benchmark.py`.

## Anti-hype rules

- Similar notation is not a bridge.
- Shared vocabulary is not shared mathematics.
- A local linearization is not a global model.
- Algebraic quantization is not automatically physical quantization.
- A verifier establishes its encoded claim, not the entire interpretation wrapped around it.
- Independent-looking scripts that share the same engine are replication, not full methodological independence.
- A model-generated conjecture earns no extra probability from eloquence.

The aim is not to sterilize speculation. It is to let speculation grow roots without pretending the roots are already a forest.

-- GPT-Sol (GPT-5.6 Thinking), July 2026
