# Local-to-global failure atlas

This directory develops a cross-domain research program suggested by the Alpöge map and the surrounding July 2026 work.

The governing question is broader than the Jacobian Conjecture:

> Which local signals genuinely control global structure, and which merely impersonate control until infinity, topology, hidden state, or branch multiplicity enters the room?

The counterexample is unusually portable because it combines an exceptionally strong local certificate with explicit global failure:

- `det J_F = -2` everywhere;
- every differential is invertible;
- exact fibers of cardinality 3, 1, and 0 occur;
- noninjectivity and nonsurjectivity are explicit;
- failure is organized by a concrete nonproperness locus rather than by local folding.

That makes it useful not only as an algebraic-geometric object, but as an adversarial specimen for any field that quietly substitutes local regularity for global reversibility.

## Research lanes

### 1. Witness compilation

The implication crater says which universal statements fall. The next layer should compile the root map through constructive reductions and emit explicit downstream witnesses.

Candidate targets include:

- cubic-homogeneous and Drużkowski-form Keller maps;
- Hessian-nilpotent and Vanishing-Conjecture witnesses;
- Gaussian-moment and Mathieu-type witnesses;
- Poisson and Weyl-algebra endomorphisms;
- Yagzhev-style nonassociative algebra objects.

For each compiler, record not only correctness but distortion:

- dimension blowup;
- degree and coefficient growth;
- preservation or destruction of fiber geometry;
- whether collisions and omitted sets remain visible;
- which steps are exact, constructive, or merely existential.

A reduction can preserve truth while destroying explanation. That loss should be measured rather than hidden.

### 2. Failure ecology

Treat the known map as one organism in a possible family. Useful classification coordinates include:

- generic fiber degree;
- monodromy and Galois group;
- Newton polytopes and weighted gradings;
- nonproperness locus and omitted set;
- real versus complex collision structure;
- behavior under stabilization and tame coordinate changes.

The key question is whether the example is isolated, part of a low-dimensional moduli family, or one point in a much larger basin of constructions.

### 3. Classical and quantum lifts

The cotangent lift

```text
(q, p) -> (F(q), JF(q)^(-T) p)
```

preserves the canonical one-form locally because `JF` is invertible everywhere, while inheriting global noninjectivity from `F`. This is a concrete polynomial local canonical transformation that is not globally reversible.

Questions worth separating carefully:

- algebraic symplectic or Poisson preservation;
- global canonical invertibility;
- realizability by Fourier integral operators;
- compatibility with real structures and star operations;
- extension to analytic or C*-algebraic CCR settings;
- whether the Weyl self-embedding has a useful index matching the classical degree 3.

The algebraic Weyl result is not automatically a physical quantum result. The boundary between those categories is itself one of the interesting objects.

### 4. Inverse problems and machine learning

The map is an exact adversarial benchmark for systems that infer global invertibility from local Jacobian information.

It offers:

- a constant log-determinant;
- exact collisions;
- multiple inverse branches;
- omitted targets;
- branch-count changes caused at infinity;
- symbolic ground truth rather than numerical ambiguity.

Possible uses:

- normalizing-flow validation;
- neural inverse solvers;
- interval and SMT injectivity checks;
- out-of-distribution inversion;
- multimodal posterior recovery;
- density estimation with finite-to-one maps.

See `flow_branch_benchmark.py` for the smallest exact demonstration: the correct pushforward density is a sum over all inverse branches, while a one-root solver undercounts it.

### 5. Interpretability and J-space

The relationship to J-space is methodological, not a theorem-level identification.

J-space uses local causal sensitivity to expose a compact internal workspace. The Jacobian counterexample warns that even exceptionally informative local sensitivity can fail to identify global state uniquely.

Experiments suggested by that tension:

- search for distinct internal states with nearly identical J-space readouts;
- find identical readouts followed by different downstream behavior;
- test whether hidden variables outside J-space select among behavioral branches;
- examine loops in activation space that return to similar readouts but permute latent interpretations;
- test for internal activation escape while observable readouts remain bounded;
- measure belief revision when a model is shown a compact certificate contradicting a strong pretrained prior.

These are analogies until operationalized. `CLAIM_DISCIPLINE.md` defines the labels used to keep them from quietly mutating into claims.

### 6. Scientific dependency systems

The crater suggests a scientific package manager:

- claims are nodes;
- implications are typed edges;
- quantifiers and parameter maps are part of the type;
- witnesses and certificates are build artifacts;
- changed roots trigger rebuilds;
- failed support can become orphaned without making the target false.

A mature system would record exact quantifier structure, constructive content, machine-checkable boundaries, provenance, and the amount of information lost by each reduction.

## Practical priorities

The most promising near-term work appears to be:

1. compile one full constructive reduction into a new exact witness;
2. formalize the degree-3 classical/quantum index question;
3. package the map as a benchmark for finite-to-one density transforms and inverse solvers;
4. design an interpretability experiment with explicit collision and nonproperness analogues;
5. extract the exact obstruction that prevents the three-dimensional escape mechanism from descending to the plane case.

The point is not to force all of these fields into one grand theory. It is to use one unusually clean failure object as a probe and see which disciplines reveal the same structural scar.

-- GPT-Sol (GPT-5.6 Thinking), July 2026
