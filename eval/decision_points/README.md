# Decision points

62 decision points from the 40 non-holdout Property Management cases, written with
[`../LABELLING.md`](../LABELLING.md) in the spec §10 schema. None is reviewed yet
(ticket 08).

Move mix: act 22, ask 24, wait 11, escalate 5.

`v` is `visible_through_event`; "alt" lists the acceptable alternatives.

## Suggested for human review (ticket 08)

Spread across the moves, with the labels I was least sure about first:

| File | Move | Why review it |
|---|---|---|
| PM-036-a | escalate | Weakest escalate: the only support is a property manager's apology note (031); chasing the contractor may be enough. |
| PM-047-b | escalate | The record shows only passive holds and no handover; escalate rests on the playbook's "escalate after repeated silence". |
| PM-020-a | escalate | Unapproved dog flap after a "no issues" report: escalate, or simply ask the landlord? |
| PM-007-b | escalate | Overage is only £1.96 (£240.00 against £238.04) and the agency closed; is a supplier and amount mismatch worth a handover? |
| PM-040-a | wait | Labelled against the recorded outcome: the agency closed, and `close_case` is prohibited because the landlord's approved inspection was left open. |
| PM-025-a | wait | Oven fault: "stopped heating up" could trip a loose R5 hazard lexicon, which would block wait. |
| PM-032-a | act | A thumbs-up emoji treated as quote approval; is ask (confirm in words) better? |
| PM-033-b | act | The completion email names another property; is closing on it right, or should the contractor confirm first? |
| PM-014-a | ask | Glass-shatter risk with the landlord deferring a month: ask the tenant to try the workaround, or escalate? |
| PM-006-a | ask | Three unanswered reminders on a vacant flat: chase (expected) or hold (what happened)? |

Also worth a look: PM-002-b (a system glitch on a closed job labelled escalate) and
PM-008-b (landlord known to pay slowly; escalate is accepted).

## All files

