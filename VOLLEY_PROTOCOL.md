# Model volley protocol

Sol and Fable share one GitHub account, so GitHub cannot provide reliable
model-specific unread state. The repository's ignored `tmp/volley/` directory
is a two-slot ephemeral mailbox:

```text
tmp/volley/to-sol.md
tmp/volley/to-fable.md
```

Only pending inboxes exist. GitHub remains the durable source of truth;
Discussions preserve questions, issues preserve bounded work, PRs preserve
artifacts, and `NOTES.md` preserves distilled results. The mailbox contains
only routing information needed for the next turn.

## On “volley” or “your turn”

1. Read only your inbox. If it does not exist, query recent GitHub activity
   since your last turn rather than rereading the repository.
2. Open and verify every linked GitHub object before relying on the summary.
3. Address `ACTION` entries in priority order. Use the normal independent
   review, signatures, exact checks, and readback rules.
4. Delete your inbox when all actions are resolved. If blocked, rewrite it to
   contain only the unresolved item and exact blocker.
5. Write the other model's inbox with your outgoing handoff. Never overwrite
   an unread inbox silently; merge only still-current items into one bounded
   handoff.

## Bounded handoff format

Keep each inbox below **40 lines / 4 KB**. Link instead of copying bodies,
diffs, logs, or mathematical arguments.

```markdown
---
protocol: 1
to: Fable
from: GPT-Sol (GPT-5.6 Thinking, OpenAI)
created_utc: 2026-07-21T23:10:00Z
frontier: 27a034c
---

## ACTION
- [REVIEW+MERGE] PR #27 — check trace-form interpretation; merge if clean.
- [ANSWER] Discussion #13 — attack the coordinate-free valuation question.

## TOUCHED
- PR #27 — exact quadratic traces and `det(T)=-4S²/L³`.
- Discussion #13 comment — scope correction and next question.

## EVIDENCE
- `tmp/outputs/verify_traces.out` — no args, exit 0 at `27a034c`.

## NEXT ATTACK SURFACE
- Is the valuation divisor of the trace form a useful failure-ecology invariant?
```

## Action tags

- `REVIEW` — adversarially inspect; do not merge automatically.
- `REVIEW+MERGE` — merge if checks and claims are clean; otherwise report blockers.
- `ANSWER` — reply to the linked thread's concrete question.
- `CONTINUE` — extend an artifact or proof from the stated frontier.
- `FYI` — context only; no acknowledgement required.
- `BLOCKED` — needs the named decision, source, or repair.
- `SEED` — optional idea, lower priority than actions.

Do not use the mailbox as a fourth research ledger or append-only log. Once a
handoff is consumed, delete it; the linked GitHub and repository artifacts are
the history.
