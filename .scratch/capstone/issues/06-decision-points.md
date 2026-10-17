# 06 Label the eval decision points

Status: done
Track: B (eval)
Blocked by: none

Spec: [`../spec.md`](../spec.md) §10, glossary moves in [`GLOSSARY.md`](../../../GLOSSARY.md).

## What

This is judgement work, not code. Write `eval/LABELLING.md` (the procedure below, so the
holdout can be labelled the same way later), then read each of the 40 non-holdout Property
Management cases in full and write one or two decision points per case as
`eval/decision_points/PM-<case>-<letter>.json` in the spec's schema.

Never open the holdout cases in `docs/holdout.md`, any other branch, `teams/`, `official/` or `reconstructed/`.

Procedure: pick a moment where the agency had to choose; record the last visible event; decide
the expected move from the events that follow (the recorded outcome is one acceptable answer,
not the only one); list acceptable alternatives; list required and prohibited action patterns
using the tool names from spec §8; cite the later events in `rationale` and `evidence_events`;
set `reviewed: false`. Favour exception moments. Aim for a move mix with at least 5 each of
act, ask and escalate, and at least 3 wait.

## Acceptance criteria

- [ ] At least 40 files, at most 2 per case, every non-holdout case used at least once.
- [ ] Every file validates against the schema (add `tests/test_decision_points.py`, which also asserts that no file references a holdout case).
- [ ] The move mix meets the minimums above.
- [ ] `eval/decision_points/README.md` lists every file with its move and a one-line reason, for the human review in ticket 08.
