# 05 Batch runner, answers and tracing

Status: done
Track: A (agent core)
Blocked by: 04

Spec: [`../spec.md`](../spec.md) §9.

## What

`run.py` (`pm-agent run` and `pm-agent eval`), `render.py`, cost and latency accounting,
concurrency, the per-case timeout, failure answers, and Phoenix trace ids.

## Acceptance criteria

- [ ] `pm-agent run` on a temp folder with three cases (two public, one raw-mode junk folder) writes all five files for each, with concurrency 3.
- [ ] A forced exception in one case still produces "Escalated: system failure" with the error, and the other cases are unaffected.
- [ ] `ANSWER.md` follows the submission-template headings; held actions read "awaiting property manager approval".
- [ ] `pm-agent eval --only <id>` runs one decision point into `runs/<id>/` (`live`).
- [ ] With Phoenix running, each case appears as one trace in project `pm-agent`.
