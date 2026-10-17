# Holdout decision points

17 decision points from the 10 holdout Property Management cases in
[`../../docs/holdout.md`](../../docs/holdout.md), labelled after the freeze with
[`../LABELLING.md`](../LABELLING.md) in the spec §10 schema. None is reviewed yet.

Move mix: act 7, ask 6, wait 4, escalate 0. No holdout case has a moment that needs the
property manager, so no escalate label was forced.

`v` is `visible_through_event`; "alt" lists the acceptable alternatives.

| File | v | Move | Alt | Reason |
|---|---|---|---|---|
| PM-003-a | 7 | ask | - | Contractor asks "tell me if it didn't attach", and no estimate is visible: ask for it again. |
| PM-003-b | 17 | act | ask, wait | Approved checkout clean with the invoice "sent to Theo": close-out, no invoice approval without an amount. |
| PM-015-a | 7 | act | ask | Landlord says "get Imogen to have a look": book his named contractor. |
| PM-015-b | 15 | act | ask | £68.97 invoice under another brand after an unpriced inspection: close-out, do not approve. |
| PM-017-a | 8 | ask | - | Landlord points to a switch beside the hob: ask the tenant to try it before any call-out. |
| PM-017-b | 11 | act | - | Tenant found the switch and the fan works: close without payment. |
| PM-021-a | 20 | wait | ask | Lock replaced, office and landlord keys promised for tomorrow: follow up, do not close yet. |
| PM-022-a | 12 | ask | - | "No work results" a day after the locksmith set off: ask what happened. |
| PM-022-b | 16 | wait | ask | Lock changed; new key and invoice promised: follow up for the key, do not close. |
| PM-023-a | 16 | wait | ask | Tenant was texted twice minutes ago to call the locksmith back: dated follow-up. |
| PM-026-a | 22 | ask | act | Visit recorded for 30/08 (a Saturday) while the tenant arranged 8 September: confirm the date. Wait is excluded by R5 ("gas" in the intake Q&A). |
| PM-043-a | 13 | wait | act, ask | Landlord's written approval arrives after the contractor was already instructed: give him time. |
| PM-043-b | 16 | act | ask | Contractor reports the repair done "on November 4th" (impossible date, noise): close-out. |
| PM-046-a | 15 | ask | - | £90 plus VAT hinge quote after an approved look: landlord approval first. |
| PM-046-b | 36 | ask | wait | "No work results" two days after the booked visit: ask the contractor (the agency held five days). |
| PM-050-a | 21 | act | - | Landlord says "Yes please proceed" to the £35 or £90 plus VAT options: instruct. |
| PM-050-b | 35 | act | ask | Invoice from another brand, no amount, dated before the booked visit: close-out, no approval. |

## Least certain

- PM-003-a: the agency approved the estimate it apparently received off-record ("Received :)
  Please proceed"); the agent sees none, so ask is expected and act is not accepted.
- PM-050-b: the invoice predates the booked 8 July visit; close-out follows the recorded
  outcome, but confirming completion first (ask) may be the better move.
- PM-043-a: wait versus confirming the landlord's approval to the contractor (act).
- PM-021-a and PM-022-b: `close_case` is prohibited while promised keys are outstanding,
  although the agency closed within hours once the keys arrived.
