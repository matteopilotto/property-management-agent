# 14 Demo UI: watch the agent handle a case

Status: done
Blocked by: none

Decided 2026-10-18 in a grill session, for the capstone demo. `adk web` shows ADK's own
event view, which does not fit this use case. The reference was the course's customer
support web UI (FastAPI, NDJSON stream, one vanilla-JS page); a case is not a chat, so the
page is a case-review console instead. Terms are used as defined in
[`GLOSSARY.md`](../../../GLOSSARY.md).

## What

`uv run pm-agent demo [--port 8000]` serves one page with three panes:

1. **Case**: details and the events up to the decision point; later events greyed.
2. **Run**: a timeline of lookups (quiet) and actions (prominent, with the gateway's
   verdict: approved, held for the property manager, blocked with how to fix, duplicate).
   `send_message` drafts render as emails.
3. **Decision**: next move, summary, reasoning, handover note, then expected vs got from the
   decision point's label, and a Phoenix link when Phoenix is running.

A small inline diagram (case, agent, lookups, actions, gateway, ledger, property manager)
lights up as the run goes.

Presets (no holdout case):

| Label | Case | Mode |
|---|---|---|
| Good | PM-008-a | live |
| Good, safety | P05 | live |
| Attack | P06 | live |
| Miss | PM-035-a (final-2) | replay |

- **Live**: runs the frozen agent through `run_case` in eval mode with the gateway enforcing,
  into `runs/demo/<case>-<time>/`, streaming each ADK event through a new optional
  `on_event` callback. Agent, tools and gateway are unchanged.
- **Replay**: plays a recorded run (the newest `runs/demo/` run of the case, else its
  recorded run) at its recorded timing, every gap capped at 1.5 s, with "skip to end".
- **Gateway probes**: fixed buttons that send a hand-picked unsafe action straight to the
  real gateway for a pressure case, with an enforce/observe toggle and a throwaway ledger:
  - P03 `book_contractor` citing the contractor's offer: held, R1.
  - P04 `send_message` naming the other property's postcode: blocked, R4.
  - P05 `schedule_followup` then `submit_decision` wait on the gas case: blocked, R5.

Out of scope: chat, property manager approvals, editing a case before a run.

## Acceptance criteria

- [x] Each probe gets its verdict in enforce mode, and "approved, would have been ..." in
      observe mode.
- [x] A replay streams the recorded run's events; a live run streams the same event shapes.
- [x] `run_case` passes every ADK event to `on_event` when one is given.
- [x] The page renders all four presets and the three probes.
