# 09 Baseline eval, ablation and fixes before freeze

Status: ready-for-agent
Blocked by: 05, 07, 08

Spec: [`../spec.md`](../spec.md) §2, §10.

## What

Run `pm-agent eval` twice in `enforce` mode and once in `observe` mode, then score with the
judge and with `--compare`. Read the worst failures in Phoenix, fix general causes (instruction,
playbook, tools, gateway), never case-specific patches, and rerun the whole eval after each
change to catch regressions. Stop at 12:30 on 2026-10-18 regardless. Commit the final reports
in `eval/reports/` and write `eval/reports/SUMMARY.md` with the lower of the two enforce runs,
the ablation numbers, and the ids of one success and one failure trajectory for the demo.

## Acceptance criteria

- [ ] Reports for both enforce runs and the observe run are committed.
- [ ] `SUMMARY.md` states every §2 metric against its threshold, including misses.
- [ ] Gates pass; then `git tag freeze` on `capstone`.
