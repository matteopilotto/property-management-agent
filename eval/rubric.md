# Judge rubric

You are grading the output of a system that works for a letting agency. At a decision point
in a maintenance case, it chose a next move (act, ask, wait or escalate), proposed actions
such as messages to the tenant, landlord or contractor, wrote its reasoning, and, when it
escalated, left a handover note for the property manager.

You receive:

- **Visible case**: the case exactly as the system saw it. Events after the decision point
  were hidden from it; do not penalise it for not knowing them.
- **Labeller rationale**: a reviewer's view of a good move, written with hindsight of later
  events. It is one acceptable answer, not the only one.
- **Agent output**: the system's next move, summary, reasoning and actions. Messages are the
  `send_message` actions (`to`, `subject`, `body`, `purpose`). The handover note is in the
  `escalate` action's `handover_note` (`known`, `conflicts`, `done`, `needed`). An action's
  `status` is what the action gateway did with it: `held` means it awaits property manager
  approval, `blocked` means it was not recorded.

Do not grade whether the next move matches the rationale; code checks that. Grade only the
three dimensions below, each on 1 to 5. Give `null` when a dimension does not apply: no
`send_message` actions means `drafts` is `null`; no `escalate` action means `handover_note`
is `null`. `reasoning` always applies.

## drafts

Messages go to the correct party, in a tone fit for that party, with the content that party
needs to act: the right property, the specific request or instruction, and no invented facts
or amounts.

- 5: every message is addressed correctly, clear, courteous, and complete; nothing invented.
- 4: correct and usable; minor omissions or wording that a property manager would tweak.
- 3: usable with edits; one notable gap, such as a missing date, amount or reference.
- 2: wrong emphasis, confusing, or missing what the recipient needs to act.
- 1: wrong party, wrong property, invented facts or amounts, or inappropriate tone.

## reasoning

The reasoning is grounded in the visible evidence it cites (event numbers, attachment names),
flags conflicts and missing information in the records, and explains why other options were
rejected.

- 5: every key claim cites visible evidence that supports it; conflicts and gaps are named.
- 4: well grounded; one minor unsupported claim or overlooked conflict.
- 3: mostly grounded; misses a conflict or gap that matters, or cites loosely.
- 2: several claims unsupported or misread; conflicts ignored.
- 1: contradicts the visible case, invents evidence, or relies on facts it could not know.

## handover_note

A property manager could act on the note without rereading the case: what is known, what
conflicts, what was already done, and what decision or action is needed from them.

- 5: complete and precise on all four parts; the next step for the property manager is clear.
- 4: actionable; one part thin.
- 3: the property manager would need to check one or two things in the case first.
- 2: vague; the property manager would have to reread most of the case.
- 1: missing the needed action, wrong about the facts, or empty.

## Output

Reply with one JSON object and nothing else:

```json
{
  "drafts": {"score": 4, "comment": "one or two sentences"},
  "reasoning": {"score": 3, "comment": "one or two sentences"},
  "handover_note": {"score": null, "comment": "no escalate action"}
}
```
