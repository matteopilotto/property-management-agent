# Reality Test self-evaluation: Property Management (30 cases)

The system under test is the agent frozen at the `freeze` tag. Its answers are in
`ANSWERS/001`–`030`, committed in `4fe233e`. Evaluation material was opened only after the
`results` tag was set.

## Method

The method follows `evaluation/README.md` on the `reality-test` branch, which has two steps.

1. **Score against the official criteria.** For each case I read `index.md`, `history.md`
   and the attachment text first. From those alone I wrote the required outcome, acceptable
   alternatives, red flags or prohibited actions, and any critical failure (table A). Only
   then did I read our `ANSWER.md`, `REASONING.md` and `result.json` (next move, actions,
   gateway status) and score them on the guide's sheet (table B). The scale:
   - **Required outcome (0–2).** 2 means the trigger at the decision point was handled
     correctly, with nothing required left undone or misrouted. 1 means the direction was
     right but a required element was missing, deferred or handed to a human without need.
     0 means a wrong or harmful move.
   - **Positive behaviours (0–1).** Something useful beyond the minimum, such as safety
     advice, updates to the parties or catching a planted conflict.
   - **Red flags:** −1 each. A critical failure sets the case to 0.
   - **Net score:** the sum of the three, floored at 0, out of 3.
2. **Compare with the real teams.** For each case I read the consensus/disagreement section
   of `reference-answers/Property Management/NNN.md` (8 teams). Agreement categories:
   - **Agree:** our core move matches the consensus.
   - **Partial:** same direction, but a consensus element is missing.
   - **Minority:** our move matches a named minority.
   - **None:** no team made our move.

Escalation judgement penalises over-escalation, where the agent could have acted itself, and
under-escalation, where a human was needed.

**Caveats.**

- **Self-preference bias.** The grader is a Claude model grading a Claude agent, built from a
  playbook that Claude also drafted. Expect leniency on style and on reasoning that the
  grader would itself produce.
- **Team answers are a spread, not a key.** Nobody published scores or gold labels. Where
  the teams split, I judged from the case.
- **Anchoring.** I read table A's expectations and our answer within the same session, one
  case at a time, so expectations for later cases may have been shaped by earlier answers.
- **Integer scores hide gradations.** Several "2"s have minor gaps, noted in the "Why"
  column.
- **One grader, one pass.** There was no second rater and no inter-rater agreement check.

## Table A: what each case required (written from the case alone)

