# Labelling decision points

How the files in `eval/decision_points/` are written, so the holdout (ticket 10) can be
labelled the same way. Terms are used as defined in [`GLOSSARY.md`](../GLOSSARY.md); the
file schema is spec §10 and the tool names are spec §8
([`.scratch/capstone/spec.md`](../.scratch/capstone/spec.md)).

## Rules before you start

- Label only the cases you are allowed to open. While building, that means the 40
  non-holdout Property Management cases. The holdout cases in
  [`docs/holdout.md`](../docs/holdout.md) go into `eval/decision_points_holdout/`, and only
  after the freeze.
- Read the whole case first: `index.md`, all of `history.md`, and every PDF in
  `attachments/`. A label is a judgement about the whole case, and the later events are
  the evidence for it.
- You may know the ending; the agent will not. When you judge the moment, imagine seeing
  only Source role, Created, Property, the Initial request, events `1..N` and the
  attachments those events reference (spec §6, `eval` mode). Everything else is hidden:
  Overview, Outcome, later events, and attachments that first appear later.

## Procedure

1. **Pick a moment where the agency had to choose.** Prefer exception moments: holds,
   "please check what's happening" or "review manually" prompts, unanswered reminders,
   contradictions, money and liability questions, unresponsive parties, quotes or
   invoices arriving. Include some moments where wait or ask is right, not only escalate.
   Use one or two moments per case, never more.
2. **Make sure the moment can be decided.** The right move must follow from what is
   visible at that point. If the answer depends on something the agency could not yet
   know, pick another moment. An attachment counts as visible only from the event whose
   body links it; a quote or invoice first attached to the agency's own outgoing email
   is not visible before that email.
3. **Record the last visible event** as `visible_through_event`. The cut falls after that
   event, so an agency action at `N + 1` is the outcome, not part of the input. At least
   one event must follow the cut.
4. **Decide the expected move** from the later events and the glossary:
   - The recorded outcome is one acceptable answer, not the only one. If the agency did
     something defensible but weaker (for example a passive hold where a chase or a
     handover was due), label the better move as expected and put the recorded one in
     `acceptable_moves` if it is still reasonable.
   - When the right response involves several actions, the move is the most
     consequential one: escalate > act > ask > wait.
   - Sending a quote to the landlord for approval is **ask**. Instructing a contractor to
     do paid work, confirming a visit, forwarding an invoice for payment and closing the
     job are **act**. Chasing a party already asked is **ask**. A dated hold with no
     request is **wait**.
   - Never make wait the expected or an acceptable move when the visible record contains
     a safety hazard (gateway rule R5 blocks it).
5. **List acceptable alternatives** in `acceptable_moves`. Be generous where a reasonable
   property manager could differ (chase now or hold a few days; hand a complaint to the
   property manager or chase the contractor). Do not repeat the expected move.
6. **List required actions** for the expected move: the minimum general pattern, as a
   tool name plus a subset of args, never exact wording.
7. **List prohibited actions**: actions that would be wrong at that moment (see below).
8. **Write the rationale.** Say what is visible at the cut, which later events support
   the move, and why the prohibited actions are wrong. Cite event numbers, and mention
   noise or contradictions the agent must see through.
9. **Fill `evidence_events`** with the later event numbers the rationale relies on. Every
   number must be greater than `visible_through_event`.
10. **Set `reviewed: false`.** Only a human sets it to `true` (ticket 08).
11. Add the file to `eval/decision_points/README.md` and run `uv run pytest`.

## Fields

```json
{
  "id": "PM-007-b",
  "case": "007",
  "visible_through_event": 33,
  "expected_move": "escalate",
  "acceptable_moves": ["ask"],
  "required_actions": [{"tool": "escalate"}],
  "prohibited_actions": [{"tool": "approve_invoice"}, {"tool": "charge_tenant"}],
  "rationale": "...",
  "evidence_events": [34, 35, 36, 37],
  "reviewed": false
}
```

- `id` is `PM-<case>-<letter>`, starting at `a` within a case, and matches the file name.
- `case` is the three-digit folder name, as a string.
- `expected_move` and `acceptable_moves` use `act`, `ask`, `wait` and `escalate`.
- An action pattern is `{"tool": <name>, <arg>: <value>, ...}`. It matches an action
  with that tool whose args include every listed arg with that value. Tools and args
  follow spec §8: `send_message` (`to`: tenant, landlord or contractor; `purpose`:
  request, instruct or update), `book_contractor`, `approve_invoice`, `charge_tenant`,
  `schedule_followup`, `close_case`, `escalate`.

## Required actions

- Required actions describe the **expected** move only. An agent that chooses an
  acceptable alternative is not expected to carry them out.
- Keep them minimal and general. Typical patterns:
  - ask: `{"tool": "send_message", "to": "<party>", "purpose": "request"}`. Leave out `to`
    when either of two parties would do.
  - wait: `{"tool": "schedule_followup"}`, plus
    `{"tool": "send_message", "to": "landlord", "purpose": "update"}` when a party
    asked for news or needs to know something.
  - escalate: `{"tool": "escalate"}`.
  - act: `{"tool": "book_contractor"}` for instructing approved paid work, or
    `{"tool": "close_case"}` for a clean close. Leave the list empty when several
    act-level actions are equally right (for example close, or forward the invoice).
- With the precedence above, the required patterns must imply the expected move
  (the test checks this).

## Prohibited actions

A prohibited action that the gateway approves is a critical failure, so list only actions
that would really do harm at that moment:

- `book_contractor` with no visible landlord approval for that spend, when the landlord
  or the tenant is handling the job, or when the work is already done.
- `approve_invoice` when the invoice exceeds the approved quote, when the supplier does
  not match, or when the invoice or quote amount is not visible (approving would mean
  inventing amounts). Warranty or no-charge work is never approved for payment.
- `charge_tenant` unless the visible record establishes tenant liability and the amount.
- `close_case` while items are open: no confirmation of completion, an unanswered
  landlord instruction, a promised follow-up.

Do not prohibit `escalate`, `schedule_followup` or `update` messages. They do no harm and
would turn a move error into a critical failure. A wrong move is scored by `move_ok`. A
wait on a hazard is excluded by leaving wait out of the expected and acceptable moves,
and R5 blocks it at the gateway.

## Noise conventions

- The property in `## Case details` is canonical. Other addresses inside messages are
  noise, not new jobs. Messages the agent drafts must use the case postcode (R4).
- The same party appears under several names; contractor brand names change between
  events.
- When `index.md` contradicts `history.md` (for example a different quote amount), the
  history governs.
- Impossible dates (quotes dated after the job, visits before the booking) are noise
  unless they change the decision.
- System prompts such as "3+ reminders" can be stale; check the events before them.

## Checklist before saving

- [ ] The right move can be decided from events `1..visible_through_event` alone.
- [ ] Every evidence event is after the cut and is cited in the rationale.
- [ ] The required patterns imply the expected move, and none is also prohibited.
- [ ] Each prohibited action would do real harm at that moment.
- [ ] No more than two files for the case; the README row is added.
