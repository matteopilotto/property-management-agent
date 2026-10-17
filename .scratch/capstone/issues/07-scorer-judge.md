# 07 Scorer, judge and report

Status: ready-for-agent
Track: B (eval)
Blocked by: 01, 06 (the scorer needs run output from 05 only for its live check)

Spec: [`../spec.md`](../spec.md) §2, §10.

## What

`eval/score.py` (deterministic metrics, thresholds, exit code, the ablation view),
`eval/judge.py` and `eval/rubric.md` (the OpenAI judge, reported only), and report rendering to
`eval/reports/<run_id>.md` and `.json`. Wire `pm-agent score <run_id> [--judge]
[--compare <observe_run_id>]`.

## Acceptance criteria

- [ ] Unit tests on hand-made `result.json` and `ledger.jsonl` fixtures cover: move matching with alternatives, a prohibited action that was held (not critical) vs approved (critical), arg-subset pattern matching, and threshold failure giving a non-zero exit.
- [ ] `--compare` prints the observe run's unsafe proposals next to the enforce run's approved prohibited actions.
- [ ] The judge is mocked in tests, and the `live` test scores one decision point.
- [ ] The report includes the §2 table, per-decision-point rows, the five worst failures and total cost.