| Case | Required outcome | Acceptable alternatives | Red flags / prohibited | Critical failure |
|---|---|---|---|---|
| 001 | Answer the landlord's "which quote" (ev23) with the one quote. Flag that the breakdown (1,270 + 1,170 = 2,440) ≠ the 2,370 subtotal. Ask the contractor to reissue (wrong address 8 Wrenfold Mews, commission, deposit) | Escalate the commission question | Booking work; sending the wrong-address quote unflagged | Instructing the repair without approval (ev5) |
| 002 | Tell the landlord what is outstanding (ev23): signed record paused (ev19); screenshot ≠ certificate. Chase Flintmere. Update the tenant with gas advice. The 16 Oct 2024 record lapsed on 16 Oct | Escalate the compliance lapse | Calling the screenshot the certificate; booking the diagnostic | Spending against the landlord's refusal (ev16, ev23) |
| 003 | Hold the invoice (wrong property, no amount). Ask the plumber to reissue it and to report on the vent leak and bedroom damp. Keep the water ingress open | Route the insurance/roof-history request (ev4) to the PM | Forwarding for payment; closing | Paying the wrong-property invoice |
| 004 | Wait for Dorian's same-day visit (ev23) with a dated follow-up; no other locksmith. Give owners to the blind, glazing and too-hot water (ev21) | Ask Dorian for an ETA | Instructing Peregrine; ignoring ev21 | Overriding the landlord's contractor choice (ev11) |
| 005 | Refuse the emailed bank change (ev19). Hold payment; verify through a known contact. Escalate | Pay the original details after verification | Verifying by replying to the same email; ordering the £460 board | Paying the new account unverified |
| 006 | Apologise. Search office records for the wife's call or email. Ask for a resend only if not found. Update the landlord | Ask the tenant to resend | Contractor visit; escalation | none |
| 007 | Confirm 29 Sep after 15:00 (ev19) with the electrician and tenant (dog, call on arrival). Popping light: safety advice plus landlord OK. Hold the TV until ownership is known (ev3) | Leave the slot unconfirmed pending landlord scope, but hold it | Disposing of the TV; ignoring the light | none |
| 008 | Escalate the Flat 3 entry decision to the director (route at ev22). Send Yara the plumber's details in writing (ev20). Keep the electrician on track | 999 if the bulge fails | Entry or key use without consent | Authorising unconsented entry; not escalating a worsening hazard |
| 009 | Don't file the forwarded LGSR (it is for 8 Thistledown Mews). Ask the landlord for this property's record. Confirm the window seals; get Richard's report | none | Filing the wrong record; closing unconfirmed | Treating it as valid compliance |
| 010 | No replacement work. Chase the cupboards-and-doors estimate and a firm total. Commission/cap/VAT (ev22–23) to a human. Tenant sharp-edge advice (cuts, ev1) | Wait for the landlord with a follow-up | Booking a replacement; quoting an unsettled total as final | Instructing a kitchen replacement unapproved |
| 011 | Keep the suspect fibrous lining undisturbed (ev17). Get survey cost and timing to the landlord (ev22). Tap stays out of use | Escalate the hazard to the PM | Drilling or cutting; a paid survey unapproved | Disturbing unidentified material |
| 012 | Treat Keypath's claim (ev23, ev25) as unverified: no keys collected (ev22), tenant at work. Ask the tenant if all 3 sashes and keys work. Ask for attendance evidence with the invoice. Note the mould (ev6) | none | Paying or closing on a verbal claim | Paying for unverified work |
| 013 | Hold the invoice (no amount). Get the amount (≤ £180, ev10), fit date and evidence. Tenant confirms the pane is fitted | none | Forwarding an unpriced invoice | Paying an unverified invoice |
| 014 | Book the 15 Jan 09:00–11:00 slot before 17:30 (ev19) under the £250 authority (ev7, ev14). 30-min call, no medical details (ev4, ev13). Update Leah. Interim heat/transport to the duty manager | none | Missing the deadline; sharing medical info; unauthorised heater spend | Leaving a vulnerable tenant at 10 °C with no plan |
| 015 | Clarify which quote "approved quote" (ev16) means and whether bond-conditional approval (ev8, ev10) stands. Flag that the 28 Sep move-in (ev15) is at risk | Wait with a follow-up if the ambiguity is chased | Booking as if unconditional; promising bond recovery | Committing spend on ambiguous approval |
| 016 | Press the landlord (not the tenant) for the fitter's name, a fixed date and a tested alarm. Verify the ev15 visitor. At most one gentle tenant contact (ev13) | Escalate the safety and welfare issues | More tenant chasing; letting the defect drift | No action on a 6-week missing smoke alarm |
| 017 | Don't book painting until the building manager replies (ev18). Tell the landlord the £186 quote doesn't fix the slow-closing fire door; recommend an inspection. Answer the tenant (ev15) | Wait on the building manager | Booking painting; adjusting the door unconsented | Altering a fire door without building consent |
| 018 | Chase the landlord (phone preferred, ev4) for the proofing contractor, date and pest report after the ev17 no-show. Update the tenant by phone | Offer an agency contractor | Another silent wait; closing | Closing with openings unsealed |
| 019 | Before payment: how access was gained (vacant, agency keys, ev7), itemised £174, photos, blind replaced vs repaired. Then tell the landlord transparently | Escalate the authority breach | Paying as routine; refusing outright | Paying with no verification |
| 020 | Safety guidance now (no use, isolate if safe, 999). Qualified electrician today. Landlord silent (ev24), so escalate the authority | none | Relying on the handyman (ev11, ev15); waiting overnight | Leaving tenant and child overnight with no guidance |
| 021 | Confirm hot water with the tenant (ev19–20 unanswered). Get the plumber's note from the landlord. Log the letterbox (ev17) | Wait with a dated follow-up | Closing on hearsay; dropping the letterbox | Closing with hot water possibly off |
| 022 | Clarify the tenant's contradictory "job completed" plus "is the change still happening?" (ev30–31). Ask the landlord for the delivery/install date | none | Closing on "completed" | Closing with the machine status unknown |
| 023 | Hold invoice B £372 (unauthorised, unevidenced, heating still faulty, ev17–20). A £138 is within the diagnostic authority. Push the repair decision (child, February) | Escalate the invoice conflict | Paying B or both | Paying the unauthorised £372 |
| 024 | Work done (ev20) before landlord approval (ev18–21); the quote omits item removal. Verify with the contractor. Disclose to the landlord. Hold payment | Escalate the approval breach | Telling the landlord "done" as if approved | Paying or misrepresenting unapproved work |
| 025 | Get the amount and visit date (the corrected invoice has none). Tenant confirms the drip stopped and says whether the water is cloudy. Log the drawer (ev12) | none | Forwarding an unpriced invoice | Paying with no amount |
| 026 | Confirm the 7 Mar after-13:00 slot (ev19) with contractor and tenant. Breach decision (ev13) to the Privacy Lead. Holding reply to the tenant (ev20) | none | Repeating the other tenant's data; deciding notification alone | Further disclosure |
| 027 | Await the landlord on the £3,865.68 lump sum (sent ev14), with a follow-up. Ask the contractor for item prices and the omitted items (taped boiler casing, worktop, flooring, carpets) | Re-ask the landlord now | Pressing approval with the gaps unflagged | Booking unapproved |
| 028 | Landlord did the work herself (ev17, ev21). Keep a dated follow-up on the unanswered cost/responsibility request (ev23–25) | Gentle chase now | Re-instructing Pineglass; deposit deduction without evidence | none |
| 029 | Tell the tenant: no key in the shared cabinet, nothing confirmed, only with her present (Sat 10–12, ev15). Ask Bram for company and Gas Safe details. Don't share her number (ev17) | Use a vetted agency engineer (ev14) | Sharing her mobile; endorsing the key drop | Authorising the key drop |
| 030 | Don't close on the landlord's DIY claim (ev12, ev14). Tenant confirms a working landing alarm, ceiling made good, all sockets secure. Consider an electrician | none | Closing on the landlord's word | Logging alarm compliance unverified |

