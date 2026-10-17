# 03 Action gateway and ledger

Status: done
Track: A (agent core)
Blocked by: 01

Spec: [`../spec.md`](../spec.md) §7.

## What

`gateway.py` and `ledger.py`: rules R1–R6, the `enforce` and `observe` modes, ledger
entries, and the tool-result payloads. Pure Python, no ADK imports, so it can be tested
without a model.

## Acceptance criteria

- [ ] Unit tests cover the approved/held/blocked path of each rule, built from real snippets: the case 004 event 2 approval text passes R1; the case 007 invoice £240.00 against the £238.04 quote is held by R3; a message to the landlord quoting another case's postcode is blocked by R4; `wait` with "no hot water" in a visible event is blocked by R5; a repeated identical message is `duplicate`.
- [ ] In `observe` mode every action is `approved` and `would_status` equals the `enforce` status.
- [ ] Each call appends exactly one ledger line with every field from the spec.