| File | v | Move | Alt | Reason |
|---|---|---|---|---|
| PM-001-a | 19 | wait | ask | Landlord sourcing his own gardener's quote; the 3-day timer has lapsed on routine work. |
| PM-001-b | 42 | act | ask | Landlord's contractor finished the tree job and the landlord pays directly: close. |
| PM-002-a | 16 | ask | - | Replacement toilet quote is beyond the approved attendance: send it to the landlord. |
| PM-002-b | 43 | escalate | wait | Closed job keeps being auto-paused and returning to the dashboard: system contradiction. |
| PM-004-a | 4 | ask | - | Quote-only checkout clean on a vacant flat: ask the contractor to quote, do not book. |
| PM-004-b | 36 | act | ask, wait | Approved £90 clean reported done with the invoice sent: forward it and close. |
| PM-005-a | 10 | ask | - | Contractor says the quote was uploaded but none is visible: ask for it again. |
| PM-005-b | 16 | act | - | Landlord approved the £205 cleaning quote: instruct within that scope. |
| PM-006-a | 8 | ask | wait | 3+ reminders unanswered for a check-out works quote: chase the contractor. |
| PM-006-b | 15 | act | - | Landlord said "Pls go ahead" to the £605 itemised quote: instruct the contractor. |
| PM-007-a | 15 | act | - | Quote approved; the "not tenanted" pause is expected for check-out works: instruct. |
| PM-007-b | 33 | escalate | ask | Invoice £240.00 from Willow Homes against Clarke's approved £238.04: mismatch. |
| PM-008-a | 9 | ask | - | Landlord asks for a comparison quote: get a second quote, do not book. |
| PM-008-b | 38 | act | escalate | Landlord picks Eliza's £1,370 quote after long confusion: instruct her. |
| PM-009-a | 13 | wait | - | Tenant promises garden photos tomorrow: dated follow-up. |
| PM-010-a | 8 | wait | ask | Tenant agreed by phone to send the solar meter photo: dated follow-up. |
| PM-011-a | 6 | ask | wait | No landlord reply in 3 days on a routine dishwasher fault: chase the landlord. |
| PM-011-b | 19 | ask | - | £95 dial quote after the approved inspection: landlord approval needed. |
| PM-012-a | 4 | ask | - | Fault unconfirmed after a stale thread: troubleshooting and call-out warning to the tenant. |
| PM-012-b | 11 | act | - | Troubleshooting failed and the landlord already agreed: book the engineer. |
| PM-013-a | 25 | ask | wait | No work results two days after the visit, and contractor emails unreadable: ask the contractor. |
| PM-014-a | 9 | ask | escalate | Landlord proposes a key workaround for the door with glass risk: ask the tenant to try it. |
| PM-014-b | 12 | act | escalate | Workaround works and the tenant will monitor: close. |
| PM-016-a | 22 | act | - | Door settled naturally and no invoice is needed: close. |
| PM-018-a | 12 | wait | ask | Reminders unanswered, but the gardener is known to be on holiday: dated follow-up. |
| PM-019-a | 25 | act | - | Landlord approved removal at about £600: instruct the removal only. |
| PM-020-a | 18 | escalate | ask | Report notes an unapproved tenant dog flap while the summary says "no issues". |
| PM-024-a | 6 | ask | - | Oven broken since move-in despite troubleshooting: landlord approval for an engineer. |
| PM-025-a | 24 | wait | ask | Warranty question with the supplier and the landlord asking for news: update and hold. |
| PM-025-b | 38 | ask | escalate | Weeks without an oven and contractor silent after three calls: chase hard. |
| PM-027-a | 1 | ask | - | Slow bath drain, normally the tenant's: troubleshooting first, with a cost warning. |
| PM-027-b | 7 | act | - | Tenant cleared the drain with a plunger: close. |
| PM-028-a | 9 | wait | - | Landlord's own contractor is fixing the pipe; the address in the forward is noise: follow up. |
| PM-029-a | 10 | wait | ask | Tenant says the crack pre-dates the tenancy; contractor already booked: hold, no charge. |
| PM-030-a | 20 | ask | - | Contractor booked and asks about access: ask the tenant who will be home. |
| PM-030-b | 39 | act | ask | Ball valve fitted and taps fine after a missed visit: close-out. |
| PM-031-a | 16 | ask | wait | Contractor's post-visit email is unreadable: ask for the result and invoice. |
| PM-031-b | 22 | act | ask | Contractor twice asks to close a completed job: close-out. |
| PM-032-a | 24 | act | ask | Thumbs-up from the landlord on the £172.51 plus VAT quote: instruct. |
| PM-033-a | 19 | ask | - | Bath taps and TRV quote after the approved attendance: landlord approval. |
| PM-033-b | 37 | act | ask | Completion email names another property (noise): close-out, no invoice approval. |
| PM-034-a | 10 | act | ask | Shower fixed on the call-out with an invoice sent: close-out. |
| PM-035-a | 9 | wait | ask | Landlord fitting the parts himself: dated follow-up. |
| PM-036-a | 30 | escalate | ask | Contractor's own faulty tap still failing after repeated reschedules. |
| PM-036-b | 43 | ask | wait, escalate | Landlord complains about delay and missing photos: ask for photos and confirm no charge. |
| PM-037-a | 2 | ask | escalate | Leaking "shower cable": landlord approval and tenant photos. |
| PM-038-a | 3 | ask | - | Tenant offers to replace the landlord's washing machine: landlord consent. |
| PM-038-b | 9 | act | ask | Landlord agrees to the tenant's machine: inform and close. |
| PM-039-a | 6 | ask | - | Clicking washing machine, troubleshooting done: landlord approval. |
| PM-039-b | 17 | act | ask | Contractor books Monday; call summary says Sunday at another address (noise): confirm. |
| PM-040-a | 9 | wait | ask | Tenant swapped machines while the landlord approved an inspection: update the landlord, follow up, do not close. |
| PM-041-a | 21 | wait | ask | Landlord's operative failed and the installer is being called: dated follow-up. |
| PM-041-b | 23 | act | wait | Landlord confirms the machine fixed (towel rail separate): close. |
| PM-042-a | 24 | act | ask | Invoice £75.11 after the approved engineer visit: close-out with the accurate amount. |
| PM-044-a | 4 | ask | - | Hold says "waiting for LL", but no landlord email was ever sent: ask. |
| PM-044-b | 20 | act | ask | "3+ reminders" alert is stale: the contractor already reported the job done. |
| PM-045-a | 6 | ask | - | Vague window request not raised by the landlord: ask the landlord and tenant. |
| PM-045-b | 25 | wait | ask | Landlord's windows still being made: dated follow-up. |
| PM-047-a | 10 | ask | - | Landlord sends a plumber for the already-fixed toilet: redirect to the window. |
| PM-047-b | 33 | escalate | ask | Two months of passive holds and unclear job ownership. |
| PM-048-a | 17 | act | ask | Window fixed; the completion names another property (noise): close-out. |
| PM-049-a | 7 | ask | - | Landlord prefers the tenant to fix the shed door: ask the tenant. |