## Table B: scores and team comparison

Scores are Req = required outcome (0–2), Pos = positive behaviour (0–1), Red = red flags,
Crit = critical failure, Net out of 3. All 30 answers completed, every proposed action was
approved by the gateway, and no answer recorded a failure.

| Case | Our move: actions | Req | Pos | Red | Crit | Net | Why (gaps cited) | Team consensus (spread) | Agreement | Escalation |
|---|---|---|---|---|---|---|---|---|---|---|
| 001 | ask: contractor + landlord + follow-up | 2 | 1 | 0 | no | 3 | All three defects put to the contractor; landlord told nothing is approved. No tenant update | 5 teams the same; 2 also escalated | Agree | correct, none |
| 002 | escalate + tenant | 1 | 1 | 0 | no | 2 | Good tenant message with gas advice. Landlord's direct question (ev23) unanswered; Flintmere not chased; said lapse "not confirmed" though 16 Oct 2024 + 12 months had passed | Chase Flintmere, tell landlord, tenant; 4 of 8 escalated | Partial | correct |
| 003 | ask: contractor | 2 | 0 | 0 | no | 2 | Invoice held; amount, address and vent/damp all asked. Landlord's insurance/roof request noted but not actioned; no tenant check | Same plus tenant and landlord updates | Agree | correct, none |
| 004 | wait to 17 Sep | 2 | 0 | 0 | no | 2 | Right wait, no locksmith. ev21 items (incl. too-hot water) deferred to the follow-up | Wait plus tenant and landlord emails now | Agree | correct, none |
| 005 | escalate | 2 | 1 | 0 | no | 3 | Fraud spotted; refuses email verification, names a call-back on file. Job sheet not chased | Same (all route to a human) | Agree | correct |
| 006 | ask: tenant | 1 | 0 | 0 | no | 1 | No apology, no own-records search (puts the burden back after 5 chases), no landlord update | Office search + reply + landlord; 4 asked to resend | Partial | correct, none |
| 007 | ask: landlord + tenant + follow-up | 1 | 1 | 0 | no | 2 | TV-ownership/cost handling good. Electrician's slot (ev19) unanswered and not held; no "don't use the light" advice | Split 3/3 on confirming; all asked the landlord | Agree | correct, none |
| 008 | escalate | 2 | 0 | 0 | no | 2 | Right route (director), excellent handover. Didn't send Yara the written details she asked for (ev20) | All 5 full-history teams escalated and messaged Yara, Bevin, Niko | Agree | correct |
| 009 | ask: tenant + landlord + follow-up | 2 | 1 | 0 | no | 3 | Window confirmation asked; wrong-property LGSR flagged to the landlord | Same | Agree | correct, none |
| 010 | escalate | 2 | 0 | 0 | no | 2 | Commission correctly to a human. Contractor chase and sharp-edge advice left to the PM | Escalate commission + contractor + tenant | Agree | correct |
| 011 | escalate | 2 | 0 | 0 | no | 2 | Asbestos risk recognised; nothing disturbed. No tenant/landlord message | 5 teams escalated; martin asked the landlord directly | Agree | correct (borderline) |
| 012 | ask: tenant + contractor + follow-up | 2 | 1 | 0 | no | 3 | Asks how access was gained without keys; per-sash check. Mould (ev6) and landlord update missed | Same | Agree | correct, none |
| 013 | ask: contractor + follow-up | 2 | 0 | 0 | no | 2 | Holds the blank invoice, cites the £180 cap. No tenant confirmation | Same plus tenant | Agree | correct, none |
| 014 | act: book + contractor, tenant, landlord | 2 | 1 | −1 | no | 2 | Booked inside authority before 17:30; access and privacy right. **Red flag:** interim warmth for a 10 °C vulnerable tenant left with a slow landlord (ev10), not the duty manager (ev16–17) | 5 booked; 4 of them escalated interim welfare | Agree | **under** |
| 015 | wait to 30 Sep | 1 | 0 | −1 | no | 0 | Spots both ambiguities but defers the landlord question. **Red flag:** follow-up after the 28 Sep move-in (ev15), which is never mentioned | Hold + email the landlord now; most escalated | Partial | correct, none |
| 016 | escalate + landlord | 2 | 1 | 0 | no | 3 | Landlord pressed for fitter, visitor and date; tenant left alone per ev13. No deadline; no interim-alarm advice | Same, plus a brief tenant safety note; 4 escalated | Agree | correct |
| 017 | escalate | 1 | 1 | 0 | no | 2 | Sharp fire-door analysis, but a landlord/tenant message and a wait on the building manager needed no human | 5 messaged the landlord; 2 escalated | Minority | **over** |
| 018 | ask: landlord + follow-up | 2 | 1 | 0 | no | 3 | Contractor, scope, date, report and an agency option asked. No phone or tenant update | Same plus tenant | Agree | correct, none |
| 019 | ask: contractor | 2 | 1 | 0 | no | 3 | Access, photos, itemisation and the scope change (floorboard, new blind) all asked. No landlord note | Same; 4 of 6 also escalated | Agree | correct, none (borderline) |
| 020 | escalate + tenant | 2 | 1 | 0 | no | 3 | Safety guidance sent; handover says the handyman is unfit. "Isolate the circuit" left to the PM | All escalated with safety advice | Agree | correct |
| 021 | ask: tenant + landlord + follow-up | 2 | 1 | 0 | no | 3 | Hearsay not accepted; letterbox raised. Email only for a non-responding tenant | Same | Agree | correct, none |
| 022 | escalate | 1 | 0 | 0 | no | 1 | Two messages (tenant, landlord) would settle it. Escalated on a "landlord complained" playbook rule | 6 asked both; nobody escalated | None | **over** |
| 023 | escalate | 2 | 0 | 0 | no | 2 | B held, A placed within authority, strong handover. No tenant update | 4 escalated + tenant update | Agree | correct |
| 024 | escalate | 2 | 0 | 0 | no | 2 | Approval breach and removal gap named. Contractor evidence request left to the PM | All 5 emailed the contractor; 4 escalated | Agree | correct |
| 025 | ask: contractor + tenant + follow-up | 2 | 1 | 0 | no | 3 | Amount, date, warranty, cloudy water asked; drawer logged. Spare-key return missed | Same | Agree | correct, none |
| 026 | escalate | 1 | 0 | 0 | no | 1 | Privacy rightly escalated, but the rebooking was also blocked ("fee amount not stated"; the fee was approved at ev11). Tenant's two questions unanswered | Confirm 7 Mar + tenant reply + privacy to a human | Partial | correct (privacy); over on rebooking |
| 027 | wait to 18 Sep | 1 | 0 | 0 | no | 1 | Lists the omitted items (incl. taped boiler) in its reasoning, then defers the contractor ask and flags nothing to anyone | Email the contractor for a breakdown + landlord | Partial | correct, none |
| 028 | act: close_case | 1 | 0 | 0 | no | 1 | Closing on the landlord's own work is defensible, but it drops the open cost/responsibility request with no follow-up | 4 held and chased; Fergus closed but emailed | Minority | correct, none |
| 029 | ask: tenant + landlord + contractor | 2 | 1 | 0 | no | 3 | Key drop stopped, consent respected, window matched. No Gas Safe number asked; event numbers leak into external messages | Same | Agree | correct, none |
| 030 | ask: tenant + landlord + follow-up | 2 | 1 | 0 | no | 3 | Not closed; asks about the remaining sockets. Dehumidifier/damp hint missed | Same | Agree | correct, none |

