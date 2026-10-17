# 10 Holdout dress rehearsal

Status: done
Blocked by: 09 (the freeze tag must exist)

## What

Only after `git tag freeze`: label the 10 holdout cases with `eval/LABELLING.md` into
`eval/decision_points_holdout/` (a labeller that has not seen the agent's output on them), run
`pm-agent eval` against that folder unattended and timed, score it, and commit the report as
`eval/reports/holdout.md`. No code changes; rerunning the same frozen code on a crashed case is allowed.

## Acceptance criteria

- [ ] The holdout report is committed with wall-clock time, cost and every §2 metric.
- [ ] `git diff freeze -- src/` is empty.
