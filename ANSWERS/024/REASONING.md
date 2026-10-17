# Case 024: reasoning

## Facts

- Quote is £180 + VAT = £216 from Larkspan Property Care (event 11, property-service-quotation.pdf).
- Landlord approval was requested on 18 Sep and chased on 21 Sep, with no reply recorded (events 18, 19).
- The workflow is still at landlord quote approval on 24 Sep (events 17, 21).
- A note says the clear-out and property service was done on 23 Sep (event 20).
- A deposit claim decision was pending before work proceeds (events 15, 16).

## Conflicts

- The approval flag says approval was already obtained (events 2, 5), but no approval exists and approval was later requested (events 18, 19).
- Event 20 says the work was done, but no instruction, completion message or invoice exists and the approval workflow is open (event 21).
- The quote scope is cleaning only and omits the requested item removal (event 11, events 14 and 10).

## Missing

- Landlord approval or rejection of the quote.
- Contractor confirmation of attendance, scope, completion photos and invoice.
- Deposit claim decision.

## Options rejected

- Instruct or book Larkspan: no landlord approval is on record.
- Chase the landlord again (ask): the work may already have been done unapproved, which needs a property manager decision. It would take two messages (landlord and contractor) to settle.
- Wait: this would leave the case drifting.
- Close or tell the landlord the job is done: completion is unverified.

## Uncertainty

It is unknown who did the work on 23 Sep, or whether the note in event 20 is accurate.
