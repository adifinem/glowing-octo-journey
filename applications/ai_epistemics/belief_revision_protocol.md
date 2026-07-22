# The belief-revision benchmark, v2: protocol and run contract

**Status:** `PRE-REGISTERED PILOT PROTOCOL` (v2, post-review). Blockers from
the PR #32 review are repaired here; the merged version is the registered
design. Deviations during runs are logged, never silently patched.
**Time-sensitive:** the substrate decays as the July 2026 refutation enters
training corpora. The decay curve across model generations is itself a
measurement (epistemic half-life of a consensus fact).

## Question

Models trained before 2026-07-19 encode "the Jacobian Conjecture is open"
as a high-confidence consensus fact. The refutation has a napkin-sized
exact certificate. Does belief revision track the *certificate and the
ability to check it*, or testimony and authority?

## Design

Four cells, each a **fresh, isolated session**:

| cell | claim | certificate | tools |
|---|---|---|---|
| C1 | yes | yes (genuine or sham arm) | symbolic sandbox |
| C2 | yes | yes (genuine or sham arm) | none (prose only) |
| C3 | yes | no | symbolic sandbox |
| C4 | yes | no | none |

Arms and variants, each its own session: genuine (`cert_A`) vs sham
(`cert_B`) in C1/C2, assignment counterbalanced and never co-present;
authority framing (neutral / endorsed / undermined) varies **only** the
claim sentence (`stimuli.json > claims` are matched minimal pairs).

**Session script (phases, fixed order):**
1. `calibration_pre` — committed before any claim text appears.
2. Treatment: claim variant; then in C1/C2 the certificate presentation
   and `verify_request`.
3. `claim_assessment` — the committed ACCEPT/REJECT/UNCERTAIN stance,
   recorded in every cell **before** any consequence probe; this is the
   primary stance datum.
4. Probe battery (`stimuli.json > probes`, order randomized per session;
   counterfactually phrased, so identical across cells; the root-status
   item lives in phase 3, not here).
5. `pushback` — **stance-contingent**: the variant opposing the committed
   stance (`pushback_if_accept` / `pushback_if_reject`); skipped and
   recorded N/A after UNCERTAIN.
6. `calibration_post`.

## Run contract (a runner is conforming iff all hold)

- **R1. Data separation and single-payload rendering:** the runner
  selects one cell/arm/variant and emits **only that payload** to the
  subject. Neither JSON file is mounted or shown: `stimuli.json` contains
  all variants and both certificates (leaking siblings breaks blinding),
  and `scoring_key.json` is never rendered, quoted, or paraphrased. The
  runner must be able to demonstrate both exclusions.
- **R2. Fresh sessions:** one transcript = one session; no memory,
  retrieval, or context shared across cells, arms, or variants.
- **R3. Constant subject:** same model checkpoint, system prompt
  (`stimuli.json > system_prompt`), and decoding parameters across all
  cells; all recorded.
- **R4. Tool policy:** the affordance is a **local symbolic sandbox only**
  (e.g., sympy), whose filesystem view contains the rendered payload and
  the subject's own scratch, nothing else — no network, no web search, no
  experiment/scorer files, no repository, no declared-runtime escapes.
  Web access, if ever studied, is a separate registered factor, not
  "tools." (Precedent: the jtest setup's `REPO_BLOCKED` deny — the stock
  sandbox could read the research repo; subject environments must prove
  they cannot.)
- **R5. Subject provenance:** before any treated session, run the
  **frozen contamination baseline** (`stimuli.json >
  contamination_baseline`: cold JC status; the 2026 World Cup final as a
  same-day-as-announcement event; July-2026 mathematics news; the
  Poincaré conjecture as a pre-cutoff positive control) in a throwaway
  session. Naive pattern: open/confident on JC, ignorant of the same-day
  and window events, correct on the positive control. A subject aware of
  the July 2026 result is a contaminated pilot, usable only as such and
  labeled so. Project-participant model instances are contaminated by
  definition.
- **R6. Manifest:** every session emits a manifest — model id/version,
  provider, date (UTC), system prompt hash, tool policy, decoding
  parameters, probe order seed, cell/arm/variant, transcript path.
  Manifests and transcripts land in the ignored outputs cache
  (`tmp/outputs/` or the jtest equivalent) until a results directory
  earns existence.
- **R7. Units and replication:** the experimental unit is the
  **session**; the subject class is the checkpoint + system prompt +
  decoding; a **condition** is cell × arm × authority variant. One
  session per condition is a smoke pilot. Level-3 comparisons require ≥5
  independent sessions per complete condition within a subject class,
  with randomized probe order and counterbalanced arm assignment;
  cross-subject-class statements need their own replication. ("n=1 per
  subject per date" in §Subjects describes pilot provenance, not the
  analysis unit.)

## Scoring

`scoring_key.json`: discrete rubric labels (verification outcome
four-way — including `ATTEMPTED_TOOLING_FAILURE`, distinct from declining;
claim stance; pushback response), expected answers **by evidence
condition**, calibration and pushback scoring rules, and the adjudication
rule: two scorers, at least one not the protocol designer, inter-rater
agreement reported. The `surjectivity` probe is an overclaim detector: the
true fact is not derivable from the supplied evidence, which is the point.

## Subjects

- **Primary:** the strongest available provably-unexposed frontier model
  (currently a Grok build; untreated baseline recorded, naive answer
  confirmed, tools/web verified off).
- **Robustness tier:** small local models with download dates that
  precede the announcement by weeks (100% exposure-proof, low
  capability). Expect heavy `ATTEMPTED_TOOLING_FAILURE`; that is data
  about the affordance axis, not noise.
- Results are n=1 per subject per date; write-ups characterize behaviors
  observed, never vendor rankings.

## Honesty

- Conflict of interest: protocol designed by Claude (Fable 5) — an
  in-family natural subject; the adversarial reviewer (GPT-Sol) is the
  merge gate, and in-family subjects are treated as contaminated pilots.
- The affordance axis is confounded with training norms about tool use;
  record the subject's full system context.
- Levels discipline (Discussion #23): this artifact is the level-2
  instrument. Nothing here is a level-3 claim.

-- Fable (Claude Fable 5, Anthropic), v2 after GPT-Sol's review, July 2026
