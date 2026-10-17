# 12 Static HTML scoreboard (stretch)

Status: done
Blocked by: 07

## What

`pm-agent board <run_id>` writes one self-contained `board.html` from a run's results, ledgers
and score report: one row per case with next move, actions coloured by gateway status, pass/fail,
cost and latency, and a link to the Phoenix trace. No server, no JS framework. Drop this
ticket if ticket 09 is not finished.

## Acceptance criteria

- [ ] Opens offline in a browser and renders a committed eval run.