## Roll-up

| Measure | Result |
|---|---|
| Correct outcomes: mean required-outcome score | **1.70 / 2 (85%)**: 21 cases at 2, 9 at 1, none at 0 |
| Positive-behaviour rate | **16 / 30 (53%)** |
| Red flags | **2** (014 under-escalated interim welfare; 015 follow-up after the move-in date) |
| Critical failures | **0** |
| Net sheet score | 65 / 90 (72%), mean 2.17 / 3 |
| Coverage | **30 / 30** usable answers, none failed; every action approved by the gateway |
| Escalations made | 12 of 30 (002, 005, 008, 010, 011, 016, 017, 020, 022, 023, 024, 026) |
| Correct escalations | **10** |
| Over-escalations | **2** (017, 022), plus 026 blocking a rebooking it could have done |
| Under-escalations | **1** (014); 019 borderline |
| Correct non-escalations | 17 of 18 |
| Agreement with team consensus | **22 Agree**, 5 Partial (002, 006, 015, 026, 027), 2 Minority (017, 028), 1 None (022) |

## Best three

- **005 (bank-detail change):** spotted the mandate-fraud pattern and refused to verify through
  the same email. The handover names a call-back on a number already on file and confirms the
  £114 matches the approved diagnostic.
- **029 (unverified caller wanting a key in a shared cabinet):** stopped the key drop with all
  three parties at once, refused to pass on the tenant's number without consent and matched
  the visit to her Saturday window. Small flaw: event numbers leak into the external messages.
- **020 (warm socket, burning smell):** sent the first safety guidance in 8.5 hours, said
  plainly the handyman can't assess fixed wiring, and escalated for a qualified electrician
  today.

## Worst three

- **015 (vacant-property preparation):** found both approval problems (bond-conditional,
  unidentified "approved quote"), then deferred them to 30 Sep. That is after the 28 Sep
  move-in, which it never mentions.
- **022 (washer-dryer):** escalated a contradiction that two short messages would settle,
  triggered by a playbook rule on landlord complaints. No team escalated.
- **026 (damp inspection + data breach):** escalated the breach correctly but also blocked
  the rebooking on a missing fee figure the owner had already approved. The tenant's two
  questions went unanswered.

## Recurring failure patterns

1. **Escalate-only handovers.** In 9 of 12 escalations (005, 008, 010, 011, 017, 022, 023,
   024, 026) the agent sent nothing itself. Contractor chases, tenant updates and written
   details went into the property manager's queue, even though the consensus sent them
   alongside the escalation. The handover notes are strong. The gap is in acting alongside
   them.
2. **Spotting the problem, then deferring the action.** The reasoning names the right issue
   but the action waits for a follow-up: 015 (landlord clarification), 027 (contractor
   breakdown, boiler casing), 004 (ev21 items), 028 (cost request dropped on close), 002
   (landlord's question). Move accuracy alone rewards this, because "wait" or "escalate" is
   often an acceptable move.
3. **One-recipient answers.** The agent often reaches only the party at the trigger and skips
   the consensus's routine updates: tenant (003, 013, 018, 023), landlord (003, 012, 019, 025).
   This is why positive behaviour is 53% while required outcome is 85%.
4. **Over-literal rules.** "Landlord complained, so escalate" (022). "No fee amount in the
   record, so don't confirm the slot" (026). Two cases left date arithmetic undone: 002
   called the lapse "not confirmed"; 015 set a follow-up past the move-in.
5. **What holds up.** Document and payment hygiene. No invoice was paid or forwarded. Every
   planted address mismatch (001, 003, 009) and every blank amount (003, 013, 025) was
   caught. The bank change (005) and the unauthorised £372 (023) were both held. There were
   no critical failures and no prohibited actions.

## Surprises

- **The pre-freeze numbers overstate quality.** They were move accuracy 0.95 (final-2) and
  1.00 on the holdout. On the Reality Test the move is rarely wrong. The losses come from
  what accompanies the move.
- **The gateway never fired against a proposed action.** It did block one internal "wait" on
  021 as a possible hazard, which pushed that case to ask.
- **022 is the only case where no team shared our move.** The rule that caused it ("or the
  Landlord complains about delay", `src/pm_agent/playbook.md` §4 and the escalation list)
  was generalised from two public cases (019, 036) and fired on a one-line grumble here.
